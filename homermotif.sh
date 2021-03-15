#!/bin/bash

#SBATCH -n 1                               # Request one core
#SBATCH -N 1                               # Request one node (if you request more than one core with                                            # -N 1 means all cores will be on the same node)
#SBATCH -t 0-08:00                         # Runtime in D-HH:MM format
#SBATCH -p short                         # Partition to run in
#SBATCH --mem=60000
module load gcc/6.2.0
module load homer/4.10.3

findMotifsGenome.pl $1 dicty_chromosomal $2 -size 200 -mask -h
