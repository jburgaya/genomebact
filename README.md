# genomebact
A pipeline for bacterial assembly and annotation

Test set: 40 E. coli reads

| **xx** | **Rule** | **Description** |
| ------------- | ------------- |
| trim, qc reads | fastp/run_fastp |  |
| assembly | assembly/run_assembly | shovill (using spades) |
|  | fast_assembly/run_fast_assembly | skesa |
| qc assembly | quast |  |
| remove bad assemblies | filter.py |  |
| check species | kraken |  |
| sort by species | sort.py | mkdir with species name and split fastas |
| annotate | proka |  |
