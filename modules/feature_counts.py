import sys
sys.path.append('/home/bsc/bsc008978/Box/SnapFlow')
from sf import IO_type, rule

@rule
def feature_counts_RNA(alignment_process, working_dir, cell, cond, rep, gtf_annotation, **kwargs):
    """
    Count reads per gene using featureCounts.
    This rule depends on the output of the alignment process.
    """
    cpus = kwargs.get('cpus', 8)

    sample_dir = f"{working_dir}/{cell}_{cond}"
    outdir     = f"{sample_dir}/results/RNA"
    logs_dir   = f"{sample_dir}/logs/RNA"
    log_file   = f"{logs_dir}/3_featurecounts_RNA_{rep}.log"
    counts_file = f"{outdir}/fcount/{cell}_{cond}_{rep}.counts.tsv"

    # Input: The sorted BAM file from the alignment step.
    input_ = {
        "sorted_bam": IO_type('path', 'bam', alignment_process)
    }

    output = {
        "counts": counts_file,
        "summary": f"{counts_file}.summary",
        "log": log_file
    }

    cmd = f"""
    module load subread

    set -e
    mkdir -p {outdir}/fcount
    echo "## featureCounts for {cell}_{cond} {rep}" > {log_file}

    featureCounts -T {cpus} \\
                  -a {gtf_annotation} \\
                  -s 2 -p -t exon -g gene_id \\
                  -o {counts_file} \\
                  {input_['sorted_bam']}

    """
    return cmd