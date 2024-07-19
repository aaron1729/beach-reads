# beach-reads

## overview

this repo contains the code behind [this webpage](https://etale.site/beach-reads/). `main.py` enables an AI chatbot to "think" before writing a ~1000-word "beach read" vignette. it contains the prompts that are fed to the chatbot, which are essentially human-readable.

## notes

to create a conda environment, do `conda create --name beach-reads python=3.11`. (it seems that python <3.12 may be needed to work with langchain?). activate it with `conda activate beach-reads`, and deactivate it with `conda deactivate`. install packages/modules via `conda install -c conda-forge PACKAGE_NAME` when possible, and use `pip install PACKAGE_NAME` if it doesn't exist in `conda-forge`.

## to-do

* fit txt encoding (displays with a few issues in browser)
* add chatGPT (or even langchain)