import os
import shutil

shovill = "out/shovill"
data = "data/fastas"

for root, dirs, files in os.walk(shovill):
    for filename in files:
        if filename == 'contigs.fa':
            dir_name = os.path.basename(root)
            source_file = os.path.join(root, filename)
            destination_file = os.path.join(data, f'{dir_name}.fasta')

            # Check if the source file exists before moving
            if os.path.exists(source_file):
                shutil.move(source_file, destination_file)
                print(f"Moved: {source_file} to {destination_file}")
            else:
                print(f"Source file does not exist: {source_file}")
