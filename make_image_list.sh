#!/bin/bash

# Define the target directory and output file
TARGET_DIR="/g/data/jk72/jl0818/DATA/miz_voyage/Sentinel-1/L1"
OUTPUT_FILE="./image_lists/S1_image_list.txt"

OUTPUT_FILE_2025="./image_lists/S1_image_list_2025.txt"
OUTPUT_FILE_2024="./image_lists/S1_image_list_2024.txt"
OUTPUT_FILE_2023="./image_lists/S1_image_list_2023.txt"
OUTPUT_FILE_2022="./image_lists/S1_image_list_2022.txt"


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

> "$OUTPUT_FILE_2025"
cat $OUTPUT_FILE | grep "_2025" >> $OUTPUT_FILE_2025

> "$OUTPUT_FILE_2024"
cat $OUTPUT_FILE | grep "_2024" >> $OUTPUT_FILE_2024

> "$OUTPUT_FILE_2023"
cat $OUTPUT_FILE | grep "_2023" >> $OUTPUT_FILE_2023

> "$OUTPUT_FILE_2022"
cat $OUTPUT_FILE | grep "_2022" >> $OUTPUT_FILE_2022
