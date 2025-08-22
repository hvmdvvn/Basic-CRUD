# Makefile for Flask Pizza Ordering API

# Variables
APP=app.py
PORT=8000
VENV?=.venv

.PHONY: help install run lint format test clean

help:
	@echo "Makefile commands:"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Run the Flask app"
	@echo "  make lint      - Lint code with flake8"
	@echo "  make format    - Format code with black"
	@echo "  make test      - Run tests with pytest"
	@echo "  make clean     - Remove cache and pyc files"

install:
	pip install -r requirements.txt

run:
	FLASK_APP=$(APP) flask run --port=$(PORT)

lint:
	flake8 .

format:
	black .

test:
	pytest -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
