# Python

Python is a high-level programming language that has been embraced by the
scientific community. There's a host of freely-available scientific packages,
including [numpy](https://numpy.org/), [scipy](https://www.scipy.org/), and
[matplotlib](https://matplotlib.org/).

Python is also an excellent language for learning how to program. It avoids
some of the more complex features of other languages, such as pointers, and
provides a simple syntax that is easy to read and write. It is also an
interpreted language, which means that you can write and run code in the same
session without needing to recompile. This makes it easy to prototype, rapidly
test out new ideas, and debug your code.

## Conda

We recommend installing Python via
[miniconda](https://docs.conda.io/en/latest/miniconda.html). This bundled
distribution makes installation on any platform simple (even on Windows, though
we'll be using WSL). Miniconda is a no-frills, stripped-down version of the 
[Anaconda distribution](https://www.anaconda.com/products/distribution), which
is a popular Python distribution that includes a host of scientific packages.
We don't necessarily need all of these packages, and it tends to be a pretty
large install, so we'll use miniconda instead.

Use the [latest installer
links](https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links)
to download the appropriate installer for your operating system. For MacOS and
Linux, they are simple bash scripts that you'll need to execute after
downloading. 

:::{note} 

For Windows, it's easiest to download the script in the Ubuntu terminal using
curl so you don't have to copy it from the Windows filesystem over to the
Ubuntu. Even though you're on Windows, since you're installing it to the Ubuntu
system, download the Linux installer! 
:::

## Package Managers

Python has a robust open-source community. To that end, there exist several
free tools for hosting packages so others can install them easily. The most
well-known and well-established of these is the [Python Package
Index](https://pypi.org/) (PyPI). Any one is free to host Python packages there,
as long as the name of your package hasn't been used by anyone else before!
This is where we will install most of the packages we use from. Some prominent
ones you will become very familiar with include:

* NumPy: the fundamental package for scientific computing with Python. Think of
    it as the Python counterpart to MATLAB.
* SciPy: fundamental algorithms for scientific computing in Python. This includes
    thinks like signal processing, optimization, etc.
* Matplotlib: the defacto Python plotting package. It provides an interface
    that will be very familiar to MATLAB users.
* gdsfactory: A Python library for generating GDS layouts.

It's very easy to install packages from PyPI. Most base installations of Python
include "pip", a tool used to install other packages from PyPI. It can be
invoked from the command line, like so:

```bash
pip install numpy
```

It can be used to upgrade packages, too (including itself):

```bash
pip install --upgrade pip
```

You can also stack package names to save some typing:

```bash
pip install numpy scipy matplotlib
```

## Package Versioning

Modern packages aren't just released to the world once; instead, they are often
released incrementally, with new features and changes that break previous 
application programming interfaces (API's).

API's are basically contracts that a software provides to a user. "If you call
this function, provide these values, I will give you this answer or perform a
specific task." Sometimes, as programs evolve, new ways of accomplishing tasks
are introduced into the program and it becomes necessary to change or remove
old functions. In the open-source world, especially with relatively immature
packages, it's common for API's to change frequently. Therefore, if you want
to guarantee your code will continue to work in the future or on someone else's
machine, it's important that you track the version of the software you're
using. This way you ensure you have a **reproducible environment**.

There's a concept out there called [**semantic
versioning**](https://semver.org/). This simply means that the version numbers
tell you something about its compatibility with other programs. The general
rule is as follows:

> Given a version number MAJOR.MINOR.PATCH, increment the:
> 
> 1. MAJOR version when you make incompatible API changes
> 2. MINOR version when you add functionality in a backward compatible manner
> 3. PATCH version when you make backward compatible bug fixes

For example, you're using version **3.4.2** of a package. They have now
released version **4.0.0**. It's likely that your code won't immediately work
with the new release without some amount of refactoring. PyPI always keeps 
old releases of packages around, though, so if you're passing your code on to
someone else, they'll still be able to install the specific version you used
to write the code.

In Python, when you're working on a software, or writing code that depends on
other software, it's best practice to include some list of dependencies and 
their versions. This is most commonly done with a **requirements.txt** file, 
which is a text file that simply contains package versions and a fixed
version number. An example ``requirements.txt`` file might look like this:

```
numpy==1.24.3
scipy==1.10.1
matplotlib==3.7.1
```

The full list of packages in the file can be installed easily from the command
line:

```bash
pip install -r requirements.txt
```

## Virtual Environments

It's best practice to use a **virtual environment**. A virtual environment is
simply an environment that is isolated from your main Python installation 
or any other installation on your computer. You can think of it as a sandbox;
you can have as many of them as you want, and they don't interact with each 
other. They're especially useful if you need to have different versions of 
the a library for different programs.
They can both be on your computer, but in their own walled off areas.

In Python, virtual environments are also very easy to create and destroy.
This way, if you mess up your environment, it only costs you a few seconds to
delete it and start again. The nice thing about a requirements file that pins
versions of the software is that once you've verified all the versions work
well together, you never have to worry about compatability or recreating the
setup you were originally using again. Simply install your requirements file,
or give it to someone else, and you can create the same environment anywhere
you want.

While Python has a virtual environment mechanism built in to the language 
([venv](https://docs.python.org/3/library/venv.html)), since we're using 
conda to access Python, we'll use its virtual environment management features
as well.

To create an environment, in this case named ``photonics``, run:

```bash
conda create --name photonics python
```

You can even specify a specific version of Python, if you'd like to use the
latest and greatest version:

```bash
conda create --name photonics python=3.11
```
