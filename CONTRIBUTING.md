# Contributing to Code Review Assistant

Thank you for your interest in contributing to Code Review Assistant! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/LeoLLM/code-review-assistant-2/issues) to avoid duplicating existing bug reports. When creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and why it's problematic
- Include screenshots or animated GIFs if possible
- Include details about your environment:
  - OS and version
  - Python version
  - Package version
  - Any relevant configuration settings

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear and descriptive title
- Provide a detailed description of the proposed functionality
- Explain why this enhancement would be useful to users
- Specify which version you're using
- Include mock-ups or examples if applicable

### Pull Requests

- Fill in the required template
- Follow the coding standards
- Include appropriate tests
- Update documentation as needed
- Be open to feedback and be prepared to make changes to your PR
- Link the PR to any relevant issues

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/code-review-assistant-2.git
   cd code-review-assistant-2
   ```
3. Create a new branch:
   ```bash
   git checkout -b name-of-your-feature
   ```
4. Set up a development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) coding style
- Write docstrings in the [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Include type hints where appropriate
- Use meaningful variable and function names
- Keep functions focused on a single responsibility
- Maintain test coverage for new code

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR:
  ```bash
  pytest
  ```
- Include both unit tests and integration tests where appropriate
- Try to write tests that verify the behavior, not the implementation

## Documentation

- Update documentation for all new features or changes to existing functionality
- Document public API methods, classes, and modules
- Keep README and other guides up to date
- Add examples for new features

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line
- Consider starting the commit message with an applicable emoji:
  - ✨ (sparkles) for new features
  - 🐛 (bug) for bug fixes
  - 📚 (books) for documentation changes
  - ♻️ (recycle) for refactoring
  - 🧪 (test tube) for adding tests
  - 🔧 (wrench) for configuration changes

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the CHANGELOG.md with a description of the change
3. The PR must pass all CI tests before being merged
4. PR requires approval from at least one maintainer
5. For major changes, maintainers may request additional reviews

## Release Process

1. Maintainers will create releases according to [Semantic Versioning](https://semver.org/)
2. Release notes will be generated from the CHANGELOG.md entries
3. All releases will be tagged in the repository
4. Releases will be published to PyPI by maintainers

## Questions?

If you have any questions about contributing, please open an issue labeled "question" or contact one of the maintainers directly.

Thank you for contributing to Code Review Assistant!