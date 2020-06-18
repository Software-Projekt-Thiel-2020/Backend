set FLASK_APP=backend
set FLASK_ENV=development
echo "PROSPECTOR:"
prospector -0 backend
echo "BANDIT:"
bandit -r backend
echo "PYTEST:"
pytest -v
