install:
	python3 python/install_all_shortcuts.py

save-venv:
	pip freeze > requirements.txt