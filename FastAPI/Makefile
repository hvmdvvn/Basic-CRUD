.PHONY: run test lint format install

# Run the app
run:
	uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Run tests
test:
	pytest -v --maxfail=1 --disable-warnings -q

# Code formatting with black
format:
	black .

# Linting with flake8
lint:
	flake8 .

# Install dependencies
install:
	pip install -r requirements.txt
