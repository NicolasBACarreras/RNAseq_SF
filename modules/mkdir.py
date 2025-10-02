from sf import IO_type, rule

@rule
def mkdir_RNA(working_dir, cell, cond, reps, fasta_dir, param_file=None, **kwargs):
    """
    Create the directory structure for RNA-seq project.
    Translated from the original shell script.
    """

    input_ = {
        "working_dir": IO_type("dir", working_dir),
        "cell": IO_type("str", cell),
        "cond": IO_type("str", cond),
        "reps": IO_type("int", reps),
        "fasta_dir": IO_type("dir", fasta_dir),
        "param_file": IO_type("file", param_file) if param_file else None,
    }

    output = {
        "rna_dir": f"{working_dir}/{cell}_{cond}",
        "fastq_dir": f"{working_dir}/{cell}_{cond}/fastq/RNA",
        "results_dir": f"{working_dir}/{cell}_{cond}/results/RNA",
        "logs": f"{working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log",
    }

    cmd = f"""
    set -e
    cd {input_['working_dir']}

    if [ -d "{cell}_{cond}" ]; then
        cd {cell}_{cond}
    else
        mkdir -p {cell}_{cond}
        cd {cell}_{cond}
    fi

    mkdir -p results fastq logs jobs

    echo "Working Directory:" {working_dir} >> {working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log
    echo "Cell Type or Tissue:" {cell} >> {working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log
    echo "Condition:" {cond} >> {working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log
    echo "Replicates:" {reps} >> {working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log

    mkdir -p fastq/RNA
    mkdir -p results/RNA
    mkdir -p jobs/RNA
    mkdir -p logs/RNA

    cd results/RNA
    mkdir -p quality alignment fcount salmon reports coverage

    for i in $(seq 1 {reps}); do
        mkdir -p salmon/{cell}_{cond}_${{i}}
        echo mv $(find {fasta_dir} -maxdepth 1 -name "{cell}_{cond}_${{i}}_*") {working_dir}/{cell}_{cond}/fastq/RNA >> {working_dir}/{cell}_{cond}/logs/0_mkdir_RNA.log
        mv $(find {fasta_dir} -maxdepth 1 -name "{cell}_{cond}_${{i}}_*") {working_dir}/{cell}_{cond}/fastq/RNA/
    done
    """