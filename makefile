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

freeze:
	pip freeze > requirements.txt
load:
	python src/load_data.py

validate:
	python src/validate_data.py

db:
	python src/create_db.py

test:
	pytest tests/
