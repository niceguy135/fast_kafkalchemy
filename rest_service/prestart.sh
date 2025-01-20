#! /usr/bin/env bash

set -e
set -x

python app/rest_prestart.py

alembic upgrade head

python app/initial_data.py
