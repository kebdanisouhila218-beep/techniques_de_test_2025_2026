.PHONY: test unit_test perf_test coverage lint doc

test:
	pytest

unit_test:
	pytest -m "not performance"

perf_test:
	pytest -m performance

coverage:
	coverage run -m pytest -m "not performance"
	coverage report
	coverage html

lint:
	ruff check .

doc:
	pdoc3 triangulator --html --output-dir docs