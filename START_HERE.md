# Start Here (Students)

## Day 1: Get running quickly (recommended)

If you are on Windows, do all of these steps inside
[WSL (Ubuntu)](https://learn.microsoft.com/en-us/windows/wsl/install).

#### 1. Clone the course repository

```Shell
git clone https://github.com/BYUCamachoLab/Photonics-Bootcamp.git
cd Photonics-Bootcamp
```

#### 2. Create a virtual environment with conda or venv

conda (recommended, because the simulation notebooks need Meep, which only
installs through conda)

```Shell
conda create -n bootcamp python=3.12
conda activate bootcamp
```

venv

```Shell
python3 -m venv bootcamp
source bootcamp/bin/activate
```

#### 3. Install the required packages

```Shell
pip install --upgrade -r requirements.txt
```

If you are using conda and want to run the Meep simulation notebooks, also run:

```Shell
conda install -c conda-forge pymeep
```

#### 4. Open the notebooks

The course notebooks are in `book/pages/`. Open them in VS Code (select the
`bootcamp` environment as the kernel) or with Jupyter:

```Shell
jupyter lab book/pages
```

#### 5. (Optional) Preview the course website locally

```Shell
cd book
jupyter book start
```

Then open the `http://localhost:3000` link it prints. The first run may ask to
install Node.js; answer yes. Press `Ctrl+C` to stop the preview.
