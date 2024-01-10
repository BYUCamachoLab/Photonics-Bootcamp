# Setting up the tools

Since we primarily use Python tools in this course, there are some things 
you'll need to install. In short, you'll need:

1. A Linux machine, a Mac, or a Windows machine with the 
    [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/about) 
    installed.
2. A code editor. The recommended code editor is 
    [Visual Studio Code](https://code.visualstudio.com/), (installation 
    instructions [here](/pages/vscode.md)).
3. Miniconda. Most of the tools are installable through the 
    [Python Package Index (PyPI)](https://pypi.org/), i.e. "pip" installable, 
    while some precompiled packages are only available through Conda 
    repositories. Miniconda, which also provides a Python installation and 
    virtual environments by default, is a nice way to manage all these tools 
    in a single place.
4. KLayout, a layout/GDS file viewer, which we'll use to view the circuits we 
    create.

## Install WSL

If you are using Windows, you'll need to install {term}`WSL``. This can be 
easily installed through the Windows store (recommended), or via the command 
line:

1. Open Command Prompt as Administrator.
2. Run the command ``wsl --install``.
3. Restart your computer.
4. From the Start menu, run Ubuntu.
5. On the first run, set up a new user account on the Linux machinen (username 
    and password, which can be different from your Windows machine).

## Install VSCode
You now need to install VSCode. Refer to the chapter on VSCode [here](/pages/vscode.md), which explains what VSCode is and how to install it.

Open VSCode. You can setup a theme and other things. If you are using WSL, make sure to [open VSCode in your WSL environment](https://code.visualstudio.com/docs/remote/wsl#_open-a-remote-folder-or-workspace). You can check this by checking the green box in the bottom left-hand corner. If VSCode is connected to WSL it will say "WSL" in this box. If it doesn't then click the green box. A menu will pop up. Click the option "Connect to WSL" and VSCode will now be connected to WSL.

<!-- ## Setup Script
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
If everything installed correctly you are ready to move onto the [next chapter](/pages/what_is_a_photonic_device).

The following pages in this section would explain how to use the tools. They also include instructions on how to install the tools individually, if you don't want to use Miniconda.   -->