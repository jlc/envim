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

