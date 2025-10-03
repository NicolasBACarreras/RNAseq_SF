#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from yaml import Loader, load as load_yaml

sys.path.append('/home/bsc/bsc008978/Box/pipelines/SnapFlow')

from sf import Process_dict, create_workdir, make_path_absolute

from modules.mkdir  import mkdir_RNA,  quality_trimming_RNA

# import your rules
#from modules.quality_trimming    import quality_trimming_RNA  # import your rules


def main(): 
    opts = get_options()
    
    yaml_params = opts.yaml_params
    sample = opts.sample
    result_dir = opts.outdir

    # Load YAML metadata
    params = load_yaml(open(yaml_params, 'r', encoding='utf-8'), Loader=Loader)
    try:
        params = params[sample]
    except KeyError:
        raise KeyError(f'ERROR: sample name should be one of: [{", ".join(list(params.keys()))}]')

    make_path_absolute(params)
    create_workdir(result_dir, sample, None, None, params)

    ##################################################################################################
    # START WORKFLOW


    # Initialize Process_dict for workflow management
    processes = Process_dict(params, name="RNAseq-HPC")


    # -------------------
    # Step 1: Create directory structure
    # -------------------
    mkdir_out = mkdir_RNA(
                    working_dir=result_dir,
                    cell=params['cell'],
                    cond=params['condition'],
                    reps=len(params['reps']),
                    fasta_dir=params['fasta_path']
    )

    # -------------------
    # Step 2: Quality control and trimming
    # -------------------
    # Assume single replicate example; loop over replicates if needed
    for rep in params['reps']:
        # Construct fastq files for this replicate
      
        quality_trimming_RNA(
            mkdir_out,
            fastq_path=params['fasta_path'],
            outdir=os.path.join(result_dir, params['cell'] + "_" + params['condition'], 'results/RNA'),
            working_dir=result_dir,
            cell=params['cell'],
            cond=params['condition'],
            rep=rep,
            cpus=10   # specify CPUs for trimming
        )


    ##################################################################################################
    # END WORKFLOW
    processes.write_commands(opts.sequential)


def get_options():
    parser = ArgumentParser()
    parser.add_argument('--sample', required=True, help="Name of the sample in YAML")
    parser.add_argument('-o', dest='outdir', required=True, help="Output directory")
    parser.add_argument('-p', '--yaml_params', required=True, help="YAML parameter file")
    parser.add_argument('--sequential', action='store_true', help="Write commands sequentially")
    opts = parser.parse_args()
    return opts


if __name__ == "__main__":
    sys.exit(main())
