#!/usr/bin/env python

import sys
import argparse
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

def get_options():
    description = 'Script to generate scatterplots with modified colors from Quast output.'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('quastout',
                        help='Quast output file with all the samples quast_output.tsv')
    parser.add_argument('output_dir',
                        help='Directory to save the scatterplots')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    df = pd.read_csv(options.quastout, sep='\t')

    if 'n50' in df.columns and 'cds' in df.columns and 'totallen' in df.columns:
        # Create the conditions for color assignment
        # to show the global conditions, hence the removed fastas
        conditions = [(df['n50'] > 50000) & (df['cds'] > 5000) & (df['totallen'] > 5500000) & (df['totallen'] < 7500000) & (df['cds'] < 7500)]
        # to show the specific conditions per each plot
#        conditions = [
#            (df['n50'] > 50000) & (df['cds'] > 5000) & (df['cds'] < 7500),
#            (df['totallen'] > 5500000) & (df['totallen'] < 7500000) & (df['cds'] > 5000) & (df['cds'] < 7500)
#        ]

	colors = ['grey', 'grey']
        default_color = 'red'

        # Create a new column for colors based on conditions
        df['color'] = default_color
        for i, cond in enumerate(conditions):
            df.loc[cond, 'color'] = colors[i]
        print(df)

        # Create scatter plots using Seaborn
        plt.figure(figsize=(18, 6))
        plt.subplot(1, 3, 1)
        sns.scatterplot(data=df, x='n50', y='cds', hue='color', palette={'grey': 'grey', 'red': 'red'})
        plt.title('N50 vs CDS count')
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=5))

        plt.subplot(1, 3, 2)
        sns.scatterplot(data=df, x='totallen', y='cds', hue='color', palette={'grey': 'grey', 'red': 'red'})
        plt.title('Genome length vs CDS count')
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=5))

        plt.subplot(1, 3, 3)
        sns.scatterplot(data=df, x='totallen', y='n50', hue='color', palette={'grey': 'grey', 'red': 'red'})
        plt.title('Genome length vs N50')
        plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=5))

        plot_filename = os.path.join(options.output_dir, 'plot_quast.png')
        plt.savefig(plot_filename)

        plt.tight_layout()

    else:
	print("The required columns ('n50', 'cds', and 'totallen') are missing in the DataFrame.")
