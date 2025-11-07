# RNAseq_SF
RNAseq pipeline using SnapFlow (https://github.com/fransua/SnapFlow)

Flow diagram of Pipeline:

![RNAseq_SF](flow_diagram_rna.png)

Example usage:

```bash
python rna_seq_pipeline.py --sample sample1 -o results -p params.yaml > command.q
```

Use slurm_do.py (https://github.com/fransua/slurm_utils/blob/master/scripts/submitting/slurm_do.py) to schedule the jobs to Slurm

```bash
slurm_do.py -i command.q
```


