# Contributing to DataFlow Toolkit

First off, thank you for considering contributing to DataFlow Toolkit! It's people like you that make DataFlow Toolkit such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include logs and error messages

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these beginner and help-wanted issues:

* [Beginner issues](https://github.com/dataflow-toolkit/dataflow-toolkit/labels/good%20first%20issue)
* [Help wanted issues](https://github.com/dataflow-toolkit/dataflow-toolkit/labels/help%20wanted)

### Pull Requests

1. Fork the repo and create your branch from `develop`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/your-username/dataflow-toolkit.git
cd dataflow-toolkit
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -e ".[dev]"
pre-commit install
```

4. Create a branch:
```bash
git checkout -b feature/your-feature-name
```

## Development Process

1. **Write Code**: Follow the coding standards below
2. **Write Tests**: Ensure your code is tested
3. **Run Tests**: `make test`
4. **Lint Code**: `make lint`
5. **Format Code**: `make format`
6. **Commit**: Use conventional commits
7. **Push**: Push to your fork
8. **Create PR**: Open a pull request

## Coding Standards

### Python Style Guide

We follow PEP 8 with the following modifications:
* Line length: 100 characters
* Use Black for formatting
* Use isort for import sorting

### Docstrings

All public modules, functions, classes, and methods should have docstrings:

```python
def process_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Process data according to configuration.
    
    Args:
        df: Input DataFrame to process
        config: Processing configuration
            - transform_type: Type of transformation
            - parameters: Transformation parameters
    
    Returns:
        Processed DataFrame
    
    Raises:
        ValueError: If configuration is invalid
        ProcessingError: If processing fails
    """
```

### Type Hints

Use type hints for all function signatures:

```python
from typing import Dict, List, Optional, Union

def connect(
    host: str,
    port: int = 5432,
    database: Optional[str] = None,
    **kwargs: Any
) -> Connection:
    ...
```

### Testing

* Write unit tests for all new functionality
* Maintain test coverage above 80%
* Use pytest for testing
* Mock external dependencies

Example test:

```python
def test_process_data_success():
    """Test successful data processing."""
    # Arrange
    df = pd.DataFrame({'a': [1, 2, 3]})
    config = {'transform_type': 'scale', 'factor': 2}
    
    # Act
    result = process_data(df, config)
    
    # Assert
    assert len(result) == 3
    assert result['a'].tolist() == [2, 4, 6]
```

## Commit Messages

We use [Conventional Commits](https://www.conventionalcommits.org/):

* `feat:` New feature
* `fix:` Bug fix
* `docs:` Documentation only changes
* `style:` Code style changes (formatting, etc)
* `refactor:` Code change that neither fixes a bug nor adds a feature
* `perf:` Performance improvement
* `test:` Adding missing tests
* `chore:` Changes to the build process or auxiliary tools

Examples:
```
feat: add PostgreSQL connector
fix: handle connection timeout in S3 connector
docs: update installation guide
test: add unit tests for YAML parser
```

## Review Process

1. **Automated Checks**: CI must pass
2. **Code Review**: At least one maintainer approval
3. **Testing**: Manual testing for significant changes
4. **Documentation**: Updated if needed
5. **Merge**: Squash and merge to `develop`

## Release Process

1. Features are developed in feature branches
2. PRs are merged to `develop`
3. Release candidates are created from `develop`
4. After testing, releases are merged to `main`
5. Tags are created for releases

## Questions?

Feel free to open an issue with your question or reach out on our [Discord server](https://discord.gg/dataflow-toolkit).

Thank you for contributing! 🎉
