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

We recommend installing Python via
[miniconda](https://docs.conda.io/en/latest/miniconda.html). This bundled
distribution makes installation on any platform simple (even on Windows, though
we'll be using WSL). Miniconda is a no-frills, stripped-down version of the 
[Anaconda distribution](https://www.anaconda.com/products/distribution), which
is a popular Python distribution that includes a host of scientific packages.
We don't necessarily need all of these packages, and it tends to be a pretty
large install, so we'll use miniconda instead.

Use the [latest installer links]() to download the appropriate installer for
your operating system. For MacOS and Linux, they are simple bash scripts that
you'll need to execute after downloading. For Windows, it's easiest to 
downlaod the script in the Ubuntu terminal using curl so you don't have to
copy it from the Windows filesystem over to the Ubuntu one:

```{code-block} bash
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```
