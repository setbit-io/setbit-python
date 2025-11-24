.PHONY: install test lint format clean build publish

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v

test-cov:
	pytest tests/ --cov=setbit --cov-report=html --cov-report=term

lint:
	flake8 setbit tests
	mypy setbit

format:
	black setbit tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

publish: build
	twine upload dist/*

publish-test: build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
