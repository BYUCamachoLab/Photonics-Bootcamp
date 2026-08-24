# WSL (Windows-only)

If you are using Windows, you'll need to install {term}`WSL`. This can be 
easily installed through the Windows store (recommended), or via the command 
line:

1. Open Command Prompt as Administrator.
2. Run the command ``wsl --install``.
3. Restart your computer.
4. From the Start menu, run Ubuntu.
5. On the first run, set up a new user account on the Linux machine (username 
    and password, which can be different from your Windows machine).

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