#!/bin/bash

# Apply database migrations
python manage.py migrate

# Run your custom management command
python manage.py generate_teams_grid

# Start the server
gunicorn backend.wsgi  --log-file -
