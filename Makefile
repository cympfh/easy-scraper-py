test:
	mypy .
	python -m pytest -vvv ./tests

publish:
	pandoc README.md -o README.rst
	poetry build
	poetry publish
