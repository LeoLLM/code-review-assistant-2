# Code Review Assistant

An automated code review assistant system that provides templates and logic for standardized code reviews.

## Features

- Predefined review templates for general, security, and performance reviews
- Automated code review logic
- Issue tracking and management
- Milestone-based project planning
- Customizable review criteria
- Integration with popular version control systems

## Installation

**Prerequisites:**
- Python 3.8 or higher
- Git
- Access to GitHub API (for GitHub integration)

**Basic Installation:**
```bash
# Clone the repository
git clone https://github.com/LeoLLM/code-review-assistant-2.git
cd code-review-assistant-2

# Install dependencies
pip install -r requirements.txt

# Run initial setup
python setup.py install
```

For detailed installation instructions, see the [Installation Guide](INSTALL.md).

## Usage

1. Select the appropriate review template based on your review focus
2. Run the review logic against your codebase
3. Generate consistent, thorough code reviews
4. Track issues and improvements using the integrated issue management

### Basic Example:
```python
from code_review_assistant import ReviewAssistant

# Initialize the review assistant with a template
assistant = ReviewAssistant(template="general")

# Run a review on a specific file or directory
results = assistant.review("path/to/code")

# Output the review results
assistant.generate_report(results, output_format="markdown")
```

## Templates

This project includes several specialized review templates:
- **General code review template**: Focuses on code quality, readability, and maintainability
- **Security-focused review template**: Identifies potential security vulnerabilities  
- **Performance optimization review template**: Identifies performance bottlenecks

## Configuration

The assistant can be configured by creating a `config.yaml` file:

```yaml
templates_dir: "./templates"
output_dir: "./reviews"
github:
  token: "your-github-token"  # For GitHub integration
  owner: "repository-owner"
  repo: "repository-name"
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Similar Projects

- [SonarQube](https://www.sonarqube.org/) - Continuous inspection of code quality
- [CodeClimate](https://codeclimate.com/) - Automated code review for test coverage, maintainability and more
- [DeepSource](https://deepsource.io/) - Static analysis tool