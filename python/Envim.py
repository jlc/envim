# Envim.py
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

# TODO:
# - update QuickFixList only when received FullTypecheck done
# - test if Analyzer is ready before use TypecheckFile / TypecheckAll

import logging
from VimHelpers import *
from Helper import *

from SwankProtocol import *

from Responses import *
from Events import *

log = logging.getLogger('envim')

@CatchAndLogException
def envimConnectionAndProjectInit():
  SwankRpc().connectionInfo()(ConnectionInfoHandler())

@CatchAndLogException
def envimShutdownServer():
  echo("Shuting down Ensime server")
  SwankRpc().shutdownServer()(ShutdownServerHandler())
  State().initialized = False

@CatchAndLogException
def envimTypecheckFile():
  if not checkCompilerReady(): return

  # @todo: ensure that file is in source-roots
  filename = getCurrentFilename()
  if filename == None:
    echoe("Unknown current filename")
  else:
    SwankRpc().typecheckFile(filename)(TypecheckFileHandler())

@CatchAndLogException
def envimTypecheckAll():
  if not checkCompilerReady(): return

  SwankRpc().typecheckAll()(TypecheckAllHandler())

@CatchAndLogException
def envimSymbolAtPoint():
  if not checkCompilerReady(): return

  filename = getCurrentFilename()
  if filename == None:
    echoe("Unknown current filename")
  else:
    #saveFile()
    offset = getCurrentOffset()
    SwankRpc().symbolAtPoint(filename, offset)(SymbolAtPointHandler())

@CatchAndLogException
def envimUsesOfSymbolAtPoint():
  if not checkCompilerReady(): return

  filename = getCurrentFilename()
  if filename == None:
    echoe("Unknown current filename")
  else:
    offset = getCurrentOffset()
    SwankRpc().usesOfSymbolAtPoint(filename, offset)(UsesOfSymbolAtPointHandler())

