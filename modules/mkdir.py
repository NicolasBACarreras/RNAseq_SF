from sf import IO_type, rule

@rule
def mkdir_RNA(working_dir, cell, cond, reps, fasta_dir, **kwargs):
    """
    Create the directory structure for RNA-seq project.
    This rule has no file inputs or outputs (only creates folders).
    """

    # No file inputs or outputs
    input_ = {}
    output = {}

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