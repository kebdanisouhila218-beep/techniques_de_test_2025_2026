test:
	pytest -v

unit_test:
	pytest -v --ignore=tests/test_performance.py

perf_test:
	pytest -v tests/test_performance.py

coverage:
	coverage run -m pytest && coverage report

lint:
	ruff check .

doc:
	pdoc3 triangulator -o docs
