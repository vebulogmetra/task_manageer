d-build:
	docker build -t task_mngr .
d-start:
	docker run -d -p 8000:8000 task_mngr
d-stop:
	docker stop task_mngr
d-run-tests:
	pytest -s tests/integration/