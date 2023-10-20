#!/usr/bin/env python

import os
import gzip
import argparse
import pandas as pd

def get_options():
    description = 'Get CDS counts from .gff.gz files'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument('gffsdir',
                        help='Directory containing the .gff.gz files')
    
    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    output_file = 'cds_counts.tsv'

    with open(output_file, 'w') as out_file:
        out_file.write("sample\tcds\n")

        files = os.listdir(options.gffsdir)

        for file in files:
            if file.endswith('.gff.gz'):
                sample_id = file.split('.gff.gz')[0]
                cds_count = 0

                with gzip.open(os.path.join(options.gffsdir, file), 'rt') as gff_file:
                    for line in gff_file:
                        if "CDS" in line:
                            cds_count += 1

                out_file.write(f"{sample_id}\t{cds_count}\n")

    df = pd.read_csv(output_file, sep='\t')
    df.to_csv(os.path.join(options.gffsdir, "cds_counts.tsv"), sep='\t', index=False)
