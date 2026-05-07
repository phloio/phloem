.PHONY: install
install: ## Install the uv environment and pre-commit hooks
	@echo "🚀 Creating virtual environment using uv"
	@uv sync --all-groups
	@uv run pre-commit install

.PHONY: check
check: ## Run code quality tools (lock check, pre-commit, dep check)
	@echo "🚀 Checking uv lock file consistency with 'pyproject.toml': Running uv lock --check"
	@uv lock --check
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
	@echo "🚀 Type-checking: Running mypy"
	@uv run mypy
	@echo "🚀 Checking for obsolete dependencies: Running uv pip check"
	@uv pip check

.PHONY: test
test: ## Test the code with pytest, emit junit + coverage XML
	@echo "🚀 Testing code: Running pytest"
	@uv run pytest --cov --cov-config=pyproject.toml --cov-report=xml --junitxml=junit-test.xml

.PHONY: docs-test
docs-test: ## Build the documentation strictly (warnings = errors)
	@uv run --group docs mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation locally
	@uv run --group docs mkdocs serve

.PHONY: claude
claude: ## Start Claude Code, resuming the most recent session in this directory (or a fresh one if none)
	@claude --dangerously-skip-permissions --continue 2>/dev/null || claude --dangerously-skip-permissions

.PHONY: claude-new
claude-new: ## Start a fresh Claude Code session, ignoring any prior session in this directory
	@claude --dangerously-skip-permissions

.PHONY: docs-claude
docs-claude: ## Generate / refresh user-facing documentation using Claude
	@claude --dangerously-skip-permissions --print -p "Read .claude/CLAUDE-DOCS.md and follow the instructions"

.PHONY: claude-dev
claude-dev: ## Generate / refresh dev context for Claude sessions
	@claude --dangerously-skip-permissions --print -p "Read .claude/CLAUDE-DEV.md and follow the instructions"

.PHONY: clean
clean: ## Clean build artefacts and caches
	@rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage coverage.xml junit-*.xml dist build *.egg-info site
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
