# genomebact

A minimal pipeline for bacterial assembly and annotation

![GitHub Logo](config/img/logo.jpg)

## Pipeline

Test set: 40 E. coli reads

**QC reads**
This pipeline checks the quality of the reads and trims them using ![fastp](https://github.com/OpenGene/fastp).

**Assembly**
Two assemblers can be used:
- Fast assembly: uses the fast assembler ![skesa](https://github.com/ncbi/SKESA)
- Assmebly: uses ![shovill](https://github.com/tseemann/shovill)

Afterwards, the quality of the assemblies is checked with ![quast](https://github.com/ablab/quast), and fastas with low quality are removed.

**Annotation** 
 The preserved fastas are annotated using ![prokka](https://github.com/tseemann/prokka).


### **To include - to make it not so minimal :)**
- [ ] run ![kraken2](https://github.com/DerrickWood/kraken2) for species identification
- [ ] split fastas and gffs into species directories (data/ecoli/fastas & data/ecoli/gffs)
- [ ] typing w/ ![mlst](https://github.com/tseemann/mlst)
- [ ] ![kleborate](https://github.com/klebgenomics/Kleborate) for klebsiella isolates
- [ ] identify amr genes ![amrfinderplus](https://github.com/ncbi/amr) & ![ARIBA](https://github.com/sanger-pathogens/ariba)
- [ ] harmonize amr reports w/ ![hAMRonization](https://github.com/pha4ge/hAMRonization)
- [ ] create one single output report
- [ ] create output viz

## Usage
First run the ```bootstrap.sh``` script to create all necessary directories and input files.

Then, to make a dry run of the analyis:
```
snakemake --use-conda --cores 12 -n -p
```

Snakemake will install the appropriate packages for each step as conda environments when running it without the `-n` flag.

## Author
Judit Burgaya (BurgayaVentura.Judit@mh-hannover.de | judit.burgaya@gmail.com)
