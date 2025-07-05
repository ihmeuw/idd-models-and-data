#!/bin/bash
# Install R kernel for Jupyter
R -e "IRkernel::installspec(user = FALSE)"

# Install Python package in development mode
pip install -e .

# Create Python kernel
python -m ipykernel install --user --name idd-mad --display-name "IDD MAD (Python 3.12)"