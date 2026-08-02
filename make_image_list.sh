#!/bin/bash

# Define the target directory and output file
TARGET_DIR="/g/data/jk72/jl0818/DATA/miz_voyage/Sentinel-1/L1"
OUTPUT_FILE="./image_lists/S1_image_list.txt"

# Clear the output file if it already exists
> "$OUTPUT_FILE"

# Check if there are any zip files in the directory
if ls "$TARGET_DIR"/*.zip >/dev/null 2>&1; then

    # Loop through all .zip files
    for file in "$TARGET_DIR"/*.zip; do

        # Extract just the filename (remove the path)
        filename=$(basename "$file")

        # Remove the .zip extension and write to the file
        echo "${filename%.zip}" >> "$OUTPUT_FILE"

    done

    echo "Success! The list has been written to $OUTPUT_FILE."

else
    echo "No .zip files found in $TARGET_DIR."

fi
