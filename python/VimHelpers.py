# VimHelpers.py
#
# Copyright 2012 Jeanluc Chasseriau <jeanluc@lo.cx>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import mmap
import types
import vim
import logging
from SExpression import *
from SwankProtocol import *

log = logging.getLogger('envim')

@SimpleSingleton
class State(object):
  def __init__(self):
    self.initialized = False
    self.indexerReady = False
    self.compilerReady = False
    self.fullTypecheckFinished = False
    self.scalaNotes = []
    self.javaNotes = []

# TODO: Transform checkInitialized() and checkCompilerReady() in to decorator?
def checkInitialized():
  if not State().initialized:
    echoe("Project is not initialized. Ensure you have a .ensime project file and start using `:Envim`.")
    return False
  return True

def checkCompilerReady():
  if not checkInitialized(): return False
  if not State().compilerReady:
    echoe("Compiler is not ready yet.")
    return False
  return True

#
# Vim Helpers functions
#

# normal echo (in vim command line)
def echo(s):
  log.info(s)
  vim.command("echo('"+s+"')")

# error echo (highlighted in vim command line)
def echoe(s):
  log.error(s)
  vim.command("echoe('"+s+"')")

# debug echo (as provided by Decho addon: open a new window)
def decho(s):
  log.debug(s)
  vim.command("Decho('"+s+"')")

def writeToEnsimeClient(data):
  vim.eval("g:envim.swankClientCtx.write('"+data+"')")

def getCurrentOffset():
  return int(vim.eval('line2byte(line("."))+col(".")'))-1

def getCurrentFilename():
  filename = vim.eval("expand('%')")
  if filename != None:
    filename = os.getcwd() + '/' + filename
  return filename


def setQuickFixList(qflist):
  def listOfDictToString(li):
    o = '['

    nlist = len(li)
    for de in li:
      nlist -= 1

      o += '{'
      ndict = len(de.keys())
      for k in de.keys():
        ndict -= 1

        o += "'"+k+"'" + ':'
        if isinstance(de[k], types.StringType):
          o += '"' + de[k].replace('"', '\\"') + '"'
        else:
          o += str(de[k])

        if ndict > 0: o += ','

      o += '}'
      if nlist > 0: o += ','

    o += ']'
    return o

  o = listOfDictToString(qflist)
  log.debug("Quick fix list: ")
  log.debug(o)

  vim.command("call setqflist("+o+")")

  return

  # if we execute these, they won't be any syntax colorization in the qflist window
  # Note: find a way to delay the execution of them
  if len(qflist) > 0:
    vim.command("copen")
  else:
    vim.command("cclose")

def saveFile():
  vim.command("w")

def editAtOffset(filename, offset):
  vim.command("call feedkeys(':e fnameescape("+filename+") |goto "+offset+" |syn on")

#
# Misc tools
#

def codeDetailsString(code, detail):
  return ProtocolConst.toStr(code)+'('+str(code)+') : '+detail

def ensimeConfigToPython(filename):
  try: f = file(filename)
  except:
    log.error("ensimeConfigToPython: unable to open ensime config file ("+filename+")")
    return None
 
  outlist = []

  lines = f.readlines()

  for line in lines:
    line = line.strip()
    
    if line.startswith(';;'): continue

    comment = line.find(';;')
    if comment > 0:
      line = line[:comment].strip()

    if not len(line): continue

    outlist.append(line)

  out = ' '.join(outlist)

  log.debug("ensimeConfigToPython: reading conf:")
  log.debug(out)

  sexp = SExpParser().parse(out)
  py = sexp.toPy()

  if not py.has('root_dir'):
    setattr(py, 'root_dir', os.getcwd())

  log.debug("ensimeConfigToPython: python object:")
  log.debug(py.debugString())

  return py

def notesToQuickFixList(notes):
  # quick fix list format:
  # list = [ { 'filename': xxx, 'lnum': xxx, 'col': xxx, 'text': xxx, 'type': E/W
  # Note: maybe we can highlight the file segment (thx to notes.beg and notes.end)

  vimseverity = {'error':'E', 'warn':'W', 'info':'I'}

  qflist = []
  nr = 1

  for note in notes:
    entry = {
      'filename': note.file,
      'lnum': note.line,
      'col': note.col,
      'vcol': 1,
      'text': note.msg,
      'type': vimseverity[note.severity],
      'nr': nr
    }
    qflist.append(entry)
    nr += 1

    debugs = '['+note.severity+'] '+os.path.basename(note.file)+' l.'+str(note.line)+' c.'+str(note.col)
    debugs += ' : '+note.msg

    log.debug(debugs)

  return qflist

# NOTE: this is quite ugly and inefficient: find how vim can help here
def offsetToLineCol(filename, offset):
  try:
    f = open(filename, 'r+')
    buf = mmap.mmap(f.fileno(), 0)
    f.close()
  except Exception as detail:
    log.error("offsetToLineCol: unable to open file ("+filename+") : "+str(detail))
    return None

  found = False
  lastPos = buf.tell()
  lineno = 1
  col = 0
  line = ""

  while not found:
    line = buf.readline()
    pos = buf.tell()

    if pos < offset:
      lineno += 1
      lastPos = pos
    else:
      col = offset - lastPos
      found = True

  buf.close()

  if found:
    return (line, lineno, col)

  log.debug("offsetToLineCol: line and column not found for "+filename+":"+str(offset))
  return None

def rangePosToQuickFixList(rangePosList):

  qflist = []
  nr = 1

  for pos in rangePosList:
    r = offsetToLineCol(pos.file, pos.offset)
    if r == None:
      continue
    
    (line, lineNo, colNo) = r

    entry = {
      'filename': pos.file,
      'lnum': lineNo,
      'col': colNo,
      'text': line,
      'vcol': 1,
      'type': 'I',
      'nr': nr
    }
    qflist.append(entry)
    nr += 1

  return qflist


