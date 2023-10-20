#!/usr/bin/env python

import os
import shutil
import argparse

def get_options():
    description = 'Move fastas files based on their low-quality output from twist_quast_output.py. IMPORTANT: check fasta extension and change if necessary'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('fastasdir',
                        help='Directory containing assemblies')
    parser.add_argument('toremove',
                        help='Output file from twist_quast_output.py')
    parser.add_argument('removeddir',
                        help='Directory to move the low-quality fastas')

    return parser.parse_args()

if __name__ == "__main__":
    options = get_options()

    # You may need to convert relative paths to absolute paths based on the working directory.
    fastasdir = os.path.abspath(options.fastasdir)
    toremove = os.path.abspath(options.toremove)
    removeddir = os.path.abspath(options.removeddir)

    sample_id_mapping = {}
    with open(toremove, 'r') as f:
        # Skip header
        next(f) 
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 3:
                sample_id = parts[0]
                sample_id_mapping[sample_id] = os.path.join(removeddir, sample_id)

    # Iterate through the files in the source directory and move them based on sample ID
    for filename in os.listdir(fastasdir):
        if filename.endswith('.fna.gz'):
            sample_id = filename.split('.')[0] 
            if sample_id in sample_id_mapping:
                destination_dir = removeddir
                source_path = os.path.join(fastasdir, filename)
                destination_path = os.path.join(destination_dir, filename)

                os.makedirs(destination_dir, exist_ok=True)

                # Move the file to the destination directory
                shutil.move(source_path, destination_path)
                print(f"Moved {filename} to {destination_dir}")

    # Create the file to indicate completion
    with open("fastas_moved.txt", "w") as completion_file:
        completion_file.write("File moving completed\n")

    print("File moving completed.")

