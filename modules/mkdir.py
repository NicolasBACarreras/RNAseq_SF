import sys
sys.path.append('/home/bsc/bsc008978/Box/SnapFlow')
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

        "log_file": f"{working_dir}/{cell}_{cond}/logs/RNA/0_mkdir_RNA.log", 
    }

    cmd = f"""
    set -e

    # Define the main sample directory using an absolute path
    SAMPLE_DIR="{working_dir}/{cell}_{cond}"

    # Create the directory structure using absolute paths
    mkdir -p $SAMPLE_DIR/results/RNA
    mkdir -p $SAMPLE_DIR/fastq/RNA
    mkdir -p $SAMPLE_DIR/logs/RNA
    mkdir -p $SAMPLE_DIR/jobs/RNA

    echo "Working Directory: {working_dir}"  >> $SAMPLE_DIR/logs/0_mkdir_RNA.log
    echo "Cell Type or Tissue: {cell}"       >> $SAMPLE_DIR/logs/0_mkdir_RNA.log
    echo "Condition: {cond}"                 >> $SAMPLE_DIR/logs/0_mkdir_RNA.log
    echo "Replicates: {reps}"                >> $SAMPLE_DIR/logs/0_mkdir_RNA.log

    # Create subdirectories within the results folder
    mkdir -p $SAMPLE_DIR/results/RNA/quality
    mkdir -p $SAMPLE_DIR/results/RNA/alignment
    mkdir -p $SAMPLE_DIR/results/RNA/fcount
    mkdir -p $SAMPLE_DIR/results/RNA/reports
    mkdir -p $SAMPLE_DIR/results/RNA/coverage

    # Loop to create salmon subdirs and move files
    for i in $(seq 1 {reps}); do
    
        # Use an array to safely capture file paths found
        files_to_move=($(find {fasta_dir} -maxdepth 1 -name "{cell}_{cond}_${{i}}_*"))

        # Check if the array is not empty
        if [ ${{#files_to_move[@]}} -gt 0 ]; then
            echo "Found files to move for rep ${{i}}: ${{files_to_move[@]}}" >> $SAMPLE_DIR/logs/0_mkdir_RNA.log
            # Move the found files to the absolute path
            mv "${{files_to_move[@]}}" $SAMPLE_DIR/fastq/RNA/
        else
            echo "WARNING: No FASTQ files found in {fasta_dir} for pattern {cell}_{cond}_${{i}}_* for rep ${{i}}" >> $SAMPLE_DIR/logs/0_mkdir_RNA.log
        fi
    done
"""

