
#! /bin/bash

set -euo pipefail  # any error or undefined variable or pipefail (respectively) will stop the script



cd /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA

SECONDS=0

touch /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.running
rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.error

trap 'error_handler $LINENO $?' ERR

error_handler() {
    echo $SECONDS > /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.error
    rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.running
    exit 1
}

DONE_FILE=/home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.done



    # Provide this with the singularity
    module load hdf5
    module load python/3.12.1
    module load trimgalore/0.6.10


    set -e
    mkdir -p /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/fastq/RNA
    mkdir -p /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/results/RNA/quality /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/results/RNA/reports

    # Find all FASTQ files in the directory (assumes paired-end files)
    FASTQ_FILES=($(ls /home/bsc/bsc008978/test_data/*.fastq* | sort))

    # Check that there are exactly 2 files (paired-end)
    if [ ${#FASTQ_FILES[@]} -ne 2 ]; then
        echo "Error: Expected exactly 2 FASTQ files for paired-end data in /home/bsc/bsc008978/test_data"
        exit 1
    fi

    # Run FastQC
    fastqc ${FASTQ_FILES[0]} ${FASTQ_FILES[1]} -o /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/results/RNA/quality

    # Run Trim Galore (paired-end)
    trim_galore ${FASTQ_FILES[0]} ${FASTQ_FILES[1]}         --paired         --cores 10         --output_dir /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/fastq/RNA         --basename nB_WT1_1

    # Run MultiQC
    multiqc /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/results/RNA/quality -o /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/nB_WT1/results/RNA/reports -f -n 1_quality_RNA_1.multiqc
 2> /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.command.err 1> /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.command.out && echo $SECONDS > $DONE_FILE

echo quality_trimming_RNA ||  rm -f $DONE_FILE

rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.running

if [[ ! -f "$DONE_FILE" ]]; then
  echo $SECONDS > /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/quality_trimming_RNA/.error
  exit 1
fi

