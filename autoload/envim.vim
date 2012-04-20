" envim.vim
"
" Copyright 2012 Jeanluc Chasseriau <jeanluc@lo.cx>
" 
" Licensed under the Apache License, Version 2.0 (the "License");
" you may not use this file except in compliance with the License.
" You may obtain a copy of the License at
" 
" http://www.apache.org/licenses/LICENSE-2.0
" 
" Unless required by applicable law or agreed to in writing, software
" distributed under the License is distributed on an "AS IS" BASIS,
" WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
" See the License for the specific language governing permissions and
" limitations under the License.

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

let g:envim['started'] = get(g:envim, 'started', 0)
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
from EnvimOutputs import *

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

def elog(): return logging.getLogger('envim')

# not ready to send anything to ensime yet
SwankProcessor().setSendFunction(None)
endpython

" start ensime server thanks to async exec - log to porcelaine
fun! envim#StartServer()

  "redir >> ./envim_command_output.log

  if g:envim.started == 1
    echoe("Ensime server already started")
    return
  endif

  py if getEnsimeConfigFile() == None: vim.command("return")

  py initLog('ensime-common', 'envim.log')
  py initLog('envim', 'envim.log')

  if !exists('*async_exec') || has('gui_running')
    if !vam#IsPluginInstalled('vim-async-beans')
      echoe("Error: vim-async-beans is not installed.")
      finish
    endif
    if !g:abeans['connected']
      call abeans#start()
      sleep 1
    endif
  endif

  if !has_key(g:envim, 'portfile')
    let g:envim.portfile = tempname()
  endif

  let cmd = 'cd '.g:envim['path-ensime-dist'].' && ./bin/server '.shellescape(g:envim.portfile)
  let ctx = {'cmd': cmd}

  py PreviewOutput().setupBuffer()

  py ServerOutput().setupBuffer()

  py ServerOutput().addFilter('^Server listening on.*$', lambda(l): vim.command('call envim#StartSwankClient()'), True)
  py ServerOutput().addFilter('^Got connection, creating handler.*$', lambda(l): Envim().connectionAndProjectInit(), True)

  fun! ctx.receive(data)
    python ServerOutput().onServerOutput(vim.eval('a:data'))
  endfun

  let ctx = async#Exec(ctx)

  let g:envim.serverCtx = ctx

  let g:envim.started = 1
  " py ServerOutput().showServerOutput()
endfun

" start swank client thanks to async exec
fun! envim#StartSwankClient()

  if has_key(g:envim, 'ensimeClientCtx')
    echoe("Ensime swank client already started")
    return
  endif

  if !has_key(g:envim, 'serverCtx')
    Decho("envim#StartSwankClient: start ensime server first")
    return
  endif

  let cmd = g:envim['path-ensime-common'].'/bin/EnsimeClient.py -r -f '.shellescape(g:envim.portfile)
  let ctx = async#Exec({'cmd':cmd})
  let g:envim.ensimeClientCtx = ctx

  fun! ctx.receive(data, ...)
    python SwankProcessor().process(vim.eval('a:data'))
  endfun

  python SwankProcessor().setSendFunction(Envim().sendToEnsimeClient)

  call feedkeys('envim#Go()')
endfun

" get server connection info and initialize current project
fun! envim#connectionAndProjectInit()
  " vi doesn't want to execute a call right after setSendFunction() - ?
  py Envim().connectionAndProjectInit()
endfun

fun! envim#ShutdownServer()
  if g:envim.started == 0 | return | endif
  py Envim().shutdownServer()
endfun

fun! envim#TypecheckFile()
  py Envim().typecheckFile()
endfun

fun! envim#TypecheckAll()
  py Envim().typecheckAll()
endfun

fun! envim#SymbolAtPoint()
  py Envim().symbolAtPoint()
endfun

fun! envim#UsesOfSymbolAtPoint()
  py Envim().usesOfSymbolAtPoint()
endfun

fun! envim#logEvent(event)
  py elog().debug("envim#logEvent: %s", vim.eval("a:event"))
endfun

fun! envim#Completions(findstart, base)
  if g:envim.started == 0 | return | endif
  if !pumvisible()
    py elog().debug("envim#Completion")
    py Envim().completions(int(vim.eval("a:findstart")), vim.eval("a:base"))
  endif
  return completion_result
endfun

fun! envim#detectEndCompletions()
  if g:envim.started == 0 | return | endif
  if pumvisible() == 0
    if has_key(g:envim, 'showCompletions')
      py elog().debug("envim#detectEndCompletions")
      unlet g:envim.showCompletions
      call abeans#continueMessages()
      pclose
    endif
  endif
endfun

fun! envim#onCursorMoved()
  if g:envim.started == 0 | return | endif
  py Envim().onCursorMoved()
endfun

fun! envim#onQuickFixLeave()
  if g:envim.started == 0 | return | endif
  py Envim().onQuickFixLeave()
endfun

fun! envim#onWinLeave()
  if g:envim.started == 0 | return | endif
  py Envim().onWinLeave()
endfun

fun! envim#onTabLeave()
  if g:envim.started == 0 | return | endif
  py Envim().onTabLeave()
endfun
