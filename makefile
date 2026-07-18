install:
	pip install -r requirements.txt

run:
	python main.py

test:
	pytest

format:
	black .

lint:
	flake8 .

sort:
	isort .
db:
	python database/nifty100.db

freeze:
	pip freeze > requirements.txt

load:
	python -m src.ETL.loader

validation:
	python -m src.validators.run_validation

analytics:
	python -m src.analytics.run_analytics

test-loader:
	pytest tests/tests_loader.py

test-ratios:
	pytest tests/tests_ratios.py 


