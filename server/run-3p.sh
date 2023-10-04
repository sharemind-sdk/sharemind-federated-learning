#!/usr/bin/sh
gnome-terminal --tab -e 'sh -c "cd server1; sh run.sh"'
gnome-terminal --tab -e 'sh -c "cd server2; sh run.sh"'
gnome-terminal --tab -e 'sh -c "cd server3; sh run.sh"'
