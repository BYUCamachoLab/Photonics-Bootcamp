# Photonics Bootcamp

The CamachoLab Photonics Bootcamp, with support from Google. 

This book can be viewed [online](https://byucamacholab.github.io/Photonics-Bootcamp/).

## Installation

If you wish to create a virtual Python environment for your book (recommended),
you can do so:

conda:
```
conda create --name bootcamp python
conda activate bootcamp
```

virtualenv:
```
python3 -m venv bootcamp
source bootcamp/bin/activate
```

Then, install the required packages:

```
pip install --upgrade -r requirements.txt
```

## Building the book

You can simply run from the toplevel directory

```
jb build book
```

The output will be located in book/_build/html. To serve it in your browser,
navigate to that directory and start a simple Python server:

```
python -m http.server
```

## Development

The majority of this book is written as Jupyter notebooks. Learn more about 
creating beautiful websites online at https://jupyterbook.org/en/stable/intro.html.

When writing notebooks, if including images, it is best to reference a web
address instead of a relative file in the repository. This way, when the
notebook is downloaded independently, the links and images will not be broken.

JupyterBook by default runs all the notebooks within the repository when
generating the site. Because many of the notebooks contain lengthy simulations
that we don't want to run on the deployment server, this behavior has been 
turned off. Therefore, when pushing new notebooks to the repository, you should
have already run the notebooks from top to bottom in a fresh kernel to ensure
all the outputs (plots and results) are present.

## Deployment

By default, pushes or pull requests merged on "master" automatically trigger a
build and deploy cycle. 

Note that notebooks are only automatically executed remotely if there are any
missing outputs for any cells. If you've run the notebooks locally when you've
committed them, they will appear on the site as they are saved without 
rerunning.

## Contributors

We welcome and recognize all contributions. You can see a list of current
contributors in the 
[contributors tab](https://github.com/BYUCamachoLab/photonics_bootcamp/graphs/contributors).
