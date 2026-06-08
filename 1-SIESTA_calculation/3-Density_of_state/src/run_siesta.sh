#!/bin/bash
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=64
#SBATCH -t 1:00:00
#SBATCH -A lt200358
#SBATCH -J siesta

module load Mamba
conda activate test-siesta
ulimit -s unlimited
export OMP_NUM_THREADS=1

in="${1:-input}"

mpirun siesta < $in.fdf > $in.out

