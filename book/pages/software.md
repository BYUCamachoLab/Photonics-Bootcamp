# Software

In the following sections, we'll describe the various software packages used
in this course and how to configure them on your local machine.

The course can be completed on any modern operating system (OS); we'll provide
setup instructions for Windows, MacOS, and Linux. Some of the open-source
packages we'll describe, however, are only compatible with Mac and Linux.
Therefore, on Windows, you'll have to use Windows Subsystem for Linux ({term}`WSL`) in
order to complete the course. 

Through this setup guide, we're going to be very opinionated about which 
software to install and how to configure your system. This is for the benefit
of the newcomer&mdash;one standard setup that we'll describe and know how to
troubleshoot. If you're experienced enough to disagree with our setup method,
we assume you're also experienced enough to adapt all our instructions to your
own way of doing things. 

:::{note}

For Windows machines, we recommend installing Ubuntu through the Microsoft
Store, which will give you a terminal interface on your local machine (although
we will primarily use Visual Studio Code to interact with it, providing a
GUI-like experience, so you don't need to be too nervous about having to
navigate a terminal). 
:::

Since we primarily use Python tools in this course, here are some things we're
going to install in the next few sections:

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
