#!/bin/bash

root=$(pwd)
KX=9
KY=9
KZ=3

for E in 150 200 250 300 400 600; do
    echo "Submitting ECUT=$E Ry (k-points: $KX $KY $KZ)"
    mkdir -p "ecut_$E"

    sed -e "s/\$ECUT/$E/g" \
        -e "s/\$KX/$KX/g" \
        -e "s/\$KY/$KY/g" \
        -e "s/\$KZ/$KZ/g" \
        "$root/input.fdf" > "$root/ecut_$E/input.fdf"

    cat > "$root/ecut_$E/job.sh" << EOF
#!/bin/bash
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=64
#SBATCH -t 1:00:00
#SBATCH -A lt200358
#SBATCH -J ecut_${E}

module load Mamba
conda activate test-siesta
ulimit -s unlimited
export OMP_NUM_THREADS=1

cd $root/ecut_${E}
cp $root/*.psml .
cp $root/SnS2-mp-9984.fdf .
mpirun  siesta < input.fdf > output_${E}.out
EOF

    sbatch "$root/ecut_$E/job.sh"
done

