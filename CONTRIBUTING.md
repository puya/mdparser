# Contributing to mdparser

Thank you for your interest in contributing to mdparser!

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync --dev
   ```

3. Install pre-commit hooks:
   ```bash
   uv run pre-commit install
   ```

## Code Quality

This project uses:
- **Ruff** for linting and code formatting
- **pytest** for testing
- **pre-commit** hooks to ensure code quality

### Running Linters

```bash
# Check for linting errors
uv run ruff check src/ tests/

# Auto-fix linting errors
uv run ruff check --fix src/ tests/

# Format code
uv run ruff format src/ tests/
```

### Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ --cov=src/mdparser --cov-report=html
```

## Pre-commit Hooks

Pre-commit hooks automatically run before each commit to ensure:
- Code is properly formatted
- Linting passes
- Tests pass
- No trailing whitespace
- Proper file endings

To manually run pre-commit hooks:
```bash
uv run pre-commit run --all-files
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for all functions
- Keep line length to 100 characters (enforced by formatter)

## Submitting Changes

1. Make your changes
2. Ensure all tests pass: `uv run pytest tests/`
3. Ensure linting passes: `uv run ruff check src/ tests/`
4. Format code: `uv run ruff format src/ tests/`
5. Commit your changes (pre-commit hooks will run automatically)
6. Submit a pull request

