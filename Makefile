test:
	mypy .
	python -m pytest -vvv ./tests

publish:
	poetry build
	poetry publish
