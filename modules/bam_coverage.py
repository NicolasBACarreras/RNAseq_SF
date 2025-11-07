from sf import IO_type, rule

@rule
def bam_coverage_RNA(alignment_process, working_dir, cell, cond, rep, **kwargs):
    """
    Generate a BigWig coverage file using bamCoverage from deepTools.
    This rule also depends on the alignment process.
    """
    cpus = kwargs.get('cpus', 8)

    sample_dir = f"{working_dir}/{cell}_{cond}"
    outdir     = f"{sample_dir}/results/RNA"
    logs_dir   = f"{sample_dir}/logs/RNA"
    log_file   = f"{logs_dir}/3_bamcoverage_RNA_{rep}.log"
    bigwig_file = f"{outdir}/coverage/{cell}_{cond}_{rep}.bw"

    input_ = {
        "sorted_bam": IO_type('path', 'bam', alignment_process)
    }

    output = {
        "bigwig": bigwig_file,
        "log": log_file
    }

    cmd = f"""
    set -e
    mkdir -p {outdir}/coverage
    echo "## bamCoverage for {cell}_{cond} {rep}" > {log_file}

    bamCoverage --bam {input_['sorted_bam']} \\
                -o {bigwig_file} \\
                --numberOfProcessors {cpus} \\
                --normalizeUsing BPM --binSize 10

    """
    return cmd