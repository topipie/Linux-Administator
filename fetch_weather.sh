#!/bin/bash
cd /home/ubuntu/cron_assignment

VENV_DIR="venv"

# Luo virtuaaliympäristö jos se puuttuu
if [ ! -d "$VENV_DIR" ]; then
    echo "Luodaan virtuaaliympäristö..."
    python3 -m venv $VENV_DIR
fi

# Aktivoi venv
source $VENV_DIR/bin/activate

# Asenna riippuvuudet
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Suorita python-skripti
python fetch_weather.py

echo "Valmis!"
