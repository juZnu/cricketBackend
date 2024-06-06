#!/bin/bash

# Run your custom management command
python manage.py generate_teams_grid

# Apply database migrations
python manage.py migrate


# Start the server
gunicorn backend.wsgi  --log-file -
