[name mkdir_RNA;cpus-per-task 1;time 1]  /bin/bash /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/mkdir/mkdir_RNA/.command.sh
[name quality_trimming_RNA_trim_rep1;cpus-per-task 10;time 1;depe 1]  /bin/bash /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/quality_trimming/quality_trimming_RNA/trim_rep1/.command.sh
[name alignment_RNA_align_rep1;cpus-per-task 15;time 1;depe 2]  /bin/bash /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/alignment/alignment_RNA/align_rep1/.command.sh
[name feature_counts_RNA_counts_rep1;cpus-per-task 8;time 1;depe 3]  /bin/bash /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/feature_counts/feature_counts_RNA/counts_rep1/.command.sh
[name bam_coverage_RNA_bigwig_rep1;cpus-per-task 8;time 1;depe 3]  /bin/bash /home/bsc/bsc008978/Box/pipelines/RNAseq_SF/results/tmp/bam_coverage/bam_coverage_RNA/bigwig_rep1/.command.sh
