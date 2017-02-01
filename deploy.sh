#!/bin/bash
export LC_ALL=C
apt-get update
apt-get install -y python-pip python-dev postgresql-client httperf psutil python-mysqldb python-psycopg2
pip install Flask Flask-SQLAlchemy
pip install -r requirements.txt

sudo -u postgres psql -c "create user usuario with password 'root00';"
sudo -u postgres psql -c "create database db owner usuario encoding 'utf-8';"
python app.py
