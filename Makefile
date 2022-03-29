test:
	mypy .
	black --check easy_scraper/
	python -m pytest -vvv ./tests

publish:
	poetry build
	poetry publish
