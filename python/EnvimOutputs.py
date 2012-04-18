# EnvimOutputs.py
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

import types
import logging
from VimHelpers import *
from Helper import *

@SimpleSingleton
class ServerOutput(VimBufferHelper):

  def __init__(self):
    VimBufferHelper.__init__(self)
    self.bufferId = 0
    self.filename = "ENSIME_SERVER_OUTPUT"
    self.filters = [] # [ (regex, function, execOnce), ... ]
    self.prefix = "Ensime: "

  # Private

  def _updateBuffer(self, id, f):
    vim.command("call setbufvar(%d, '&modifiable', 1)" % (id))
    f()
    vim.command("call setbufvar(%d, '&modifiable', 0)" % (id))

  def _setDiscret(self):
    options = self.discretBufferOptions()
    self.setBufferOptions(self.bufferId, options)

  # Public

  @CatchAndLogException
  def setupBuffer(self):
    vim.command("badd %s" % (self.filename))
    self.bufferId = int(vim.eval("bufnr('%s')" % (self.filename)))

    log.debug("ServerOutput.setupBuffer: bufferId: %d", self.bufferId)

    options = self.hiddenBufferOptions()
    options.extend([
      ('modifiable', "1")
    ])

    extraCmds = [
      "sbuffer %d" % (self.bufferId),
      "autocmd * %s norm! G$" % (self.filename)
    ]
    
    self.setBufferOptions(self.bufferId, options, extraCmds)

  @CatchAndLogException
  def onServerOutput(self, data):
    def realOnServerOutput(data):
      doAppend = lambda: vim.buffers[self.bufferId-1].append(self.prefix + data)

      #self._updateBuffer(self.bufferId, doAppend)
      doAppend()

      for filter in self.filters:
        regex, fct, execOnce = filter
        if regex.match(data) != None:
          fct(data)
          if execOnce:
            self.filters.remove(filter)
  
    # set discret the first time
    # TODO: rework... discret is not set...
    self._setDiscret()
    self.onServerOutput = realOnServerOutput

    realOnServerOutput(data)

  @CatchAndLogException
  def addFilter(self, regex, fct, execOnce=True):
    self.filters.append( (re.compile(regex), fct, execOnce) )

  @CatchAndLogException
  def showServerOutput(self):
    vim.command("sbuffer %d" % (self.bufferId))
    vim.command("wincmd p")

@SimpleSingleton
class PreviewOutput(VimBufferHelper):
  def __init__(self):
    VimBufferHelper.__init__(self)
    self.bufferId = 0
    self.filename = "ENSIME_PREVIEW"
    self.isOpen = False

  # Private

  # Public

  @CatchAndLogException
  def clear(self):
    log.debug("PreviewOutput.clear: bufferId: %d", self.bufferId)
    id = self.bufferId - 1
    vim.buffers[id][:] = None

  @CatchAndLogException
  def setupBuffer(self):
    vim.command("badd %s" % (self.filename))
    self.bufferId = int(vim.eval("bufnr('%s')" % (self.filename)))

    log.debug("PreviewOutput.setupBuffer: bufferId: %d", self.bufferId)

    options = self.hiddenBufferOptions()
    options.extend([
      ('modifiable', "1")
    ])

    extraCmds = [
      "set previewheight=2",
    ]

    self.setBufferOptions(self.bufferId, options, extraCmds)

  @CatchAndLogException
  def set(self, lines=[]):
    def enc(s): return s.encode('ascii', 'replace')

    if isinstance(lines, types.StringType) or isinstance(lines, types.UnicodeType):
      lines = [enc(lines)]
    elif isinstance(lines, types.ListType):
      lines = [enc(l) for l in lines]
    else: log.error("PreviewOutput.set: lines is not of List neither String type")

    # note: show preview edit before updating it, and then redraw
    # this avoid vim to modify the source file header while setting the content
    # why? and how? haven't been solved yet
    cmds = [
      "pc",
      "pedit %s" % (self.filename),
    ]
    vim.command("\n".join(cmds))

    self.clear()

    id = self.bufferId - 1
    vim.buffers[id][:] = lines

    options = self.discretBufferOptions()
    options.extend([
      ('statusline', "'%='")
    ])

    cmds = [
      "redraw"
    ]

    self.setBufferOptions(self.bufferId, options, cmds)

    self.isOpen = True

  @CatchAndLogException
  def close(self):
    if self.isOpen:
      vim.command("pc")
      self.isOpen = False

@SimpleSingleton
class OmniOutput:
  def __init__(self):
    self.start = 0
    self.base = ''
    self.results = [] # list of dicts

  def setBase(self, base):
    self.base = base

  def getBase(self):
    return self.base

  def setStart(self, start):
    self.start = start

  def getStart(self):
    return self.start

  def setResults(self, results):
    self.results = results

  def getFormatedResults(self):
    s = listOfDictToString(self.results)
    self.results = []
    return s

  def showCompletions(self):
    vim.command("call feedkeys(\"\<c-x>\<c-o>\")")

  def pauseMessages(self):
    vim.command("call abeans#pauseMessages()")

  def continueMessages(self):
    vim.command("call abeans#continueMessages()")

@SimpleSingleton
class QuickFixOutput:
  def __init__(self):
    self.isOpen = False

  def open(self):
    if not self.isOpen:
      cmds = ["copen", "redraw"]
      vimCommands(cmds)
      self.isOpen = True

  def close(self):
    if self.isOpen:
      cmds = ["cclose", "redraw"]
      vimCommands(cmds)
      self.isOpen = False

  def clear(self):
    self.set([])

  def set(self, qflist):
    o = listOfDictToString(qflist)

    cmds = [ 
      "call setqflist(%s)" % (o),
    ]
    vimCommands(cmds)

