# D-Kevin

Flask + MySQL guestbook demo. See `README.md` for the full overview, local dev,
and deployment instructions.

## Cursor Cloud specific instructions

### Dev environment (this repo / workspace)

- Python app. Dependencies are in `requirements.txt`; the startup update script
  installs them into `.venv`. Activate with `source .venv/bin/activate` or call
  binaries directly (e.g. `.venv/bin/python`, `.venv/bin/gunicorn`).
- Creating the venv needs the `python3-venv` system package (installed during
  environment setup; not part of the update script).
- Run locally: `python app.py` (dev server on `:8080`) or
  `gunicorn --bind 0.0.0.0:8080 app:app`.
- DB config comes from env vars / `.env` (see `.env.example`): `DB_HOST`,
  `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`. The app auto-creates the
  `messages` table on startup but NOT the database — create it with
  `mysql < schema.sql` first. Running the app without a reachable MySQL only logs
  a startup warning; routes that touch the DB will error until MySQL is available.
- There is no MySQL in the Cursor Cloud workspace by default. To exercise DB code
  here, either install/start a local MySQL or tunnel to a remote one.

### Production server (`47.105.59.217`, Alibaba Cloud ECS)

- Reachable over SSH as `root` (password auth). App lives in `/opt/d-kevin`
  (a copy of this repo) with its own `.venv` and a server-local `.env`.
- Managed by systemd unit `d-kevin` (`deploy/d-kevin.service`), running gunicorn
  on `0.0.0.0:8080`. Use `systemctl {status,restart} d-kevin` and
  `journalctl -u d-kevin` for logs.
- MySQL 8 runs locally on `127.0.0.1:3306`. `root@localhost` uses the
  `auth_socket` plugin (no password over TCP), so the app connects with a
  dedicated user `dkevin` (`mysql_native_password`) granted on `d_kevin.*`.
  Don't point the app at `root` over TCP.
- Port 8080 is NOT reachable from the public internet (Alibaba security group
  blocks it). To view the app from a browser, use an SSH local port-forward,
  e.g. `ssh -L 8080:127.0.0.1:8080 root@47.105.59.217 -N`, then open
  `http://localhost:8080`.
- Deploy flow after code changes: copy files to `/opt/d-kevin`, then
  `bash deploy/deploy.sh` (rebuilds venv + restarts the service). Editing code
  requires a `systemctl restart d-kevin` — gunicorn is not run with `--reload`.
