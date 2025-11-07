# ==========================
#  Makefile - Triangulator
# ==========================

VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
RUFF = $(VENV)/bin/ruff
COVERAGE = $(VENV)/bin/coverage
PDOC = $(VENV)/bin/pdoc3

REQ    := $(if $(wildcard requirements.txt),requirements.txt,../requirements.txt)
DEVREQ := $(if $(wildcard dev_requirements.txt),dev_requirements.txt,../dev_requirements.txt)

.PHONY: install test unit_test perf_test coverage lint doc clean clean_venv check_files

check_files:
	@if [ ! -f "$(REQ)" ]; then echo "❌ Missing $(REQ)"; exit 1; fi
	@if [ ! -f "$(DEVREQ)" ]; then echo "❌ Missing $(DEVREQ)"; exit 1; fi

$(VENV)/bin/python:
	@echo "📦 Creating virtualenv in $(VENV)"
	@python3 -m venv $(VENV)
	@$(PYTHON) -m pip install -U pip

install: check_files $(VENV)/bin/python
	@echo "📦 Installing deps from $(REQ) and $(DEVREQ)"
	@$(PIP) install -r $(REQ) -r $(DEVREQ)
	@echo "✅ Virtualenv ready."

test: install
	@echo "🚀 Running all tests..."
	@$(PYTEST) -v

unit_test: install
	@$(PYTEST) -m "not perf" -v

perf_test: install
	@$(PYTEST) -m perf -v

coverage: install
	@$(COVERAGE) run -m pytest
	@$(COVERAGE) report -m

lint: install
	@$(RUFF) check .

doc: install
	@$(PDOC) --html src/triangulator -o docs --force

clean:
	@rm -rf __pycache__ .pytest_cache .coverage

clean_venv:
	@rm -rf $(VENV)
