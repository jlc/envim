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
from EnvimTools import *
from EnvimOutputs import *
from VimHelpers import *
from Helper import *

from SwankProtocol import *

from Responses import *
from Events import *

log = logging.getLogger('envim')

@SimpleSingleton
class Envim:

  @CatchAndLogException
  def __init__(self):
    self.pauseAfter = 0
    self.currentCompletions = self.beginCompletions

  def setPauseAfter(self, pauseAfter):
    self.pauseAfter = pauseAfter

  @CatchAndLogException
  def sendToEnsimeClient(self, data):
    if self.pauseAfter <= 0:
      vim.eval("g:envim.ensimeClientCtx.write('"+data+"')")
    else:
      vim.eval("g:envim.ensimeClientCtx.writeAndPause('"+data+"', %d)" % (self.pauseAfter))
      self.pauseAfter = 0

  @CatchAndLogException
  def connectionAndProjectInit(self):
    SwankRpc().connectionInfo()(ConnectionInfoHandler())

  @CatchAndLogException
  def shutdownServer(self):
    echo("Shuting down Ensime server")
    SwankRpc().shutdownServer()(ShutdownServerHandler())
    State().initialized = False

  @CatchAndLogException
  def typecheckFile(self):
    if not checkCompilerReady(): return

    # @todo: ensure that file is in source-roots
    filename = getCurrentFilename()
    if filename == None:
      echoe("Unknown current filename")
    else:
      SwankRpc().typecheckFile(filename)(TypecheckFileHandler())

  @CatchAndLogException
  def typecheckAll(self):
    if not checkCompilerReady(): return

    SwankRpc().typecheckAll()(TypecheckAllHandler())

  @CatchAndLogException
  def symbolAtPoint(self):
    if not checkCompilerReady(): return

    filename = getCurrentFilename()
    if filename == None:
      echoe("Unknown current filename")
    else:
      #saveFile()
      offset = getCurrentOffset()
      SwankRpc().symbolAtPoint(filename, offset)(SymbolAtPointHandler())

  @CatchAndLogException
  def usesOfSymbolAtPoint(self):
    if not checkCompilerReady(): return

    filename = getCurrentFilename()
    if filename == None:
      echoe("Unknown current filename")
    else:
      offset = getCurrentOffset()
      SwankRpc().usesOfSymbolAtPoint(filename, offset)(UsesOfSymbolAtPointHandler())

  @CatchAndLogException
  def onCursorMoved(self):
    PreviewOutput().close()

  @CatchAndLogException
  def onQuickFixLeave(self):
    QuickFixOutput().close()

  @CatchAndLogException
  def onWinLeave(self):
    pass

  @CatchAndLogException
  def onTabLeave(self):
    PreviewOutput().close()

  @CatchAndLogException
  def completions(self, findstart, base):
    log.debug("Envim.completions: findstart: %d %s base: %s", findstart, str(findstart.__class__), base)

    self.currentCompletions(findstart, base)

  @CatchAndLogException
  def beginCompletions(self, findstart, base):
    log.debug("Envim.beginCompletions:")

    if findstart == 1:

      cmds = [
        "let pos = col('.') -1",
        "let line = getline('.')",
        "let bc = strpart(line,0,pos)",
        "let match_text = matchstr(bc, '\zs[^ \t#().[\]{}\''\";: ]*$')",
        "let completion_result = len(bc)-len(match_text)"
      ]

      vim.command("\n".join(cmds))

      OmniOutput().setStart(int(vim.eval("completion_result")))

    else:
      vim.command("update")

      filename = getCurrentFilename()
      if filename == None:
        echoe("Unknown current filename")
      else:
        offset = getCurrentOffset()

        self.setPauseAfter(1)
        SwankRpc().completions(filename, offset, 0, False)(CompletionsHandler())

      vim.command("let completion_result = []")

      OmniOutput().setBase(base)

      self.currentCompletions = self.showCompletions

    log.debug("Envim.beginCompletions: completion_result: %s", vim.eval("completion_result"))

  @CatchAndLogException
  def showCompletions(self, findstart, base):
    log.debug("Envim.showCompletions:")

    if findstart == 1:
      vim.command("let completion_result = %d" % (OmniOutput().getStart()))

    else:
      results = OmniOutput().getFormatedResults()
      vim.command("let completion_result = %s" % (results))

      self.currentCompletions = self.beginCompletions

    log.debug("Envim.showCompletions: completion_result: %s", vim.eval("completion_result"))

