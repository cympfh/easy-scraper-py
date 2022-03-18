test:
	mypy .
	python -m pytest -vvv ./tests
