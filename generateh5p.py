# Author: Thivin Anandh
import argparse
import copy
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from os import listdir
from os.path import isfile, join


def run_cmd(command, cwd=None):
    """Run a shell command safely and exit on failure."""
    result = subprocess.run(command, cwd=cwd, shell=False)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(command)}")
        sys.exit(1)


def parse_arguments():
    """Parse CLI arguments using argparse."""
    parser = argparse.ArgumentParser(
        description="Convert PDF slides into an H5P package."
    )

    # First positional argument → Mandatory PDF file
    parser.add_argument(
        "input_pdf",
        type=str,
        help="Name of the PDF file to convert (mandatory)."
    )

    # Optional keyword arguments
    parser.add_argument(
        "--dpi",
        type=int,
        default=600,
        help="DPI for PDF to image conversion (default: 600)."
    )
    parser.add_argument(
        "--resolution",
        type=int,
        default=1920,
        help="Image resolution width in pixels (default: 1920)."
    )
    parser.add_argument(
        "--webOutput",
        type=str,
        default=".",
        help="Output directory for the generated H5P package (default: current directory)."
    )

    args = parser.parse_args()

    # Ensure the first positional argument (PDF) exists
    if not os.path.isfile(args.input_pdf):
        print(f"[ERROR] PDF file not found: {args.input_pdf}")
        sys.exit(1)

    return args


def prepare_directories(content_path, image_path):
    """Remove old content folder and create fresh directories."""
    if os.path.exists(content_path) and os.path.isdir(content_path):
        shutil.rmtree(content_path)
    os.makedirs(image_path, exist_ok=True)


def extract_images(input_pdf, dpi, resolution, image_path, title):
    """Extract PDF pages as PNG images using pdftoppm."""
    cmd = [
        "pdftoppm", "-png",
        "-r", str(dpi),
        "-scale-to", str(resolution),
        input_pdf,
        f"image-{title}"
    ]
    run_cmd(cmd, cwd=image_path)


def rename_images(image_path):
    """Rename extracted images with unique hashes."""
    image_files = [f for f in listdir(image_path) if isfile(join(image_path, f))]
    renamed_images = []

    for img in image_files:
        unique_id = str(uuid.uuid4())[:8]
        filename, ext = os.path.splitext(img)
        new_name = f"{filename}-{unique_id}{ext}"
        shutil.move(f"{image_path}/{img}", f"{image_path}/{new_name}")
        renamed_images.append(new_name)

    renamed_images.sort()
    return renamed_images


def generate_h5p(args):
    """Main conversion logic."""
    home_dir = os.getcwd()
    content_path = os.path.join(home_dir, "content")
    image_path = os.path.join(content_path, "images")
    input_pdf = args.input_pdf
    output_name = Path(input_pdf).stem

    # Load base content.json
    with open(f"{home_dir}/contentBase/content.json", "r") as f:
        json_data = json.load(f)

    # Copy one base slide and remove existing slides
    slide_template = copy.deepcopy(json_data['presentation']['slides'][0])
    del json_data['presentation']['slides'][0]

    # Prepare folders
    prepare_directories(content_path, image_path)

    # Copy PDF to images folder
    shutil.copy(input_pdf, image_path)

    # Extract images from PDF
    extract_images(input_pdf, args.dpi, args.resolution, image_path, output_name)

    # Delete copied PDF after conversion
    os.remove(f"{image_path}/{Path(input_pdf).name}")

    # Rename extracted images
    renamed_images = rename_images(image_path)

    # Prepare new template folder
    run_cmd(["cp", "-r", f"{home_dir}/BaseTemplate/", output_name])

    # Add a slide for each image
    for image in renamed_images:
        curr_slide = copy.deepcopy(slide_template)
        curr_slide['elements'][0]['action']['params']['file']['path'] = f"images/{image}"
        curr_slide['elements'][0]['action']['subContentId'] = str(uuid.uuid4())
        json_data['presentation']['slides'].append(curr_slide)

    # Write updated content.json
    with open(f"{content_path}/content.json", "w") as f:
        json.dump(json_data, f, indent=4)

    # Copy content to output folder
    run_cmd(["cp", "-r", content_path, f"{output_name}/"])

    # Create .h5p archive
    shutil.make_archive(output_name, "zip", output_name)
    run_cmd(["mv", f"{output_name}.zip", f"{output_name}.h5p"])

    # Clean up temporary folders
    shutil.rmtree(output_name)

    # Move final file to webOutput
    shutil.move(f"{output_name}.h5p", os.path.join(args.webOutput, f"{output_name}.h5p"))

    print(f"[SUCCESS] {output_name}.h5p successfully generated!")


def main():
    args = parse_arguments()
    generate_h5p(args)


if __name__ == "__main__":
    main()
