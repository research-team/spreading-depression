#source /usr/mpi/gcc/openmpi-1.10.2-lsf/bin/mpivars.sh

export OMP_NUM_THREADS=1

#mpiexec="/usr/mpi/gcc/openmpi-1.10.2-lsf/bin/mpiexec"
nrniv="/gpfs/GLOBAL_JOB_REPO_KPFU/openlab/NEURON/nrn77/build/x86_64/bin/nrniv"
script="/gpfs/GLOBAL_JOB_REPO_KPFU/openlab/NEURON/SD/Spreading-Depression-Neuron-/test_wave.py"

bsub -J NeuronCalculation -e ERRROS.err -o OUTPUT.out -m cluster-manager -n 16 mpiexec -np 16 ${nrniv} -mpi -python ${script}
