#!/bin/bash

# example command: ./run_script.sh ../src/SecreC/bank1.sc
set -e

# Get the absolute file path of the script
SCRIPT_PATH=$(dirname $(realpath $0))
PROJECT_PATH="${SCRIPT_PATH%%/client}"

# read variables from path.env
source ${PROJECT_PATH}/path.env

# User input for client number and file name
# Initialize the values to an empty string
CLIENT=""
FILENAME=""

# Use getopts to process command-line options
while getopts ":c:f:" opt; do
  case ${opt} in
    c)
      CLIENT="$OPTARG"
      ;;
    f)
      FILENAME="$OPTARG"
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

if [ -z "$FILENAME" ]; then
  echo "-f is required."
  exit 1
fi

CLIENT="client"$CLIENT

# remove the file extension if included
FILENAME="${FILENAME%.*}"

if [ "x${SHAREMIND_INSTALL_PATH}" = "x" ]; then
    SHAREMIND_INSTALL_PATH="/usr"
fi

echo "Using SHAREMIND_INSTALL_PATH='${SHAREMIND_INSTALL_PATH}'"

SCC="${SHAREMIND_INSTALL_PATH}/bin/scc"
SHAREMIND_RUNSCRIPT="${SHAREMIND_INSTALL_PATH}/bin/sharemind-runscript"

CONF_PATH=$SCRIPT_PATH"/"$CLIENT"/"$CLIENT".cfg"
SC=$PROJECT_PATH"/src/SecreC/"$FILENAME".sc"

if [ ! -e "${SC}" ]; then
    echo "File '${SC}' does not exist" && false
fi

SC_ABSS=`readlink -f "${SC}"`

[ -f "${SC_ABSS}" ]

SC_ABSSP=`dirname "${SC_ABSS}"`
SC_BN=`basename "${SC}"`
SB_BN=`echo "${SC_BN}" | sed 's/sc$//' | sed 's/$/sb/'`
STDLIB="${SHAREMIND_INSTALL_PATH}/lib/sharemind/stdlib"
SB=`mktemp -t "${SB_BN}.XXXXXXXXXX"`

echo "Compiling: '${SC}' to '${SB}'"
"${SCC}" --include "${STDLIB}" --include "${SC_ABSSP}" --input "${SC}" --output "${SB}"


# cp to servers
# for i in 1 2 3
# do
#   echo "Installing: '${SB}' to '${PROJECT_PATH}/server/server${i}/programs/${SB_BN}'"
#   scp "${SB}" "${PARTY1_PATH}:/${PROJECT_DIR}/programs/${SB_BN}"
# done

# cp to servers
echo "Installing: '${SB}' to '${PARTY1_PATH}:/${PROJECT_DIR}/programs/${SB_BN}'"
scp "${SB}" "${PARTY1_PATH}:/${PROJECT_DIR}/programs/${SB_BN}"
echo "Installing: '${SB}' to '${PARTY1_PATH}:/${PROJECT_DIR}/programs/${SB_BN}'"
scp "${SB}" "${PARTY2_PATH}:/${PROJECT_DIR}/programs/${SB_BN}"
echo "Installing: '${SB}' to '${PARTY1_PATH}:/${PROJECT_DIR}/programs/${SB_BN}'"
scp "${SB}" "${PARTY3_PATH}:/${PROJECT_DIR}/programs/${SB_BN}"



rm -f "${SB}"

TXT_PATH=$PROJECT_PATH/client/model.txt
OUT_INIT=$PROJECT_PATH/client/out.init
OUT_GLOBAL=$PROJECT_PATH/client/out.global
PY_PATH=$PROJECT_PATH"/venv/bin/python"
PY_DECIPHER=$PROJECT_PATH"/src/ML/argument-stream-decipher.py"
PY_CSV=$PROJECT_PATH"/src/ML/published_to_csv.py"

echo "Running: '${SB}'"

# Get the number of layers from model.txt (by counting | + 1)
NLayers=$(grep -o '|' $TXT_PATH| wc -l)
NLayers=$((NLayers + 1))

# For the details: https://github.com/sharemind-sdk/emulator/blob/master/doc/sharemind-emulator.h2m
case $FILENAME in
init)
  LD_PRELOAD=/lib/x86_64-linux-gnu/libstdc++.so.6 "${SHAREMIND_RUNSCRIPT}" "${SB_BN}" --conf "${CONF_PATH}" --str=model --str= --str=string --file=$TXT_PATH --outFile=$OUT_INIT -f
  $PY_PATH $PY_DECIPHER $OUT_INIT | $PY_PATH $PY_CSV /dev/stdin $FILENAME
;;
agg)
  LD_PRELOAD=/lib/x86_64-linux-gnu/libstdc++.so.6 "${SHAREMIND_RUNSCRIPT}" "${SB_BN}" --conf "${CONF_PATH}" --str=nlayers --str= --str=uint64 --size=8 --uint64=$NLayers --str=nclients --str= --str=uint64 --size=8 --uint64=3
;;
global)
  LD_PRELOAD=/lib/x86_64-linux-gnu/libstdc++.so.6 "${SHAREMIND_RUNSCRIPT}" "${SB_BN}" --conf "${CONF_PATH}" --str=nlayers --str= --str=uint64 --size=8 --uint64=$NLayers --outFile=$OUT_GLOBAL -f
  $PY_PATH $PY_DECIPHER $OUT_GLOBAL | $PY_PATH $PY_CSV /dev/stdin $FILENAME
;;
esac
