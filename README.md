# ENVIM

the ENSIME plugin for Vim

## Introduction

This plugin provides ensime integration for the magnificient Vim editor.

Here is a quick introduction which will be enhanced in the near future.

It rely on several other plugins and patch in order to work:

0) [ensime](https://github.com/aemoncannon/ensime)

Thanks to Aemon Cannon for this amazing gift to the scala community.

1) [Vim async patch](https://github.com/jlc/vim)

Bart Trojanowski is the original author. Few fixes have been applied in order to make it work.
Also, it has been upgraded to the version 7.3.401.

2) [ensime-common](https://github.com/jlc/ensime-common)

Provide Swank parsing/handling functionalities which can be embedded in any Python aware editor.

3) [vim-addon-async](https://github.com/MarcWeber/vim-addon-async)

Nice layer on top of Vim-async.

## Getting Started

### Build vim-async

Clone, build and symbolic-link somewhere so it's easy to start.

Clone the almost-up-to-date patched vim:

    git clone git://github.com/jlc/vim
    cd vim

Configure Vim:
We do not need to install it, but we need that Vim can find all your standard installation files, therefore we set --prefix.

Configure (MacOSX with macport):

    ./configure --enable-pythoninterp --enable-rubyinterp --enable-async --enable-multibyte --with-python-config-dir=/Users/jeanluc/macport/bin/python2.7 --prefix=/Users/jeanluc/macport
 
Configure (Linux Ubuntu):

    ./configure --enable-pythoninterp --enable-rubyinterp --enable-async --enable-multibyte --with-python-config-dir=/usr/lib/python2.7/config --prefix=/usr

Build:

    make

Symlink to somewhere listed in your $PATH, e.g.:

    ln -s src/vim ~/bin/vim-async

### Install vim-addon-manager

And configure it so it use envim, ensime, ensime-common, vim-addon-async (and optionaly vim-scala-behaghel).

It will then download and install all these addons. If you do not know vim-addon-manager, I would highly suggest it!

    fun SetupVAM()

      ...

      let g:vim_addon_manager = {}
      let g:vim_addon_manager.plugin_sources = {}
      let g:vim_addon_manager.plugin_sources['envim'] = {"type": "git", "url": "git://github.com/jlc/envim.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['ensime'] = {"type": "git", "url": "git://github.com/aemoncannon/ensime.git", "branch" : "scala-2.9"}
      let g:vim_addon_manager.plugin_sources['ensime-common'] = {"type": "git", "url": "git://github.com/jlc/ensime-common.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['vim-addon-async'] = {"type": "git", "url": "git://github.com/jlc/vim-addon-async.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['vim-scala-behaghel'] = {'type': 'git', 'url': 'git://github.com/behaghel/vim-scala.git'}
      
      let plugins = [
        \ 'tlib', 'tmru', 'Decho', 'gnupg3645',
        \ 'fugitive', 'gitv', 'Command-T',
        \ 'vim-addon-mw-utils',
        \ 'vim-addon-signs', 'vim-addon-async', 'vim-addon-completion',
        \ 'vim-addon-json-encoding', 'vim-scala-behaghel',
        \ 'envim', 'ensime', 'ensime-common', 
        \ ]

      call vam#ActivateAddons(plugins,{'auto_install' : 0})

      ...

    endf
    call SetupVAM()

### Build ensime

You will need the latest sbt.
Got into ensime which should be in your vim addons directory (e.g. ~/.vim/addons/ensime)

    sbt stage

In case it failed because of lack of memory, re-start it.

### Start envim :)

Started the patched vim:

    vim-async

Start Envim:

    :Envim

This should split the window and let you see how the server is talkative :)
If so, you got it all right!


## Implemented commands and shortcuts

### Typecheck file

Command:

    :EnvimTypecheckFile

Default shortcut:

    <leader>ef

### Typecheck all

Command:

    :EnvimTypecheckAll

Default shortcut:

    <leader>ea

### Symbol at point

Command:

    :EnvimSymbolAtPoint

Default shortcut:

    <leader>ei

### Uses of symbol at point

Command:

    :EnvimUsesOfSymbolAtPoint

Default shortcut:

    <leader>eo

### Completion

Everything is here, it will be the next one implemented! Few more days to wait! :)


## Thanks

Marc Weber for his initial work on ensime-vim, I got a lot of inspiration from it, thanks!

Bart Trojanowski for his initial work on vim-async.
I am not sure this is the best way to go, but at least, for now, it just works nicely!

Hubert Behaghel for his highly appreciated advises and support!
