all : black mypy isort flake8 pytest

.PHONY: black
black:
	black --check hap tests bin/*

.PHONY: mypy
mypy:
	mypy hap tests bin/*

.PHONY: isort
isort:
	isort --check-only hap tests bin/*

.PHONY: flake8
flake8:
	flake8 hap tests bin/*

.PHONY: pytest
pytest:
	pytest
