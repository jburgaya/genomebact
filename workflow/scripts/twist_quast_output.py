#!/usr/bin/env python

# script to get a simple file with the sampleid, N50 and total length
# output from quast

import sys
import argparse
import pandas as pd
import glob
import os

def get_options():
    description = 'script to get a simple file with the sampleid, N50 and total length from the multiple subdirectories and the report.tsv output from quast'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('quastdir',
                        help='Quast directory containing the output subdirectories per sample, with the report.tsv inside')
    parser.add_argument('--minlen',
                        default=4500000,
                        type=int,
                        help='Default set to 4500000')
    parser.add_argument('--maxlen',
                        default=5500000,
                        type=int,
                        help='Default set to 5500000')
    parser.add_argument('--n50',
                        default=75000,
                        type=int,
                        help='Default set to 75000')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    # Function to process a single report.tsv file
    def process_file(filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            sampleid = lines[0].strip().split('\t')[1]
            totallen = lines[15].strip().split('\t')[1]
            n50 = lines[17].strip().split('\t')[1]

            return sampleid, totallen, n50

    # Initialize empty lists to store the data
    sample_ids = []
    total_lengths = []
    n50_values = []

    report_files = glob.glob(os.path.join(options.quastdir, '**/report.tsv'), recursive=True)

    # Process each report file and store the data
    for file in report_files:
        sampleid, totallen, n50 = process_file(file)
        sample_ids.append(sampleid)
        total_lengths.append(totallen)
        n50_values.append(n50)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({'sample': sample_ids, 'totallen': total_lengths, 'n50': n50_values})
    df['totallen'] = pd.to_numeric(df['totallen'])
    df['n50'] = pd.to_numeric(df['n50'])

    # conditions
    totallen = (df['totallen'] >= options.minlen) & (df['totallen'] <= options.maxlen)
    n50 = df['n50'] > options.n50

    filterdf = df[totallen & n50]
    toremovedf = df[~(totallen & n50)]

    df.to_csv(os.path.join(options.quastdir, 'quast_output.tsv'), sep='\t', index=False)
    filterdf.to_csv(os.path.join(options.quastdir, 'quast_output_f.tsv'), sep='\t', index=False)
    toremovedf.to_csv(os.path.join(options.quastdir, 'quast_output_toremove.tsv'), sep='\t', index=False)
