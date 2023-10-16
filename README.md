# genomebact

A pipeline for bacterial assembly and annotation

## test set

Test set: 40 E. coli reads

## Rules

| **xx** | **Rule** | **Description** |
| ------------- | ------------- | ------------- |
| trim, qc reads | fastp/run_fastp |  |
| assembly | assembly/run_assembly | shovill (using spades) |
|  | fast_assembly/run_fast_assembly | skesa |
| qc assembly | quast |  |
| remove bad assemblies | filter.py |  |
| check species | kraken |  |
| sort by species | sort.py | mkdir with species name and split fastas |
| annotate | proka |  |

## Usage
To make a dry run of the analyis:
```
snakemake --use-conda --cores 36 -n -p
```
Snakemake will install the appropriate packages for each step as conda environments when running it without the `-n` flag.
