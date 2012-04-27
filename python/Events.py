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
from EnvimOutputs import *
from VimHelpers import *

log = logging.getLogger('envim')

@SwankEventBackgroundMessage
def backgroundMessage(code, details):
  s = codeDetailsString(code, details)
  log.info('Background message: '+s)
  echo(s)

@SwankEventReaderError
def readerError(code, details):
  s = codeDetailsString(code, details)
  log.error('Reader error: '+s)
  echo(s)

@SwankEventCompilerReady
def compilerReady():
  State().compilerReady = True
  echo("Compiler ready")

@SwankEventIndexerReady
def indexerReady():
  State().indexerReady = True
  echo("Indexer ready")

@SwankEventFullTypecheckFinished
def fullTypecheckFinished():
  echo("Full typecheck finished")

  qflist = notesToQuickFixList(State().scalaNotes)
  QuickFixOutput().set(qflist)
  QuickFixOutput().open()

@SwankEventScalaNotes
def scalaNotes(notes):
  # notes.is_full True|False
  # notes.notes = []

  if notes.is_full:
    log.debug("scalaNotes: Full scala notes list, clear previous list")
  else:
    log.debug("scalaNotes: Partial scala notes list")

    # here we prepend existing notes
    notes.notes.reverse()
    State().scalaNotes.reverse()
    notes.notes.extend(State().scalaNotes)
    notes.notes.reverse()

  State().scalaNotes = notes.notes

  echo("Typechecking in progress...")

@SwankEventClearAllScalaNotes
def clearAllScalaNotes():
  log.debug("clearAllScalaNotes: Clear all Scala notes")

  QuickFixOutput().clear()

  State().scalaNotes = []

@SwankEventJavaNotes
def javaNotes():
  log.debug("javaNotes: TODO: Implement Java notes")
  echoe("Java notes: TODO to implement")

@SwankEventClearAllJavaNotes
def clearAllJavaNotes():
  log.debug("clearAllJavaNotes: TODO: Implement clear Java notes")


