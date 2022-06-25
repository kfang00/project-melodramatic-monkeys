#!/bin/bash

tmux kill-server
cd MLH
cd project-melodramatic-monkeys
git fetch && git reset origin/main --hard
python -m venv python3-virtualenv
source python3-virtualenv/bin/activate
pip install -r requirements.txt
tmux new -d -s sess
sleep 1
tmux send -t sess 'flask run --host=0.0.0.0' Enter
