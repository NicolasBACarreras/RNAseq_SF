#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from yaml import Loader, load as load_yaml

from sf import Process_dict, create_workdir, make_path_absolute

from modules.mkdir    import mkdir_RNA  # import your rules
from modules.quality_trimming_RNA    import quality_trimming_RNA  # import your rules


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

    # Iterate over replicates
    for replicate in params['reps']:
        # 1 Create working directories
        mkdir_output = mkdir_RNA(
            working_dir=result_dir,
            cell=params['cell'],
            cond=params['condition'],
            reps=replicate,
            fasta_dir=params['fasta_path'],
        )
        processes.add(mkdir_output)

        # 2 Quality trimming & fastqc
        trimming_output = quality_trimming_RNA(
            working_dir=result_dir,
            cell=params['cell'],
            cond=params['condition'],
            rep=replicate,
            genome=params['genome'],
            prev_rule_output=mkdir_output[1]  # pass the output dict from mkdir_RNA
        )
        processes.add(trimming_output)

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
