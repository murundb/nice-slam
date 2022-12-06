import os
import sys
import click

import numpy as np

from PIL import Image

def rename_depths(input_dir, output_dir):
    depth_count = 0

    for depth_file in sorted(os.listdir(input_dir)):
        input_file = os.path.join(input_dir, depth_file)
        filename = str(depth_count) + ".png"
        output_file = os.path.join(output_dir, filename)

        img = Image.open(input_file)
        img.save(output_file)

        depth_count += 1

@click.command()
@click.option("--input-dir", "-i", required=True, type=str, help="Input dir containing depth images")
@click.option("--output-dir", "-o", required=False, type=str, help="Output directory to save converted depth")
def main(input_dir, output_dir="depth"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(input_dir):
        sys.exit("Input file doesn't exist")
    
    rename_depths(input_dir, output_dir)

if __name__ == "__main__":
    main()