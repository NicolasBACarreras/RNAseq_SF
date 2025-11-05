import sys
sys.path.append('/home/bsc/bsc008978/Box/SnapFlow')
from sf import IO_type, rule

@rule
def alignment_RNA(dependency_process, fastq1, fastq2, working_dir, cell, cond, rep, star_index_dir, star_options, **kwargs):
    """
    Perform STAR alignment for RNA-seq replicate.
    """
    cpus = kwargs.get('cpus', 15)

    sample_dir = f"{working_dir}/{cell}_{cond}"
    outdir     = f"{sample_dir}/results/RNA"
    jobs_dir   = f"{sample_dir}/jobs/RNA"
    logs_dir   = f"{sample_dir}/logs/RNA"
    log_file   = f"{logs_dir}/2_alignment_RNA_{rep}.log"
    path_prefix = f"{outdir}/alignment/{cell}_{cond}_RNA_{rep}"

    # --- FIX: The input_ dictionary is ONLY for building the dependency graph ---
    # It links to the log file of whichever step came before (trimming or mkdir).
    input_ = {
        "upstream_log": IO_type('path', 'log_file', dependency_process)
    }

    # The actual FASTQ files are passed in directly as arguments
    fastq_files = f"{fastq1} {fastq2}"

    output = {
        "bam": f"{path_prefix}.sort.bam",
        "log": log_file,
    }

    cmd = f"""
    module load star
    module load samtools
    module load sambamba
    module load EB/apps
    module load MultiQC/1.28-foss-2024a 


    set -e
    mkdir -p {jobs_dir} {logs_dir} {outdir}/alignment

    echo "## STAR alignment for {cell}_{cond} {rep}" > {log_file}

    # --- FINAL CORRECTED STAR COMMAND ---
    # The star_options variable from the YAML file is now the single source of truth.
    STAR --runThreadN {cpus} \\
         --genomeDir {star_index_dir} \\
         --readFilesIn {fastq_files} \\
         --readFilesCommand zcat \\
         --outFileNamePrefix {path_prefix} \\
         {star_options}

    # The rest of the script assumes STAR's default output name, which is correct.
    sambamba sort -t {cpus} -o {path_prefix}.sort.bam {path_prefix}Aligned.out.bam
    rm {path_prefix}Aligned.out.bam

    multiqc {outdir}/alignment/*Log.final.out -o {outdir}/reports -f -n 2_alignment_RNA_{rep}.multiqc
"""