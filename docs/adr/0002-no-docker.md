# Deploy without Docker

Sayd is one app, one Postgres database and a reverse proxy on a single VPS, run by one person, so we skip containers. Postgres comes from the OS package manager, the app runs from a virtual environment under systemd, Caddy provides TLS, and cron calls the command-line entry point from the same virtual environment. We accept a less reproducible server in exchange for fewer moving parts and nothing extra to learn or debug. This reverses the Docker Compose decision first written in the spec (#1).
