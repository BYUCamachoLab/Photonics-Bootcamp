#!/bin/bash

# tput setaf 2

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh ./Miniconda3-latest-Linux-x86_64.sh -b
eval "$(~/miniconda3/bin/conda shell.bash hook)"
conda init
conda create --name photonics python=3.10 -y
conda activate photonics
pip install gdsfactory[full,gmsh,tidy3d,devsim,meow,sax,database,femwell,ray]
gf install klayout-integration
pip install jaxlib
conda install -c conda-forge pymeep=*=mpi_mpich_* nlopt -y
conda install -c conda-forge slepc4py=*=complex* -y
pip install simphony sipann
wget https://www.klayout.org/downloads/Ubuntu-22/klayout_0.28.7-1_amd64.deb
sudo dpkg -i klayout_0.28.7-1_amd64.deb
