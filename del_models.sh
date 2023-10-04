#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR=$SCRIPT_DIR

# read variables from path.env
source ${ROOT_DIR}/path.env
delete_files_in_dirs() {
    # Loop over each directory provided in the array
    for DIR in "$@"; do

        # Check if the provided path is a directory
        if [ ! -d "$DIR" ]; then
            echo "Warning: $DIR is not a directory."
            continue  # Skip to the next directory
        fi

        # Delete all files in the directory
        find "$DIR" -type f -exec rm -f {} \;

        echo "All files in $DIR have been deleted."

    done
}

# Example usage:
DIRS=(
    ./client/client1/models/local
    ./client/client1/models/recv
    ./client/client2/models/local
    ./client/client2/models/recv
    ./client/client3/models/local
    ./client/client3/models/recv
    ./client/client1/importer
    ./client/client2/importer
    ./client/client3/importer
)
rm ./client/model.txt
rm ./src/ML/*.keras
rm ./client/out.*
delete_files_in_dirs "${DIRS[@]}"

ssh ${PARTY1_PATH} "cd ${PROJECT_DIR}; rm tdbhdf5/DS1/*"
ssh ${PARTY2_PATH} "cd ${PROJECT_DIR}; rm tdbhdf5/DS1/*"
ssh ${PARTY3_PATH} "cd ${PROJECT_DIR}; rm tdbhdf5/DS1/*"
