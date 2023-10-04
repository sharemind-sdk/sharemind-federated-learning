#!/usr/bin/sh

FULL_PATH=$(realpath $0)
delimiter=/importer
PARENT_PATH="${FULL_PATH%%"$delimiter"*}"

# User input for client number and file name
# Initialize the values to an empty string
CLIENT=""
FILENAME=""

# Use getopts to process command-line options
while getopts ":c:" opt; do
  case ${opt} in
    c)
      CLIENT="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Check if the CLIENT is 1, 2, or 3
if [ "$CLIENT" != "1" -a "$CLIENT" != "2" -a "$CLIENT" != "3" ]; then
  echo "Invalid value for -c. It must be 1, 2, or 3."
  exit 1
fi


CLIENT="client"$CLIENT
LOCAL_MODEL_PATH="$PARENT_PATH/$CLIENT/models/local"


for file in "$LOCAL_MODEL_PATH"/*; do
    if [ -f "$file" ]; then
        name=$(basename $file)
        name="${name%%.csv}"

        LD_PRELOAD=/lib/x86_64-linux-gnu/libstdc++.so.6 sharemind-csv-importer \
            --mode overwrite \
            --csv $file \
            --model "$PARENT_PATH/$CLIENT/importer/$name.xml" \
            --separator c \
            --log "$PARENT_PATH/$CLIENT/importer/$name.log" \
            --conf "$PARENT_PATH/$CLIENT/$CLIENT.cfg" \
            --force
    fi
done
