#!/bin/bash
export FLASK_APP=backend
export FLASK_ENV=development
export DB_TESTING=1
echo "PROSPECTOR:"
prospector -0 backend
echo "BANDIT:"
bandit -r backend
echo "PYTEST:"
pytest -v
