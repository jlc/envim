# ENVIM

the ENsime plugin for VIM

## Introduction

This plugin provides ensime integration for the magnificient Vim editor.

Currently, few ensime's features have been integrated:

- File(s) type checking

- Type under cursor

- Use of the symbol under cursor

- Completion


## Important notes

Envim requires vim to be asynchronous aware, which means to be able to receive messages from Ensime in the background.
This is quite a challenge for vim. There are not so many options to achieve this goal.

The one which is used here has been designed with console based vimmers in mind (thus without relying on GVim features), and this is how vim-async-beans is born (cf. "Behind the scene").
It may be quite a good choice while waiting for a native vim async implementation.

However, it require 2 vim buffers in order to communicate with the outside world.
These buffers are a) hidden, and b) readonly and unmodifiable by default.
But, at some point, it is possible that you automatically "jump" on one of them without asking for.

This may be anoying, but also may conflict with some configuration and/or plugins.
In order to better address this issue, I would much appreciate any feedbacks about your experience using Envim.


## Getting started

NOTE: Envim is currently evolving a lot, you should then frequently pull it.

When updating Envim, be careful to update its 2 main dependencies:

- vim-async-beans

and

- ensime-common

### Install vim plugins

#### Dependencies

Required dependencies:
- [ensime](https://github.com/aemoncannon/ensime)

- [envim](https://github.com/jlc/envim)

- [ensime-common](https://github.com/jlc/ensime-common)

- [vim-async-beans](https://github.com/jlc/vim-async-beans)

- [vim-addon-async](https://github.com/jlc/vim-addon-async) forked from [vim-addon-async](https://github.com/MarcWeber/vim-addon-async)

- [vim-addon-signs](https://github.com/MarcWeber/vim-addon-signs) required by vim-addon-async

- [vim-addon-manager](https://github.com/MarcWeber/vim-addon-manager) (this dependency will be removed soon)

#### Manually

In theory, manual installation may be done by loading the required plugins as listed above.
In practice, this simple theory may not be as easy. Any suggestion?

#### Using vim-addon-manager

vim-addon-manager is an amazing plugin manager, check it out here: [vim-addon-manager](https://github.com/MarcWeber/vim-addon-manager).

[Vim-addon-manager getting started](https://github.com/MarcWeber/vim-addon-manager/blob/master/doc/vim-addon-manager-getting-started.txt)

In your .vimrc, add ensime, vim-async-beans, ensime-common and envim plugins as shown below:

    fun SetupVAM()

      ...

      let g:vim_addon_manager = {}
      let g:vim_addon_manager.plugin_sources = {}
      let g:vim_addon_manager.plugin_sources['ensime'] = {"type": "git", "url": "git://github.com/aemoncannon/ensime.git", "branch" : "scala-2.9"}
      let g:vim_addon_manager.plugin_sources['envim'] = {"type": "git", "url": "git://github.com/jlc/envim.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['ensime-common'] = {"type": "git", "url": "git://github.com/jlc/ensime-common.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['vim-async-beans'] = {"type": "git", "url": "git://github.com/jlc/vim-async-beans.git", "branch" : "master"}
      let g:vim_addon_manager.plugin_sources['vim-addon-async'] = {"type": "git", "url": "git://github.com/jlc/vim-addon-async.git", "branch" : "master"}

      let plugins = [
        \ 'ensime',
        \ 'vim-addon-async',
        \ 'vim-async-beans',
        \ 'ensime-common',
        \ 'envim'
        \ ]

      call vam#ActivateAddons(plugins,{'auto_install' : 0})

      ...

    endf
    call SetupVAM()


Optionaly for Scala syntax:

      let g:vim_addon_manager.plugin_sources['vim-scala-behaghel'] = {'type': 'git', 'url': 'git://github.com/behaghel/vim-scala.git'}

      let plugins = [
        ...
        \ 'vim-scala-behaghel',
        ...
        ]

Start vim.

vim-addon-manager will ask you to download and install the missing plugins and their dependencies.


#### Using pathogen

Due to the fact that I still have to learn pathogen, the completion of this section may wait a little while, except if someone would like to help me to do so.


### Git add remote and pull already cloned projects

Take care of your already cloned project (such as vim-addon-async):
- git add remote jlc https://github.com/jlc/<project>
- pull last changes

### Build ensime

Ensime needs to be build using the latest sbt : [xsbt wiki](https://github.com/harrah/xsbt/wiki).

Go into the ensime directory which should be in your vim addons directory (e.g. ~/.vim/addons/ensime), and run:

    sbt stage

In case it failed because of lack of memory, simply re-start it.


### Go into your favorite scala project

Create a .ensime configuration file at the root of your project.

Aemon Cannon has created a sbt plugin to create one for you, check it out: [ensime-sbt-cmd](https://github.com/aemoncannon/ensime-sbt-cmd)

Or, you may simply needs these few lines:

    ;; this work in order to explore ensime sources
    (
    :use-sbt t
    ;; or
    ;; :use-maven t

    :compile-jars (dist/lib)
    :source-roots (src/main/scala)
    )

Please note that my knowledge regarding .ensime configuration file is very limited.

The mastery of this file may be a step in order to avoid surprising results from ensime.


### Start envim :)

Start vim:

    vim

Start Envim:

    :Envim

This should split the window and let you see how the server is talkative :)
If so, you got it all right!

Next, open a Scala source and try '<leader>ef' or '<leader>ea' for typechecking (shown in error list window :copen), or maybe move the curose on a symbol and type '<leader>ei' which should display its type, maybe you would be curious of the completion, simply type Control-x-Control-o after a symbol.


### Important notes

- You may notice 2 buffers called vim-async-beans.out and vim-async-beans.in.
They are created and used by vim-async-beans in order to help vim to communicate with the outside world. Most of the time, they are not modifiable. However, it is advised to simply ignore them and return to your favorite Scala sources.

- This plugin is still fresh out of its eggs. I would much appreciate any feedbacks: jeanluc [at] lo.cx


## Behind the scene

Envim needed asynchronous communications with external processes in order to talk with ensime.
Among several ways to do so, 2 methods have been implemented: vim-async-beans and a patch applied to vim (of course, there may be other ways like vim-addon-async which use the client-server implementation).

As a side note, these methods have been developed in order to provide a satisfying solution to vimmers who prefer the console version as opposed to GUI mode.
However, both methods should equaly works in a GUI mode, but have not been tested at all.


### Asynchronous vim

- Vim async patch : [github.com/jlc/vim](https://github.com/jlc/vim)

A patch initialy developed by [Bart Trojanowski](https://github.com/bartman) has been slightly improved. Vim has also been upgraded to version 7.3.401.

This patch provides the API to a) execute external processes, b) send data to processes, c) receive asynchronous notifications on processes outputs.

It is promising but it requires few improvements to make it reliable (thanks to the study of the NetBeans documentation, I got few ideas in order to do so).

The main disadvantage, until it get integrated, if this ever happen, is that it requires to rebuild vim, which is a burden in order to use Envim.


- Vim-async-beans : [github.com/jlc/vim-async-beans](https://github.com/jlc/vim-async-beans)

In order to avoid rebuilding anything, a new plugin has been developed: vim-async-beans.

It is based on NetBeans support integrated in Vim by default. NetBeans is a protocol enabling communications with external IDE through a TCP stream. Vim-async-beans use this feature to establish communications between vim and external processes like ensime.

It is really fresh and thus experimental, but appears to be a good alternative.


- Vim-addon-async : [github.com/jlc/vim-addon-async](https://github.com/jlc/vim-addon-async)

This is a plugin developed by [Marc Weber](https://github.com/MarcWeber) which enable vim to communicate asynchronously.

It rely on the client-server mode implemented in GVim and an external process (written in C).
It is certainly a reliable solution, but does not work with vim in console mode.

Support of both vim-async-beans and vim async patch have been added in this fork.


### Ensime Swank protocol

The famous Swank protocol which is the favorite communication method used by Ensime to talk to the external world has been implemented in a project called [ensime-common](https://github.com/jlc/ensime-common).

It is used in Envim and may be used in other project to simplify future ensime integration.


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

Default shortcut:

    <C-x><C-o>


## Acknoledgements and thanks

- Aemon Cannon, author of Ensime, thanks for this gift to the Scala community!

- Marc Weber, author of vim-addon-manager, vim-addon-async and many (many) others. More importantly, he is the author of the first vim-ensime integration from which I took a lot of inspiration and knowledge, thanks!

- Bart Trojanowski, original author of vim-async patch.

- Hubert Behaghel, a dear friend and strong supporter of this initiative.


