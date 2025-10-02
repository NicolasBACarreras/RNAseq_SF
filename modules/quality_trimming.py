from sf import IO_type, rule

@rule
def quality_trimming_RNA(working_dir, cell, cond, rep, genome, prev_rule_output, **kwargs):
    """
    Generate quality control and trimming jobs for RNA-seq.
    Depends on the output of mkdir_RNA.
    """

    fastq_dir = prev_rule_output['fastq_dir']
    outdir = prev_rule_output['results_dir']
    log_dir = prev_rule_output['logs'].rsplit('/', 1)[0]  # parent log directory

    input_ = {
        "working_dir": IO_type("dir", working_dir),
        "cell": IO_type("str", cell),
        "cond": IO_type("str", cond),
        "rep": IO_type("int", rep),
        "genome": IO_type("file", genome),
        "fastq_dir": IO_type("dir", fastq_dir),
        "outdir": IO_type("dir", outdir),
        "log_dir": IO_type("dir", log_dir),
    }

    output = {
        "job_script": f"{working_dir}/{cell}_{cond}/jobs/RNA/1_quality_trimming_RNA_{rep}.sh",
        "log_file": f"{log_dir}/RNA/1_quality_trimming_RNA_{rep}.log",
    }

    cmd = f"""
    set -e
    mkdir -p {working_dir}/{cell}_{cond}/logs/RNA
    mkdir -p {working_dir}/{cell}_{cond}/jobs/RNA

    JOB="{output['job_script']}"
    LOG="{output['log_file']}"

    # Determine file size and threads/time
    FILE_SIZE=$(ls -Ll {fastq_dir}/{cell}_{cond}_{rep}_* | gawk '{{sum += $5; n++;}} END {{print sum/n;}}' | awk '{{foo = $1 / 1024 / 1024 /1024 ; print foo}}' | awk '{{print int($1)+1}}')

    if [ $FILE_SIZE -ge 0 -a $FILE_SIZE -le 2 ]; then TIME="2:00:00"; THREADS=10; fi
    if [ $FILE_SIZE -gt 2 -a $FILE_SIZE -le 4 ]; then TIME="3:00:00"; THREADS=10; fi
    if [ $FILE_SIZE -gt 4 -a $FILE_SIZE -le 8 ]; then TIME="2:00:00"; THREADS=20; fi
    if [ $FILE_SIZE -gt 8 ]; then TIME="5:00:00"; THREADS=20; fi

    TRIM_PARAM="-a 'file:/gpfs/projects/bsc08/shared_projects/IJC_3Dchromatin/programs/adapters.fasta' -A 'file:/gpfs/projects/bsc08/shared_projects/IJC_3Dchromatin/programs/adapters.fasta' --fastqc_args '--outdir {outdir}/quality' --cores $THREADS"

    echo "## Quality & Trimming script" > $JOB

    FASTQ=( $(find {fastq_dir} -name "{cell}_{cond}_{rep}_*" | sort) )

    if [[ ${{#FASTQ[@]}} == 1 ]]; then
        echo "fastqc ${{FASTQ[0]}} -o {outdir}/quality" >> $JOB
        echo "trim_galore ${{FASTQ[0]}} --output_dir {fastq_dir} --basename {cell}_{cond}_{rep} $TRIM_PARAM" >> $JOB
    else
        echo "fastqc ${{FASTQ[0]}} ${{FASTQ[1]}} -o {outdir}/quality" >> $JOB
        echo "trim_galore ${{FASTQ[0]}} ${{FASTQ[1]}} --paired --output_dir {fastq_dir} --basename {cell}_{cond}_{rep} $TRIM_PARAM" >> $JOB
    fi

    echo "multiqc {outdir}/quality/*_fastqc.zip {fastq_dir} -o {outdir}/reports -f -n 1_quality_RNA.multiqc" >> $JOB
    echo "/gpfs/projects/bsc08/shared_projects/IJC_3Dchromatin/programs/transcriptomics/2_alignment.sh {working_dir} {cell} {cond} {rep} {genome}" >> $JOB
    echo "/gpfs/projects/bsc08/shared_projects/IJC_3Dchromatin/programs/transcriptomics/2b_salmon.sh {working_dir} {cell} {cond} {rep} {genome}" >> $JOB

    chmod +x $JOB
    sbatch --time=$TIME --cpus-per-task=$THREADS --job-name=QC_Trim_{cell}_{cond}_RNA_{rep} --output={log_dir}/RNA/1_quality_trimming_RNA_{rep}_%j.out --error={log_dir}/RNA/1_quality_trimming_RNA_{rep}_%j.err $JOB
    echo "Job submitted at $(date)" >> $LOG
    """

    return input_, output, cmd
