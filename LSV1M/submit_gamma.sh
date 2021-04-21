#!/bin/bash
#SBATCH --job-name gamma
# #SBATCH --overcommit
#SBATCH --mem 10G
#SBATCH --time 01:00:00
#SBATCH -o results/gamma_%A.out
#SBATCH -e results/gamma_%A.err

# export HDF5_USE_FILE_LOCKING=FALSE

python run_spectral_analysis.py 
