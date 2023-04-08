# Git (and GitHub)

In programming, it is desirable to be able to track changes to your code over
time. In development environments, it's not uncommon that changes may need to
be rolled back if they break something in production code. Version control
systems (VCS) are also extremely helpful in collaborative environments, as they
track who changed what and allow for simultaneous edits to be merged together
rather painlessly. 

Git is the predominant VCS used by programmers today. While git is a command-
line tool, an entire ecosystem of hosting services, GUI tools, and IDE's have
sprung up around it. 

To [install git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) on your machine:

::::{tab-set}

:::{tab-item} Windows
:sync: windows

While you can install [Git for Windows](https://gitforwindows.org/), because
the other software packages used in this course are Mac- or Linux-only, you
will be forced to use WSL to complete this course on Windows. Still, we'll
provide a [download link](https://git-scm.com/download/win) for git on Windows.

:::

:::{tab-item} MacOS
:sync: macos

Git is included with XCode Command Line Tools. These can be installed from the
terminal with the command:

```{code-block} bash
xcode-select --install
```

You can test the installation by running:

```{code-block} bash
git --version
```

:::

:::{tab-item} Linux
:sync: linux

If git is not installed on your machine, you can install it through the terminal.

Debian-based distributions (e.g. Ubuntu, Debian):

```{code-block} bash
sudo apt install git-all
```

RPM-based distributions (e.g. Fedora, RHEL, CentOS):

```{code-block} bash
sudo dnf install git-all
```

:::

::::

GitHub is the most well known hosting service, and it provides free accounts
(and free private repositories) to all users. This bootcamp, for example, is
hosted on GitHub, along with many of the most popular open-source Python
projects (including numpy, scipy, and matplotlib). If you want to version
control your code, we recommend creating an account on GitHub and keeping your
source code there.
