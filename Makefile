SHELL := /bin/bash
# ------------------------------
# Makefile (developer shortcuts)
# ------------------------------
# Usage: from the project root (with your venv active), run:
#   make dev        -> install base requirements
#   make extras     -> install optional heavy deps (embeddings/audio)
#   make test       -> run pytest test suite
#   make clean      -> remove Python cache folders
#   make notebook   -> launch JupyterLab in this repo
#   make run-nb NB=path/to/notebook.ipynb  -> execute a single notebook in-place
#   make run-all    -> execute ALL notebooks in notebooks/ (skips those starting with "_")
#   make strip      -> strip outputs from all notebooks (nbstripout)
#   make freeze     -> export a pinned requirements lock file
#
# Note: These commands operate in the active virtual environment.
# Ensure the prompt shows your venv (e.g., (.venv)) before running `make`.
#
.PHONY: dev extras test clean notebook run-nb run-all strip freeze

# Directory that holds notebooks (customize as needed)
NB_DIR ?= notebooks

# Execution timeout (seconds) for each notebook cell during run-nb/run-all
TIMEOUT ?= 600

# ------------------------------
# Setup commands
# ------------------------------

# Install base requirements (from requirements.txt) into the active venv
dev:
	pip install -r requirements.txt

# Install heavy/optional deps (embeddings, audio, prosody)
extras:
	pip install -r requirements-extras.txt

# ------------------------------
# Workflow commands
# ------------------------------

# Run unit tests with pytest (quiet output)
test:
	pytest -q

# Clean cache folders safely
clean:
	rm -rf __pycache__ .pytest_cache

# Launch JupyterLab using the venv's jupyter
notebook:
	jupyter lab

# Execute a single notebook in-place.
# Example: make run-nb NB=notebooks/03_feature_engineering_multimodal.ipynb
run-nb:
	@if [ -z "$(NB)" ]; then echo "Please provide NB=path/to/notebook.ipynb"; exit 2; fi
	jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout="$(TIMEOUT)" --execute "$(NB)"

# Execute ALL notebooks in NB_DIR, skipping those that start with "_".
# Uses the helper script in scripts/run_all_notebooks.sh for clarity.
run-all:
	NB_DIR="$(NB_DIR)" TIMEOUT="$(TIMEOUT)" bash scripts/run_all_notebooks.sh

# Strip outputs from all notebooks to keep diffs clean (requires nbstripout)
strip:
	@command -v nbstripout >/dev/null 2>&1 || { echo "Installing nbstripout..."; pip install nbstripout; }
	nbstripout $(NB_DIR)/*.ipynb || true

# Export current fully-resolved package versions to requirements-lock.txt
freeze:
	pip freeze > requirements-lock.txt


