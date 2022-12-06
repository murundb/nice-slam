import os
import sys
import click

import numpy as np

from PIL import Image

def rename_images(input_dir, output_dir):
    image_count = 0

    for img_file in sorted(os.listdir(input_dir)):
        input_file = os.path.join(input_dir, img_file)
        filename = str(image_count) + ".jpg"
        output_file = os.path.join(output_dir, filename)

        img = Image.open(input_file)
        img.save(output_file)

        image_count += 1


@click.command()
@click.option("--input-dir", "-i", required=True, type=str, help="Input dir containing images")
@click.option("--output-dir", "-o", required=False, type=str, help="Output directory to save converted images")
def main(input_dir, output_dir="color"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(input_dir):
        sys.exit("Input file doesn't exist")
    
    rename_images(input_dir, output_dir)

if __name__ == "__main__":
    main()