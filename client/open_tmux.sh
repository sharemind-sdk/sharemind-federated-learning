#!/bin/bash

# Define the directory and source
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ROOT_DIR="${SCRIPT_DIR%%/client}"
SOURCE="venv/bin/activate"

# Start a new tmux session in detached mode
tmux new-session -d

# Split the window into 4 panes. 
# First, create a vertical split which gives two panes.
tmux split-window -h

# For the right pane, split it vertically again.
tmux select-pane -t 0
tmux split-window -v

#Now, split the last pane horizontally to create the 4th pane.
tmux select-pane -t 2
tmux split-window -v

# Now we have 4 panes. Send commands to first 3 panes to change directory and activate venv.
for pane in {1..3}; do
    tmux send-keys -t ${pane} "export CLIENT_NUMBER=$pane; cd $ROOT_DIR; source $SOURCE; sh client/show_msg.sh; bash" C-m
done

# Pane 0 just starts docker compose up
tmux send-keys -t 0 "docker compose up" C-m

# Attach to the tmux session
tmux attach
