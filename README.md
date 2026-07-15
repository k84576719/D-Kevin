# D-Kevin

A small **Flask + MySQL** full-stack demo: a guestbook where you can post a
message and read all messages. Built to bootstrap the project and validate the
deployment pipeline (gunicorn + systemd).

## Features

- Post a message (name + content) via a web form or JSON API.
- View all messages, newest first.
- JSON API at `/api/messages` (GET/POST) and a `/health` endpoint.

## Tech stack

- Python 3, [Flask](https://flask.palletsprojects.com/)
- MySQL (via [PyMySQL](https://pymysql.readthedocs.io/))
- [gunicorn](https://gunicorn.org/) for serving in production, managed by systemd

## Project layout

```
app.py                 # Flask app factory + routes
db.py                  # MySQL helpers (init table, add/list messages)
config.py              # Env-based configuration
templates/index.html   # Guestbook UI
static/style.css       # Styling
schema.sql             # Database + table DDL
deploy/d-kevin.service # systemd unit
deploy/deploy.sh       # server-side deploy helper
```

## Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then edit DB_* values
mysql -u root -p < schema.sql   # create database + table

# run the dev server
python app.py                    # http://localhost:8080
# or with gunicorn
gunicorn --bind 0.0.0.0:8080 app:app
```

Configuration is read from environment variables (see `.env.example`):
`DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.

## Deployment (gunicorn + systemd)

On the server (as root), with the code in `/opt/d-kevin`:

```bash
# 1. create the database (once)
mysql < schema.sql

# 2. configure
cp .env.example .env    # set DB_PASSWORD etc.

# 3. install + register service (installs venv, deps, systemd unit on :8080)
bash deploy/deploy.sh
```

The service listens on `0.0.0.0:8080`. To reach it from the public internet,
open port 8080 in your cloud provider's security group / firewall.
