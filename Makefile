install:
#	python3 -m pip install --upgrade pip
#	python3 -m pip install -e .
	#python3 install_menu.py
	pipx install -e .
#wheel: requirements.txt
#	python3 -m build --wheel
#requirements.txt: Pipfile.lock
#	pipenv requirements > requirements.txt