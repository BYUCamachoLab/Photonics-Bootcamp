# Setting up the tools

Since we use a lot of python tools in this course, there are some things which you'd need to install. In short:

1. You'd need to either have a Linux machine, a Mac, or a Windows machine with the Windows Subsystem for Linux (WSL) installed.
2. You'd need a Code Editor. The recommended code editor is VSCode, which you can download [here](https://code.visualstudio.com/download).
3. You'd need Miniconda. Some of the tools are available through pip, while some are only available through Conda. Miniconda is a nice way to manage all these tools in a single place.
4. You'd need KLayout. This is a layout viewer, which we'll use to view the layouts we create. You can download it [here](https://www.klayout.de/build.html).

If you are using Windows, you'd have to install WSL. To install:

1. Open Command Prompt as Administrator
2. Type `wsl --install` and press Enter
3. Restart your computer
4. Click on the Start menu and type "Ubuntu" and press Enter
5. Set up your username and password

You now need to install VSCode. Refer to the chapter on VSCode [here](/pages/vscode.md), which explains what VSCode is and how to install it.

Open VSCode. You can setup a theme and other things. Open a new Terminal. If you are using WSL, make sure to open the WS terminal. You can do this by clicking on the dropdown menu on the top right of the terminal and selecting "Select Default Profile". Select "Ubuntu" from the list.

To install all the packages, download this [setup script](../scripts/setup.sh).

If you are using Linux, and assuming the script was downloaded to your Downloads folder, run the following command:

```{code-block} bash
sh ~/Downloads/setup.sh
```

If you are using WSL, get the file path of the script by opening the file explorer, right clicking on the file, and selecting "Properties". Copy the "Location" field. Then, in the terminal, run the following command:

```{code-block} bash
wslpath <path to setup script> | sh
```

```{note}
This script assumes you are using Ubuntu 22.04, which is the default WSL version. If you are using a different version, you'd have to edit the line of the script which downloads KLayout. Alternatively, if you are using a different version of Linux, you can install KLayout manually from the [downloads page](https://www.klayout.de/build.html).
```

This would take a while to install.

To start using the tools, run this command:

```{code-block} bash
conda activate photonics
```

The following pages in this section would explain how to use the tools. They also include instructions on how to install the tools individually, if you don't want to use Miniconda.
