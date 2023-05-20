# Setting up the tools

Since we use a lot of python tools in this course, there are some things which you'd need to install. In short:

1. You'd need to either have a Linux machine, a Mac, or a Windows machine with the Windows Subsystem for Linux (WSL) installed.
2. You'd need a Code Editor. The recommended code editor is VSCode, which you can set up [here](/pages/vscode.md).
3. You'd need Miniconda. Some of the tools are available through pip, while some are only available through Conda. Miniconda is a nice way to manage all these tools in a single place.
4. You'd need KLayout. This is a layout viewer, which we'll use to view the layouts we create.

## Install WSL
If you are using Windows, you'd have to install WSL. To install:

1. Open Command Prompt as Administrator
2. Type `wsl --install` and press Enter
3. Restart your computer
4. Click on the Start menu and type "Ubuntu" and press Enter
5. Set up your username and password

## Install VSCode
You now need to install VSCode. Refer to the chapter on VSCode [here](/pages/vscode.md), which explains what VSCode is and how to install it.

Open VSCode. You can setup a theme and other things. If you are using WSL, make sure to [open VSCode in your WSL environment](https://code.visualstudio.com/docs/remote/wsl#_open-a-remote-folder-or-workspace). You can check this by checking the green box in the bottom left-hand corner. If VSCode is connected to WSL it will say "WSL" in this box. If it doesn't then click the green box. A menu will pop up. Click the option "Connect to WSL" and VSCode will now be connected to WSL.

## Setup Script
To install Miniconda and KLayouts we have created a setup script you can download [here](../scripts/setup.sh). If you want to install these manual, skip this step by going to the [next page](/pages/git_and_github).

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

It's normal for this to take a long time to install.

To start using the tools, run this command:

```{code-block} bash
conda activate photonics
```
If everything installed correctly you are ready to move onto the [next section](/pages/what_is_a_photonic_device).

The following pages in this section would explain how to use the tools. They also include instructions on how to install the tools individually, if you don't want to use Miniconda.  