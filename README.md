# Photonics Bootcamp

The CamachoLab Photonics Bootcamp, with support from Google.

This book can be viewed [online](https://byucamacholab.github.io/Photonics-Bootcamp/).
Students setting up for the first time should follow [START_HERE.md](START_HERE.md).

## Installation

Python 3.12 is recommended. Create a virtual environment, either with conda
(needed if you want to run the Meep simulation notebooks, see below):

```Shell
conda create --name bootcamp python=3.12
conda activate bootcamp
```

or with venv (the `bootcamp/` folder is gitignored):

```Shell
python3 -m venv bootcamp
source bootcamp/bin/activate
```

Then, install the required packages:

```Shell
pip install --upgrade -r requirements.txt
```

### Meep (simulation notebooks only)

The FDTD simulation notebooks (for example *Scattering Parameters*, *Y-Branch*,
*Directional Couplers*, *MMIs*, *Ring Resonators*, *Grating Couplers*) use
[Meep](https://meep.readthedocs.io/), which is not available from pip. Install
it from conda-forge into your conda environment (Linux, macOS, or WSL on
Windows):

```Shell
conda install -c conda-forge pymeep
```

Everything else, including building the book, works without Meep.

## Building and previewing the book

The book uses [Jupyter Book 2](https://jupyterbook.org) (built on MyST). Its
configuration and table of contents live in `book/myst.yml`, so run the
commands from inside the `book/` folder:

```Shell
cd book
jupyter book start          # live preview at http://localhost:3000
jupyter book build --html   # static site written to book/_build/html
```

Jupyter Book 2 needs [Node.js](https://nodejs.org) 18 or newer; if it is
missing, `jupyter book` will offer to install it for you the first time.

From the top-level folder you can also use `make serve` (live preview) or
`make book` (static build).

> **Note:** don't run `jupyter book` from the top-level folder. With no
> `myst.yml` there, it starts the wizard for creating a *new* book.

## Development

The majority of this book is written as Jupyter notebooks. To add a page,
create the file under `book/pages/` and add it to the `toc` section of
`book/myst.yml`. Learn more at https://jupyterbook.org.

When writing notebooks, if including images, it is best to reference a web
address instead of a relative file in the repository. This way, when the
notebook is downloaded independently, the links and images will not be broken.

Notebooks are **not** executed when the book is built, because many of them
contain lengthy simulations. When pushing new notebooks to the repository, you
should have already run the notebooks from top to bottom in a fresh kernel to
ensure all the outputs (plots and results) are present.

## Deployment

Pushes or pull requests merged on `main` automatically build the book and
deploy it to GitHub Pages (see `.github/workflows/pages.yml`). The site shows
the notebook outputs exactly as they were saved in the repository.

## Contributors

We welcome and recognize all contributions. You can see a list of current
contributors in the [contributors tab](https://github.com/BYUCamachoLab/Photonics-Bootcamp/graphs/contributors).
