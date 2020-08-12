#!/usr/bin/env python3
import numpy as np
import os
import argparse

def CPU_script(filename,name,queue="gac.cpu"):
    script=open(filename,"w+")
    script.write(f"""
#!/bin/bash
#PBS -q {queue}
#PBS -l nodes=1:ppn=20,mem=80GB
#PBS -j oe
#PBS -r n
#PBS -o {name}.logfile
#PBS -N {name}
#PBS --mail-user=markahix@gmail.com
#PBS --mail-type=all

cd $PBS_O_WORKDIR
cat $PBS_NODEFILE > $PWD/PBS_NODEFILE

#module load amber/19-mvapich
#mpirun -np 20 -hostfile $PWD/PBS_NODEFILE
""")
    script.close()
    return

def GPU_script(filename,name,node,card_num,queue="gac.gpu"):
        script=open(filename,"w+")
    script.write(f"""
#!/bin/bash
#PBS -q {queue}
#PBS -l nodes={node}
#PBS -j oe
#PBS -r n
#PBS -o {name}.logfile
#PBS -N {name}
#PBS --mail-user=markahix@gmail.com
#PBS --mail-type=all

export CUDA_VISIBLE_DEVICES={card_num}
cd $PBS_O_WORKDIR
cat $PBS_NODEFILE > $PWD/PBS_NODEFILE

#module load amber/19-mvapich
#mpirun -np 20 -hostfile $PWD/PBS_NODEFILE
""")
    script.close()
    return


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-cpu", dest="cpu",action="store_true", default=False, help="Creates CPU-based job")
    parser.add_argument("-gpu", dest="gpu",action="store_true", default=False, help="Creates GPU-based job")
    parser.add_argument("-n","--name",dest="name",required=True,help="Job Name")
    parser.add_argument("-s","--scriptname",dest="scriptname",default="JobScript.sh", help="Filename for the job script.")
    parser.add_argument("-q","--queue",dest="queue",help="Queue identifier")
    parser.add_argument("--node", dest="node",default="g15-1-19",help="Node identifier")
    parser.add_argument("--card_num",dest="card_num",default=0,help="GPU Identifier")
    args =parser.parse_args()

