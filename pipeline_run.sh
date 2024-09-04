#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 -i input_path -p prompt [-o output_dir]"
    echo "  - input_path can be either a directory of images or a single image file."
    exit 1
}

# Parse command-line arguments
while getopts ":i:p:o:" opt; do
    case ${opt} in
        i )
            input_path=$OPTARG
            ;;
        p )
            prompt=$OPTARG
            ;;
        o )
            output_dir=$OPTARG
            ;;
        \? )
            usage
            ;;
    esac
done

# Check if input_path and prompt are provided
if [ -z "$input_path" ] || [ -z "$prompt" ]; then
    usage
fi

# Set default output directory if not provided
if [ -z "$output_dir" ]; then
    # Use the input path name for the output directory (without extension for files)
    base_name=$(basename "$input_path")
    output_dir="output_${base_name%.*}"
fi

# Create the output directory if it doesn't exist
mkdir -p "$output_dir"

# Check if the input path is a directory or a single file
if [ -d "$input_path" ]; then
    # Step 1: Run OCR on all images inside the input directory
    echo "Running OCR on images in directory: $input_path"
    python paddleocr_demo.py -i "$input_path" -o "$output_dir"
elif [ -f "$input_path" ]; then
    # Step 1: Run OCR on the single image file
    echo "Running OCR on the image file: $input_path"
    python paddleocr_demo.py -i "$input_path" -o "$output_dir"
else
    echo "Error: $input_path is not a valid file or directory."
    exit 1
fi

# Step 2: Run ollama_rag.py with the OCR output directory and specified prompt
echo "Running ollama_rag.py with OCR output directory: $output_dir"
python ollama_rag.py --dir "$output_dir" -p "$prompt"

echo "Process completed successfully."
