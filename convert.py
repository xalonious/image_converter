import argparse
import os
import sys
from PIL import Image, features

SUPPORTED_EXTENSIONS = [
    'png',
    'jpg',
    'jpeg',
    'bmp',
    'gif',
    'ico',
    'tiff',
    'tif',
    'eps',
    'psd',
    'pcx',
    'webp',
    'ppm',
    'pgm',
    'pbm',
    'xbm',
    'tga',
    'msp',
    'pdf',
]

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert image files to different formats.')
    parser.add_argument('-f', '--file', required=True, help='Path to the input file to be converted.')
    parser.add_argument(
        '-e', '--extension',
        required=True,
        help=f'Desired output file extension ({", ".join(SUPPORTED_EXTENSIONS)}).'
    )
    parser.add_argument('-o', '--output', required=True, help='Output file path with desired destination.')
    return parser.parse_args()

def validate_arguments(args):
    if not os.path.isfile(args.file):
        print(f"Error: The file '{args.file}' does not exist.")
        sys.exit(1)
    
    source_ext = os.path.splitext(args.file)[1].lower().lstrip('.')
    if source_ext not in SUPPORTED_EXTENSIONS:
        print(f"Error: The source file '{args.file}' is not a supported image format.")
        print(f"Supported formats are: {', '.join(SUPPORTED_EXTENSIONS)}.")
        sys.exit(1)
    
    desired_ext = args.extension.lower().lstrip('.')
    if desired_ext not in SUPPORTED_EXTENSIONS:
        print(f"Error: Unsupported extension '{args.extension}'. Supported extensions are: {', '.join(SUPPORTED_EXTENSIONS)}.")
        sys.exit(1)
    
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if output_dir and not os.path.exists(output_dir):
        print(f"Error: The directory '{output_dir}' does not exist.")
        sys.exit(1)
    

def convert_image(input_path, output_path, output_format):
    try:
        with Image.open(input_path) as img:
            print(f"Opened image: {input_path} (Format: {img.format}, Mode: {img.mode})")
            
            if output_format in ['jpg', 'jpeg'] and img.mode in ("RGBA", "P"):
                print("Converting image mode to RGB for JPEG format.")
                img = img.convert("RGB")
            
            if output_format == 'pdf':
                img.save(output_path, "PDF", resolution=100.0)
            elif output_format == 'eps':
                img.save(output_path, "EPS")
            elif output_format == 'psd':
                img.save(output_path, "PSD")
            else:
                img.save(output_path, output_format.upper())
        
        print(f"Successfully converted '{input_path}' to '{output_path}'.")
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)

def main():
    args = parse_arguments()
    validate_arguments(args)
    
    input_file = args.file
    output_file = args.output
    desired_extension = args.extension.lower().lstrip('.')
    
    output_file_ext = os.path.splitext(output_file)[1].lower().lstrip('.')
    if output_file_ext != desired_extension:
        output_file = os.path.splitext(output_file)[0] + '.' + desired_extension
    
    convert_image(input_file, output_file, desired_extension)

if __name__ == "__main__":
    main()
