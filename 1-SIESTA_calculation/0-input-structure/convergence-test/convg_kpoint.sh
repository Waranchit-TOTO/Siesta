#!/bin/bash

root=$(pwd)
ECUT=300

for KPOINT in "6 6 2" "7 7 3" "9 9 3" "12 12 4"; do
	read -r KX KY KZ <<< "$KPOINT"
	label="${KX}x${KY}x${KZ}"

	echo "Submitting k-point mesh: $KX $KY $KZ (ECUT=$ECUT Ry)"
	mkdir -p "$root/kpt_$label"

	sed -e "s/\$ECUT/$ECUT/g" \
		-e "s/\$KX/$KX/g" \
		-e "s/\$KY/$KY/g" \
		-e "s/\$KZ/$KZ/g" \
		"$root/input.fdf" > "$root/kpt_$label/input.fdf"

	cat > "$root/kpt_$label/job.sh" << EOF
#!/bin/bash
#SBATCH -p compute
#SBATCH -N 1
#SBATCH --ntasks-per-node=64
#SBATCH -t 1:00:00
#SBATCH -A lt200358
#SBATCH -J kpt_${label}

module load Mamba
conda activate test-siesta
ulimit -s unlimited
export OMP_NUM_THREADS=1

cd $root/kpt_$label
cp $root/*.psml .
cp $root/SnS2-mp-9984.fdf .
mpirun siesta < input.fdf > output_${label}.out
EOF

	sbatch "$root/kpt_$label/job.sh"
done

