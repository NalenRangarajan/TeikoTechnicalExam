make setup:
	python -m venv venv
	venv/bin/pip install -r requirements.txt
make pipeline:
	venv/bin/python load_data.py
	venv/bin/python main.py
make dashboard:
	python -m http.server 8000