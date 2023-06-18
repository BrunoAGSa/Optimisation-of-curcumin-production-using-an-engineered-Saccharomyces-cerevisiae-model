# Optimization of Curcumin Production in Engineered *Saccharomyces cerevisiae* Model

## Overview




This repository contains all the files used in this project, such as the models, the Python scripts, and the outputs of the optimizations.
The main objective of this project is to optimize the production of curcumin on a previously engineered *S.cerevisiae* using *in silico* strain optimization. To achieve this, we aim to construct, validate and optimize a biosynthetic pathway, that can produce curcumin efficiently.




## Contents

- `/model_code_results`: This directory contains the model, the notebooks and scripts used for the simulation, optimization, and analysis of the *Saccharomyces cerevisiae* model and also stores the results obtained from the optimizations.
  - `yeast-7-GEM_curcumin.xml`: Model

  - `model_analysis_simulations_general.ipynb`: Notebook used to analyze, simulate and visualize the data

  - `.json`: Escher Maps 

  - `optmisation.py`: Script used to perform the optimizations

  - `results_..._.csv`: Raw data from optimizations

  - `frequency_calculator.ipynb`: Notebook used to evaluate the frequency of genes in the different relevant solutions obtained from optimizations.
  
  - `post_optimizations_flux_calculation.ipynb`: # Notebook used to obtain the respective curcumin and biomass fluxes of the solutions from the optimization raw data.

  - `results_..._analisados_.csv`: Data processed with the biomass and curcumin flux from the optimizations.

