#!/bin/bash

# tput setaf 2

if [ ! -d "~/miniconda3" ]; then
    echo "Installing Miniconda"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh ./Miniconda3-latest-Linux-x86_64.sh -b
    eval "$(~/miniconda3/bin/conda shell.bash hook)"
    conda init
    conda create -n photonics python=3.11 -y
else
    echo "Miniconda already installed"
fi
conda activate photonics
conda install -c conda-forge pymeep="*=mpi_mpich_*" nlopt -y
conda install -c conda-forge slepc4py="*=complex*" -y
pip install -r requirements.txt
gf install klayout-integration
wget https://www.klayout.org/downloads/Ubuntu-22/klayout_0.28.7-1_amd64.deb
sudo dpkg -i klayout_0.28.7-1_amd64.deb
