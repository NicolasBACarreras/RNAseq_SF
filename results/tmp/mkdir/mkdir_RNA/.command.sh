
#! /bin/bash

set -euo pipefail  # any error or undefined variable or pipefail (respectively) will stop the script



cd /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA

SECONDS=0

touch /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.running
rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.error

trap 'error_handler $LINENO $?' ERR

error_handler() {
    echo $SECONDS > /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.error
    rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.running
    exit 1
}

DONE_FILE=/home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.done


    set -e
    cd /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results

    if [ ! -d "nB_WT1" ]; then
        mkdir -p nB_WT1
    fi
    cd nB_WT1

    mkdir -p results fastq logs jobs
    mkdir -p fastq/RNA results/RNA jobs/RNA logs/RNA

    echo "Working Directory: /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results"  >> logs/0_mkdir_RNA.log
    echo "Cell Type or Tissue: nB"       >> logs/0_mkdir_RNA.log
    echo "Condition: WT1"                 >> logs/0_mkdir_RNA.log
    echo "Replicates: 1"                >> logs/0_mkdir_RNA.log

    cd results/RNA
    mkdir -p quality alignment fcount salmon reports coverage

    for i in $(seq 1 1); do
        mkdir -p salmon/nB_WT1_${i}
        echo mv $(find /home/bsc/bsc008978/test_data -maxdepth 1 -name "nB_WT1_${i}_*") ../fastq/RNA >> ../../logs/0_mkdir_RNA.log
        mv $(find /home/bsc/bsc008978/test_data -maxdepth 1 -name "nB_WT1_${i}_*") ../fastq/RNA/
    done
     2> /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.command.err 1> /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.command.out && echo $SECONDS > $DONE_FILE

echo mkdir_RNA ||  rm -f $DONE_FILE

rm -f /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.running

if [[ ! -f "$DONE_FILE" ]]; then
  echo $SECONDS > /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.error
  exit 1
fi

