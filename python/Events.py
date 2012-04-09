# Events.py
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

import logging
from EnvimTools import *
from VimHelpers import *

log = logging.getLogger('envim')

@SwankEventBackgroundMessage
def backgroundMessage(code, details):
  log.debug('Background message: '+codeDetailsString(code, details))
  echo(details)

@SwankEventReaderError
def readerError(code, details):
  echoe('Reader error: '+codeDetailsString(code, details))

@SwankEventCompilerReady
def compilerReady():
  State().compilerReady = True
  echo("Compiler ready")

@SwankEventFullTypecheckFinished
def fullTypecheckFinished():
  echo("Full typecheck finished")

@SwankEventIndexerReady
def indexerReady():
  State().indexerReady = True
  echo("Indexer ready")

@SwankEventScalaNotes
def scalaNotes(notes):
  # notes.is_full True|False
  # notes.notes = []

  if (notes.is_full):
    log.debug("Full scala notes list, clear previous list")

    qflist = notesToQuickFixList(notes.notes)
  else:
    log.debug("Partial scala notes list")

    # here we prepend existing notes
    notes.notes.reverse()
    State().scalaNotes.reverse()
    notes.notes.extend(State().scalaNotes)
    notes.notes.reverse()

    qflist = notesToQuickFixList(notes.notes)

  if len(qflist) > 0:
    setQuickFixList(qflist)

  State().scalaNotes = notes.notes

@SwankEventClearAllScalaNotes
def clearAllScalaNotes():
  log.debug("Clear all Scala notes")

  setQuickFixList([])

  State().scalaNotes = []

@SwankEventJavaNotes
def javaNotes():
  echoe("Java notes: TODO to implement")

@SwankEventClearAllJavaNotes
def clearAllJavaNotes():
  #echoe("Clear all Java notes: TODO to implement")
  pass


