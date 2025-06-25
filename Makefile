.PHONY: help install dev-install test lint format clean build docs

help:
	@echo "Available commands:"
	@echo "  install       Install the package"
	@echo "  dev-install   Install with development dependencies"
	@echo "  test          Run tests"
	@echo "  lint          Run linters"
	@echo "  format        Format code"
	@echo "  clean         Clean build artifacts"
	@echo "  build         Build package"
	@echo "  docs          Build documentation"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev,docs]"
	pre-commit install

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ -v --cov=src/dataflow_toolkit --cov-report=html --cov-report=term

lint:
	isort --check-only src tests
	black --check src tests
	flake8 src tests
	mypy src

format:
	isort src tests
	black src tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

docs:
	cd docs && make clean && make html

docker-build:
	docker build -t dataflow-toolkit:latest .

docker-run:
	docker run -it --rm dataflow-toolkit:latest
