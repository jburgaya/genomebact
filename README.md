# genomebact

A minimal pipeline for bacterial assembly and annotation

![GitHub Logo](config/img/logo.jpg)

## Rules

Test set: 40 E. coli reads

This pipeline checks the quality of the reads and trims them using *fastp*, it then assembles them using a fast assembler *skesa*. Quality of the assemblies are checked with *QUAST* and then fastas with low quality criteria are removed. Further, annotations are done using *prokka*.

## Usage
To make a dry run of the analyis:
```
snakemake --use-conda --cores 12 -n -p
```
Snakemake will install the appropriate packages for each step as conda environments when running it without the `-n` flag.

## Author
Judit Burgaya (BurgayaVentura.Judit@mh-hannover.de | judit.burgaya@gmail.com)
