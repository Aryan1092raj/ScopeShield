.PHONY: setup test demo bench dev api web

setup:
	pip install -r backend/requirements.txt
	cd frontend && npm install

test:
	PYTHONPATH=. python -m pytest backend/test_audit.py -q

demo:
	PYTHONPATH=. python scripts/benchmark_tinker.py

bench:
	python scripts/generate_tinker_dataset.py --n-train 250 --n-test 50
	PYTHONPATH=. python scripts/benchmark_tinker.py

api:
	uvicorn backend.main:app --port 8000 --reload

web:
	cd frontend && npm run dev
