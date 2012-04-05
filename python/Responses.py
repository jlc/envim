# Responses.py
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

import logging
from VimHelpers import *
from Helper import SimpleSingleton

log = logging.getLogger('envim')

@SimpleSingleton
class ConnectionInfoHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("ConnectionInfo abort: "+codeDetailsString(code, details))

  def response(self, r):
    spid = ""
    if (r.pid): spid = str(r.pid)

    echo("server: "+r.implementation.name+" ("+r.version+") "+spid)

    configFile = os.getcwd() + '/' + '.ensime'
    if not os.path.isfile(configFile):
      # todo: set a variable and add a function so to be able to restart connection-info
      echoe("Ensime configuration file ("+configFile+") doest not exist")
      return

    config = ensimeConfigToPython(configFile)

    SwankRpc().projectInit(config)(InitProjectHandler())

@SimpleSingleton
class InitProjectHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("InitProject abort: "+codeDetailsString(code, details))

  def response(self, r):
    echo("Initializing project: "+str(r.project_name))

    for src in r.source_roots:
      log.debug("project source roots: "+src)

    State().initialized = True

@SimpleSingleton
class ShutdownServerHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("ShutdownServer abort: "+codeDetailsString(code, details))

  def response(self, r):
    echo("Ensime server is now off")

@SimpleSingleton
class TypecheckFileHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("TypecheckFile abort: "+codeDetailsString(code, details))

  def response(self, r):
    if r: echo("Typechecking in progress...")
    else: echoe("Typecheck file error")

@SimpleSingleton
class TypecheckAllHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("TypecheckAll abort: "+codeDetailsString(code, details))

  def response(self, r):
    if r: echo("Typechecking in progress...")
    else: echoe("Typecheck all error")

@SimpleSingleton
class SymbolAtPointHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("SymbolAtPoint abort: "+codeDetailsString(code, details))

  def response(self, symbolInfo):
    if not symbolInfo:
      echo("No symbol here")
      return

    # Example:
    # Result for a val:
    # (:return (:ok (:name "toto" :type (:name "String" :type-id 1 :full-name "java.lang.String" :decl-as class) :decl-pos (:file "/Users/jeanluc/Source/vim/test_vim_ensime/src/main/scala/HelloWorld.scala" :offset 64) :owner-type-id 2)) 47)

    # Result for a method:
    #(:return (:ok (:name "println" :type (:name "(x: Any)Unit" :type-id 2 :arrow-type t :result-type (:name "Unit" :type-id 3 :full-name "scala.Unit" :decl-as class) :param-sections ((:params (("x" (:name "Any" :type-id 1 :full-name "scala.Any" :decl-as class)))))) :is-callable t :owner-type-id 4)) 45)

    # Fields may be defined depending on the type we are accessing

    out = symbolInfo.name + ' : ' + symbolInfo.type.name

    decl_as = ''
    if hasattr(symbolInfo.type, 'decl_as'):
      decl_as = symbolInfo.type.decl_as

    full_name = ''
    if hasattr(symbolInfo.type, 'full_name'):
      full_name = symbolInfo.type.full_name

    if decl_as != '' or full_name != '':
      out += ' (' + decl_as + ' ' + full_name + ')'

    echo(out)

@SimpleSingleton
class UsesOfSymbolAtPointHandler(SwankCallHandler):

  def abort(self, code, details):
    echoe("SymbolAtPoint abort: "+codeDetailsString(code, details))

  def response(self, rangePosList):
    if not rangePosList:
      echo("Symbol not used")
      return

    qflist = rangePosToQuickFixList(rangePosList)

    setQuickFixList(qflist)


