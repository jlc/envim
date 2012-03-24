# Events.py
#
# Copyright (c) 2012, Jeanluc Chasseriau <jeanluc@lo.cx>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of ENSIME nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Aemon Cannon BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from VimHelpers import *
from Helper import SimpleSingleton, Logger

@SwankEventBackgroundMessage
def backgroundMessage(code, details):
  Logger().debug('Background message: '+codeDetailsString(code, details))
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
    Logger().debug("Full scala notes list, clear previous list")

    qflist = notesToQuickFixList(notes.notes)
  else:
    Logger().debug("Partial scala notes list")

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
  Logger().debug("Clear all Scala notes")

  setQuickFixList([])

  State().scalaNotes = []

@SwankEventJavaNotes
def javaNotes():
  echoe("Java notes: TODO to implement")

@SwankEventClearAllJavaNotes
def clearAllJavaNotes():
  #echoe("Clear all Java notes: TODO to implement")
  pass


