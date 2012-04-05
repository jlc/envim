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

" start and connect to envim server
command! -nargs=0 Envim call envim#StartServer()
command! -nargs=0 EnvimStop call envim#ShutdownServer()
command! -nargs=0 EnvimTypecheckFile call envim#TypecheckFile()
command! -nargs=0 EnvimTypecheckAll call envim#TypecheckAll()
command! -nargs=0 EnvimSymbolAtPoint call envim#SymbolAtPoint()
command! -nargs=0 EnvimUsesOfSymbolAtPoint call envim#UsesOfSymbolAtPoint()

noremap <leader>ef :EnvimTypecheckFile<cr>
noremap <leader>ea :EnvimTypecheckAll<cr>
noremap <leader>ei :EnvimSymbolAtPoint<cr>
noremap <leader>eo :EnvimUsesOfSymbolAtPoint<cr>

augroup ENVIM
  au!
  autocmd VimLeave call envim#ShutdownServer()
  " autocmd BufWritePost *.scala if !g:envim.prevent_typecheck | call envim#TypecheckFile() | endif
  autocmd BufRead,BufNewFile .ensime  setlocal ft=default.ensime
augroup end

