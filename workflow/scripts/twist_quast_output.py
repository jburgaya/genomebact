#!/usr/bin/env python

# script to get a simple file with the sampleid, N50, total length, and CDS count

import sys
import argparse
import pandas as pd
import glob
import os

def get_options():
    description = 'script to get a simple file with the sampleid, N50, total length, and CDS count from the multiple subdirectories and the report.tsv output from quast'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('quastdir',
                        help='Quast directory containing the output subdirectories per sample, with the report.tsv inside')
    parser.add_argument('cdscount',
                        help='CDS count from .gff.gz files output from count_cds.py')
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
    parser.add_argument('--mincds',
                        default=5000,
                        type=int,
                        help='Default set to 5000')
    parser.add_argument('--maxcds',
                        default=7000,
                        type=int,
                        help='Default set to 7000')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    # Function to process a single report.tsv file
    def process_file(filename, cds_data):
        with open(filename, 'r') as file:
            lines = file.readlines()
            sampleid = lines[0].strip().split('\t')[1]
            totallen = lines[15].strip().split('\t')[1]
            n50 = lines[17].strip().split('\t')[1]

            # Get CDS count for the sample from the cds_data DataFrame
            filtered_data = cds_data[cds_data['sample'] == sampleid]
            if not filtered_data.empty:
                cds_count = filtered_data['cds'].values[0]
            else:
                cds_count = 0

            return sampleid, totallen, n50, cds_count

    # Read CDS count data
    cds_data = pd.read_csv(options.cdscount, sep='\t')

    # Initialize empty lists to store the data
    sample_ids = []
    total_lengths = []
    n50_values = []
    cds_counts = []

    report_files = glob.glob(os.path.join(options.quastdir, '**/report.tsv'), recursive=True)

    # Process each report file and store the data
    for file in report_files:
        sampleid, totallen, n50, cds_count = process_file(file, cds_data)
        sample_ids.append(sampleid)
        total_lengths.append(totallen)
        n50_values.append(n50)
        cds_counts.append(cds_count)

    # Create a DataFrame from the collected data
    df = pd.DataFrame({'sample': sample_ids, 'totallen': total_lengths, 'n50': n50_values, 'cds': cds_counts})
    df['totallen'] = pd.to_numeric(df['totallen'])
    df['n50'] = pd.to_numeric(df['n50'])

    # conditions
    totallen = (df['totallen'] >= options.minlen) & (df['totallen'] <= options.maxlen)
    n50 = df['n50'] > options.n50
    cds = (df['cds'] >= options.mincds) & (df['cds'] <= options.maxcds)

    filterdf = df[totallen & n50 & cds]
    toremovedf = df[~(totallen & n50 & cds)]

    toremovedf['reason'] = ''
    toremovedf.loc[~totallen, 'reason'] += 'len'
    toremovedf.loc[~n50, 'reason'] += 'n50'
    toremovedf.loc[~cds, 'reason'] += 'cds'
    toremovedf = toremovedf[['sample', 'totallen', 'n50', 'cds', 'reason']]

    df.to_csv(os.path.join(options.quastdir, 'quast_output.tsv'), sep='\t', index=False)
    filterdf.to_csv(os.path.join(options.quastdir, 'quast_output_f.tsv'), sep='\t', index=False)
    toremovedf.to_csv(os.path.join(options.quastdir, 'quast_output_toremove.tsv'), sep='\t', index=False)
