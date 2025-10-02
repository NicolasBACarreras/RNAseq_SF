from sf import IO_type, rule

@rule
def quality_trimming_RNA(mkdir_out, fastq_path, outdir, working_dir, cell, cond, rep, **kwargs):
    """
    Quality control and trimming for RNA-seq.

    """

    cpus = kwargs.get('cpus', 10)  # default to 10 if not provided

    # Only real files in input/output
    input_ = {
        "log_file": mkdir_out

    }

    output = {
        "trimmed_fastq_1": f"{working_dir}/{cell}_{cond}/fastq/RNA/{cell}_{cond}_{rep}_1_trimmed.fq.gz",
        "trimmed_fastq_2": f"{working_dir}/{cell}_{cond}/fastq/RNA/{cell}_{cond}_{rep}_2_trimmed.fq.gz"
    }

    cmd = f"""

    # Provide this with the singularity
    module load hdf5
    module load python/3.12.1
    module load trimgalore/0.6.10


    set -e
    mkdir -p {working_dir}/{cell}_{cond}/fastq/RNA
    mkdir -p {outdir}/quality {outdir}/reports

    # Find all FASTQ files in the directory (assumes paired-end files)
    FASTQ_FILES=($(ls {fastq_path}/*.fastq* | sort))

    # Check that there are exactly 2 files (paired-end)
    if [ ${{#FASTQ_FILES[@]}} -ne 2 ]; then
        echo "Error: Expected exactly 2 FASTQ files for paired-end data in {fastq_path}"
        exit 1
    fi

    # Run FastQC
    fastqc ${{FASTQ_FILES[0]}} ${{FASTQ_FILES[1]}} -o {outdir}/quality

    # Run Trim Galore (paired-end)
    trim_galore ${{FASTQ_FILES[0]}} ${{FASTQ_FILES[1]}} \
        --paired \
        --cores {cpus} \
        --output_dir {working_dir}/{cell}_{cond}/fastq/RNA \
        --basename {cell}_{cond}_{rep}

    # Run MultiQC
    multiqc {outdir}/quality -o {outdir}/reports -f -n 1_quality_RNA_{rep}.multiqc
"""
