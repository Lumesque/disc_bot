.RECIPEPREFIX = %

unit_tests: ## Runs the unit tests for pytest
%	@echo "$(PWD)"
%	(source ../bot_env/bin/activate)
%	(pytest -v -s disc_bot/tests/unit_tests)

test:
%	@echo "$(PWD)"
