.PHONY: install-dev test run

install-dev:
	python -m pip install -r backend/requirements-dev.txt

test:
	PYTHONPATH=backend python -m unittest discover -s backend/tests -p "test_*.py"

run:
	uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
