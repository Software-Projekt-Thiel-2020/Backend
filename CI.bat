set FLASK_APP=backend
set FLASK_ENV=development
set DB_TESTING=1
echo "PROSPECTOR:"
prospector -0 backend
echo "BANDIT:"
bandit -r backend
echo "PYTEST:"
pytest -v
set DB_TESTING=
