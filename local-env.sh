#!/bin/bash

export FLASK_APP=app
export PORT=5050

alias p-run="source venv/bin/activate && python3 app.py"

alias p-build-image="docker image build -t peek ."
alias p-run-image='docker run -p '"$PORT"':'"$PORT"' -d --name peek_app peek'
alias p-stop-image="docker kill peek_app && docker rm peek_app"
