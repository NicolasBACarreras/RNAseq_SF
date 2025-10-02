from sf import IO_type, rule

@rule
def mkdir_RNA(working_dir, cell, cond, reps, fasta_dir, **kwargs):
    """
    Create the directory structure for RNA-seq project.
    This rule has no file inputs or outputs (only creates folders).
    """

    # No file inputs or outputs
    input_ = {}
    output = {

        "log_file": f"{working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log", 
    }

    cmd = f"""
    set -e
    cd {working_dir}

    if [ ! -d "{cell}_{cond}" ]; then
        mkdir -p {cell}_{cond}
    fi
    cd {cell}_{cond}

    mkdir -p results fastq logs jobs
    mkdir -p fastq/RNA results/RNA jobs/RNA logs/RNA

    echo "Working Directory: {working_dir}"  >> logs/0_mkdir_RNA.log
    echo "Cell Type or Tissue: {cell}"       >> logs/0_mkdir_RNA.log
    echo "Condition: {cond}"                 >> logs/0_mkdir_RNA.log
    echo "Replicates: {reps}"                >> logs/0_mkdir_RNA.log

    cd results/RNA
    mkdir -p quality alignment fcount salmon reports coverage

    for i in $(seq 1 {reps}); do
        mkdir -p salmon/{cell}_{cond}_${{i}}
        echo mv $(find {fasta_dir} -maxdepth 1 -name "{cell}_{cond}_${{i}}_*") ../fastq/RNA >> ../../logs/0_mkdir_RNA.log
        mv $(find {fasta_dir} -maxdepth 1 -name "{cell}_{cond}_${{i}}_*") ../fastq/RNA/
    done
    """

@rule
def quality_trimming_RNA(mkdir_out, fastq_path, outdir, working_dir, cell, cond, rep, **kwargs):
    """
    Quality control and trimming for RNA-seq.

    """

    cpus = kwargs.get('cpus', 10)  # default to 10 if not provided

    # Only real files in input/output
    input_ = {
        "log_file": IO_type('path' , 'log_file', mkdir_out),

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