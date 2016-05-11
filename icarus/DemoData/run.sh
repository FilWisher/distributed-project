#!/bin/sh

# Enable command echo
set -v

# Directory where this script is located
CURR_DIR=`pwd`

# Icarus main folder
ICARUS_DIR=${CURR_DIR}/..

# Config file
CONFIG_FILE=${CURR_DIR}/config.py

# FIle where results will be saved
RESULTS_FILE=${CURR_DIR}/results.json

# Add Icarus code to PYTHONPATH
export PYTHONPATH=${ICARUS_DIR}:$PYTHONPATH

# Run experiments
echo "Run experiments"
python ${ICARUS_DIR}/icarus.py --results ${RESULTS_FILE} ${CONFIG_FILE}

#cleanup results file for visualisation
python ${ICARUS_DIR}/scripts/event_cleanup.py ${RESULTS_FILE}

python ${CURR_DIR}/streamToRequestFile.py ${RESULTS_FILE}


