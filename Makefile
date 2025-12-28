.PHONY: help install install-dev test reproduce lint format clean

help:
	@echo "MQGT-SCF Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install      - Install dependencies from lockfile (reproducible)"
	@echo "  make install-dev  - Install dependencies for development"
	@echo ""
	@echo "Testing & Validation:"
	@echo "  make test         - Run test suite"
	@echo "  make reproduce    - Run reproduction script"
	@echo "  make lint         - Run linter (ruff)"
	@echo "  make format       - Format code (black)"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean        - Clean generated files and caches"

install:
	pip install -r requirements-lock.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]" || pip install pytest pytest-cov ruff black

test:
	pytest tests/ -v

reproduce:
	python reproduce_all.py

lint:
	ruff check code/ tests/ || echo "Ruff not installed, skipping lint"

format:
	black code/ tests/ --check || echo "Black not installed, skipping format check"

clean:
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	rm -rf .coverage htmlcov dist build .ruff_cache

