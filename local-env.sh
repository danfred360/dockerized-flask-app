#!/bin/bash

export FLASK_APP=app

alias p-run="source venv/bin/activate && export FLASK_ENV=development && flask run"
alias p-run-public="source venv/bin/activate && flask run --host=0.0.0.0"
