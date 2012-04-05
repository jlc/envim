# Envim.py
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

