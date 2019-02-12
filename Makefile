build:
	docker-compose build

build-test:
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build

run:
	docker-compose run --rm wordcounter python main.py

help:
	docker-compose run --rm wordcounter python main.py -h

lint:
	echo "==> Building test environment..."
	$(MAKE) build-test
	echo "==> Formatting code..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter black .
	echo "==> Sorting python imports..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter isort --recursive --apply .
	echo "==> Linting..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter pylint .

test:
	echo "==> Building test environment..."
	$(MAKE) build-test
	echo "==> Running tests..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter pytest --cov=. --cov-report=term-missing --no-cov-on-fail $(args)
	echo "==> Checking code format..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter black --check .
	echo "==> Checking the order of python imports..."
	docker-compose -f docker-compose.yml -f docker-compose.test.yml run --rm wordcounter isort --recursive --check-only .