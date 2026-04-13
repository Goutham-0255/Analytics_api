#!/bin/bash

# Use the full path to the python/gunicorn inside the venv 
# instead of "sourcing" (which can be finicky in some shells)
export PATH="/opt/venv/bin:$PATH"

cd /code

# Default to 8000 if PORT/HOST aren't set
RUN_PORT=${PORT:-8000}
RUN_HOST=${HOST:-0.0.0.0}

# Start Gunicorn
exec gunicorn -k uvicorn.workers.UvicornWorker -b $RUN_HOST:$RUN_PORT main:app