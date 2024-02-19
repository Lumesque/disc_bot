.RECIPEPREFIX = %
_ENV := $(shell dirname $(PWD))
V_ENV := $(shell dirname $(PWD))/bot_env
PYTHON := $(V_ENV)/bin/python
PYTEST := $(V_ENV)/bin/pytest

prepare_venv: ## If environment does not exist, create it
	# It is crucial venv/anaconda is used, virtualenv created issues that could \
	# not allow logging to be packaged
%	@test -d ${V_ENV} && echo exit 0 ; echo "Env not found, creating..." ; \
	python -m venv ${V_ENV} ; \
	. ${V_ENV}/bin/activate ; \
	pip install --upgrade pip ; pip install -Ur requirements.txt

unit_tests: prepare_venv ## Runs the unit tests for pytest
%	$(PYTEST) -v -s disc_bot/tests/unit_tests

test:
%	@echo "$(PWD)"
