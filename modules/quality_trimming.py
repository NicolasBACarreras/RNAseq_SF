import sys
sys.path.append('/home/bsc/bsc008978/Box/SnapFlow')
from sf import IO_type, rule

@rule
def quality_trimming_RNA(mkdir_out, fastq_dir, outdir, working_dir, cell, cond, rep, **kwargs):
    """
    Quality control and trimming for RNA-seq.
    """
    # This line is good, it gets the value from the pipeline script
    cpus_requested = kwargs.get('cpus', 10)

    logs_dir = f"{working_dir}/{cell}_{cond}/logs"
    log_file = f"{logs_dir}/1_trimming_RNA_{rep}.log"

    input_ = { "mkdir_log": IO_type('path' , 'log_file', mkdir_out) }
    
    output = {
        "trimmed_fastq_1": f"{working_dir}/{cell}_{cond}/fastq/RNA/{cell}_{cond}_{rep}_val_1.fq.gz",
        "trimmed_fastq_2": f"{working_dir}/{cell}_{cond}/fastq/RNA/{cell}_{cond}_{rep}_val_2.fq.gz",
        "log_file": log_file
    }

    # --- THIS IS THE FIX ---
    # We explicitly define the 'cpus' variable right before the f-string uses it.
    cpus = cpus_requested

    cmd = f"""
    module load hdf5
    module load python/3.12.1
    module load trimgalore/0.6.10

    set -e
    mkdir -p {outdir}/quality {outdir}/reports
    mkdir -p {logs_dir}

    echo "## Trimming for {cell}_{cond} rep{rep}" > {log_file}

    FASTQ_1=$(ls {fastq_dir}/{cell}_{cond}_{rep}_*R1*)
    FASTQ_2=$(ls {fastq_dir}/{cell}_{cond}_{rep}_*R2*)
    
    if [ $(echo "$FASTQ_1" | wc -w) -ne 1 ] || [ $(echo "$FASTQ_2" | wc -w) -ne 1 ]; then
        echo "ERROR: Could not find exactly one R1 and one R2 file in {fastq_dir}" >> {log_file}
        exit 1
    fi

    echo "Found FASTQ files:" >> {log_file}
    echo "R1: $FASTQ_1" >> {log_file}
    echo "R2: $FASTQ_2" >> {log_file}

    fastqc $FASTQ_1 $FASTQ_2 -o {outdir}/quality

    trim_galore --paired $FASTQ_1 $FASTQ_2 \\
        --cores {cpus} \\
        --output_dir {working_dir}/{cell}_{cond}/fastq/RNA \\
        --basename {cell}_{cond}_{rep} 2>> {log_file}

    multiqc {outdir}/quality -o {outdir}/reports -f -n 1_quality_RNA_{rep}.multiqc
    """