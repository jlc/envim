" envim.vim
"
" Copyright (c) 2012, Jeanluc Chasseriau <jeanluc@lo.cx>
" All rights reserved.
"
" Redistribution and use in source and binary forms, with or without
" modification, are permitted provided that the following conditions are met:
"     * Redistributions of source code must retain the above copyright
"       notice, this list of conditions and the following disclaimer.
"     * Redistributions in binary form must reproduce the above copyright
"       notice, this list of conditions and the following disclaimer in the
"       documentation and/or other materials provided with the distribution.
"     * Neither the name of ENSIME nor the
"       names of its contributors may be used to endorse or promote products
"       derived from this software without specific prior written permission.
"
" THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
" ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
" WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
" DISCLAIMED. IN NO EVENT SHALL Aemon Cannon BE LIABLE FOR ANY
" DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
" (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
" LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
" ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
" (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
" SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

if !exists('g:envim') | let g:envim = {} | endif

if !has('python')
  echo("Error: python vim extension is required.")
  finish
endif

if !vam#IsPluginInstalled('ensime')
  echo("Error: ensime is not installed.")
  finish
endif

if !vam#IsPluginInstalled('ensime-common')
  echo("Error: ensime-common is not installed.")
  finish
endif

let g:envim['path-ensime'] = get(g:envim, 'path-ensime', vam#DefaultPluginDirFromName('ensime'))
let g:envim['path-ensime-common'] = get(g:envim, 'path-ensime-common', vam#DefaultPluginDirFromName('ensime-common'))
let g:envim['path-envim'] = get(g:envim, 'path-envim', expand('<sfile>:h:h'))

python << endpython
import os
import vim
import sys
import logging

# retrieve paths on the python side of the force
ensimePath = vim.eval("g:envim['path-ensime']")
envimPythonPath = vim.eval("g:envim['path-ensime-common']") + '/src/main/python'
vimPythonPath = vim.eval("g:envim['path-envim']") + '/python'

# import ensime-common and envim python modules
sys.path.append(envimPythonPath)
sys.path.append(vimPythonPath)

from Helper import *
from VimHelpers import *
from Envim import *

# search for the last ensime distribution
filesList = os.listdir(ensimePath)
lastDist = findLastDist(filesList)
if lastDist == None:
  echoe("Unable to find ensime dist directory in "+ensimePath+" (did you compile it?)")
  # TODO: does not work 'cause not in sourced file: find a proper way to finish here
  vim.command("finish")

# tell vim where is ensime/dist
ensimeDistPath = ensimePath + os.path.sep + lastDist
vim.command("let g:envim['path-ensime-dist'] = get(g:envim, 'path-ensime-dist', '"+ensimeDistPath+"')")

# setup logger
initLog('ensime-common', 'envim.log')
initLog('envim', 'envim.log')

# not ready to send anything to ensime yet
SwankProcessor().setSendFunction(None)
endpython

" start ensime server thanks to async exec - log to porcelaine
fun! envim#StartServer()

  if has_key(g:envim, 'serverCtx')
    echoe("Ensime server already started")
    return
  endif

  if !has_key(g:envim, 'portfile')
    let g:envim.portfile = tempname()
  endif

  let cmd = 'cd '.g:envim['path-ensime-dist'].' && ./bin/server '.shellescape(g:envim.portfile)
  let ctx = {'cmd': cmd, 'move_last':1, 'line_prefix': 'server  : '}

  call async_porcelaine#LogToBuffer(ctx)

  fun! ctx.gotPort(data)
    call envim#StartSwankClient()
  endf

  let regex_port = 'Server listening on \(\d\+\)\.\.'
  call ctx.dataTillRegexMatchesLine(regex_port, ctx.gotPort)

  fun! ctx.gotConnection(data)
    call envim#connectionAndProjectInit()
  endf

  let regex_conn = 'Got connection, creating handler'
  call ctx.dataTillRegexMatchesLine(regex_conn, ctx.gotConnection)

  let g:envim.serverCtx = ctx
endfun

" start swank client thanks to async exec
fun! envim#StartSwankClient()

  if has_key(g:envim, 'swankClientCtx')
    echoe("Ensime swank client already started")
    return
  endif

  if !has_key(g:envim, 'serverCtx')
    Decho("envim#StartSwankClient: start ensime server first")
    return
  endif

  let cmd = g:envim['path-ensime-common'].'/bin/EnsimeClient.py -r -f '.shellescape(g:envim.portfile)
  let ctx = async#Exec({'cmd':cmd})
  let g:envim.swankClientCtx = ctx

  fun! ctx.receive(data, ...)
    python SwankProcessor().process(vim.eval('a:data'))
  endfun

  python SwankProcessor().setSendFunction(writeToEnsimeClient)

  call feedkeys('envim#Go()')
endfun

" get server connection info and initialize current project
fun! envim#connectionAndProjectInit()
  " vi doesn't want to execute a call right after setSendFunction() - ?
  py envimConnectionAndProjectInit()
endfun

fun! envim#ShutdownServer()
  py envimShutdownServer()
endfun

fun! envim#TypecheckFile()
  py envimTypecheckFile()
endfun

fun! envim#TypecheckAll()
  py envimTypecheckAll()
endfun

fun! envim#SymbolAtPoint()
  py envimSymbolAtPoint()
endfun

fun! envim#UsesOfSymbolAtPoint()
  py envimUsesOfSymbolAtPoint()
endfun

