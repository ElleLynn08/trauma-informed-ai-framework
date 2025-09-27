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

.PHONY: dev extras all-deps test clean notebook run-nb run-all strip freeze

# Defaults used by run-nb/run-all
NB_DIR ?= notebooks
TIMEOUT ?= 600

# ------------------------------
# Setup commands
# ------------------------------

# dev: Install base, reproducible dependencies for notebooks, tests, and core pipeline.
# Why: Keeps CI and collaborators on the same baseline environment.
dev:
	pip install -r requirements.txt

# extras: Install optional, heavy, or interactive dependencies (embeddings/audio/widgets/etc).
# Why: Let contributors opt-in to large or optional stacks without bloating the base env.
extras:
	pip install -r requirements-extras.txt

# all-deps: Bootstrap both base + extras in one shot by chaining dev and extras.
# Why: Convenience for local development machines where you want everything.
all-deps: dev extras


# ------------------------------
# Workflow commands
# ------------------------------

# test: Run unit tests quietly with pytest.
# Why: Fast signal that the core code path and interfaces still behave as expected.
test:
	pytest -q

# clean: Remove Python cache folders that can confuse editors or tests.
# Why: Prevents stale bytecode or cached test artifacts from masking real issues.
clean:
	rm -rf __pycache__ .pytest_cache

# notebook: Launch JupyterLab inside the active venv.
# Why: Standard entry point for interactive exploration and report notebooks.
notebook:
	jupyter lab

# run-nb: Execute a single notebook in-place with a timeout (provide NB=path/to.ipynb).
# Why: Make notebooks machine-checkable and reproducible; catches hidden state issues.
# Example: make run-nb NB=$(NB_DIR)/03_feature_engineering_multimodal.ipynb
run-nb:
	@if [ -z "$(NB)" ]; then echo "Please provide NB=path/to/notebook.ipynb"; exit 2; fi
	PYTHONPATH="$(PWD)/src:$(PYTHONPATH)" jupyter nbconvert --to notebook --inplace --ExecutePreprocessor.timeout="$(TIMEOUT)" --execute "$(NB)"

# run-all: Execute every notebook under NB_DIR (skips those starting with "_").
# Why: Pre-push guardrail that all analysis is reproducible end-to-end.
# Note: Delegates to scripts/run_all_notebooks.sh for clarity and filtering.
run-all:
	NB_DIR="$(NB_DIR)" TIMEOUT="$(TIMEOUT)" PYTHONPATH="$(PWD)/src:$(PYTHONPATH)" bash scripts/run_all_notebooks.sh

# strip: Remove all cell outputs from notebooks (keeps code/markdown intact).
# Why: Privacy (no accidental data leakage), small diffs, fewer merge conflicts, public-repo friendly.
strip:
	@command -v nbstripout >/dev/null 2>&1 || { echo "Installing nbstripout..."; pip install nbstripout; }
	find "$(NB_DIR)" -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" -print0 | xargs -0 -I{} nbstripout "{}" || true

# freeze: Write the fully-resolved environment to requirements-lock.txt.
# Why: Capture an exact, shareable snapshot for archival or paper replication.
freeze:
	pip freeze > requirements-lock.txt
