#!/usr/bin/env python

import os
import sys
from argparse import ArgumentParser
from yaml import Loader, load as load_yaml

from sf import Process_dict, create_workdir, make_path_absolute, IO_type

# Import modules
from modules.mkdir import mkdir_RNA
from modules.quality_trimming import quality_trimming_RNA
from modules.alignment import alignment_RNA
from modules.feature_counts import feature_counts_RNA
from modules.bam_coverage import bam_coverage_RNA

def main():

    #######################################
    # SETUP
    #######################################

    opts = get_options()
    yaml_params = opts.yaml_params
    sample = opts.sample
    result_dir = opts.outdir

    params = load_yaml(open(yaml_params, 'r', encoding='utf-8'), Loader=Loader)
    try:
        sample_params = params[sample]
    except KeyError:
        raise KeyError(f'ERROR: sample name should be one of: [{", ".join(list(params.keys()))}]')

    sample_params['results directory'] = result_dir
    make_path_absolute(sample_params)
    create_workdir(result_dir, sample, None, None, sample_params)

    processes = Process_dict(sample_params, name="RNAseq Pipeline")

    #######################################
    # CREATE DIRECTORY STRUCTURE
    #######################################

    mkdir_process = mkdir_RNA(
        working_dir=result_dir,
        cell=sample_params['cell'],
        cond=sample_params['condition'],
        reps=len(sample_params['reps']),
        fasta_dir=sample_params['fasta_path']
    )

    #######################################
    # RUN PIPELINE PER REPLICATE
    #######################################

    for rep in sample_params['reps']:

        dependency_for_alignment = None
        fastq1_for_alignment = None
        fastq2_for_alignment = None

        sample_dir = f"{result_dir}/{sample_params['cell']}_{sample_params['condition']}"

        #######################################
        # TRIMMING
        #######################################
        if sample_params.get('trimming', 'noTrimming').lower() == 'trimgalore':

            moved_fastq_dir = f"{sample_dir}/fastq/RNA"
            trim_process = quality_trimming_RNA(
                mkdir_process,
                fastq_dir=moved_fastq_dir,
                outdir=os.path.join(sample_dir, 'results/RNA'),
                working_dir=result_dir,
                cell=sample_params['cell'],
                cond=sample_params['condition'],
                rep=rep,
                cpus=10,
                replicate_name=f"trim_rep{rep}"
            )
            dependency_for_alignment = trim_process
            fastq1_for_alignment = trim_process.output['trimmed_fastq_1']
            fastq2_for_alignment = trim_process.output['trimmed_fastq_2']
        else:
            dependency_for_alignment = mkdir_process
            fastq1_for_alignment = f"{sample_dir}/fastq/RNA/{sample_params['cell']}_{sample_params['condition']}_{rep}_R1.fastq.gz"
            fastq2_for_alignment = f"{sample_dir}/fastq/RNA/{sample_params['cell']}_{sample_params['condition']}_{rep}_R2.fastq.gz"

        #######################################
        # ALIGNMENT
        #######################################

        alignment_process = alignment_RNA(
            dependency_for_alignment,
            fastq1=fastq1_for_alignment,
            fastq2=fastq2_for_alignment,
            working_dir=result_dir,
            cell=sample_params['cell'],
            cond=sample_params['condition'],
            rep=rep,
            star_index_dir=sample_params['STAR_index_dir'],
            cpus=15,
            replicate_name=f"align_rep{rep}"
        )


        #######################################
        # QUANTIFICATION
        #######################################

        feature_counts_RNA(
            alignment_process, # <-- Dependency
            working_dir=result_dir,
            cell=sample_params['cell'],
            cond=sample_params['condition'],
            rep=rep,
            gtf_annotation=sample_params['gtf_annotation'],
            cpus=8,
            replicate_name=f"counts_rep{rep}"
        )

        #######################################
        # Coverage
        #######################################

        bam_coverage_RNA(
            alignment_process, # <-- Dependency
            working_dir=result_dir,
            cell=sample_params['cell'],
            cond=sample_params['condition'],
            rep=rep,
            cpus=8,
            replicate_name=f"bigwig_rep{rep}"
        )

    processes.write_commands(opts.sequential, dag_name=f"RNAseq Pipeline for {sample}")


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