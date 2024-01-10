# Visual Studio Code

While you can write computer code using any text editor, some text editors have
special features that make writing code easier.  In this course, we will be
using [Visual Studio Code](https://code.visualstudio.com) (also known as
{term}`vscode`), a popular open-source text editor by Microsoft that is desiged
specifically for writing code. It boasts a healthy set of extensions that 
can provide integrated development environment (IDE)-like capabilities in a 
much lighter program.

To [install vscode](https://code.visualstudio.com/docs/setup/setup-overview) on
your machine:

::::{tab-set}

:::{tab-item} Windows
:sync: windows

Download the installer [here](https://code.visualstudio.com/Download).

Detailed installation instructions can be found
[here](https://code.visualstudio.com/docs/setup/windows).

:::

:::{tab-item} MacOS
:sync: macos

Download the installer [here](https://code.visualstudio.com/Download).

Detailed installation instructions can be found
[here](https://code.visualstudio.com/docs/setup/mac).

:::

:::{tab-item} Linux
:sync: linux

Download the installer [here](https://code.visualstudio.com/Download).

Detailed installation instructions can be found
[here](https://code.visualstudio.com/docs/setup/linux).

:::

::::

## Configure vscode

There are several useful extensions in vs code. Here are some recommendations
for this course:

* [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
    * [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) (included with Python extension)
    * [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter) (included with Python extension)
* [WSL](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl) (if you're on a Windows machine)
* [Open](https://marketplace.visualstudio.com/items?itemName=sandcastle.vscode-open) (allows you to open files from the code editor tree in their default program)
* [vscode-icons](https://marketplace.visualstudio.com/items?itemName=vscode-icons-team.vscode-icons) (some eye-candy, makes it easier to find files in the tree)

## Connect to WSL (Windows Machines)

1. Open VSCode. You can setup a theme and other things. 
1. Connect to WSL. There are a few ways to do this, but the easiest is to look
   for a small colored box in the bottom left-hand corner of VSCode. If VSCode
   is connected to WSL it will say "WSL" in this box. If it doesn't, then click
   the box. A menu will pop up. Click the option "Connect to WSL" and VSCode
   will now be connected to WSL. More information about WSL in VSCode and other
   ways to connect can be found in [VSCode's WSL docs](https://code.visualstudio.com/docs/remote/wsl#_open-a-remote-folder-or-workspace). 
1. From now on, all coding and installing should be done through WSL using the
   VSCode terminal, and since WSL is a linux system, the linux install
   instructions should be used.