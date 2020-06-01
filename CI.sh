#!/bin/bash
export FLASK_APP=backend
export FLASK_ENV=development
echo "PROSPECTOR:"
prospector -0 backend
echo "BANDIT:"
bandit -r backend
echo "PYTEST:"
pytest -v
