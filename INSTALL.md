# Installation Guide

This guide provides detailed instructions for installing and configuring the Code Review Assistant on various platforms.

## System Requirements

- **Python**: Version 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.15+, or Linux (Ubuntu 18.04+, Debian 10+, CentOS 8+)
- **Disk Space**: Minimum 200MB free space
- **RAM**: Minimum 512MB (1GB+ recommended)
- **Git**: Version 2.25.0 or higher
- **Internet Connection**: Required for GitHub API integration

## Dependencies

The following Python packages are required:
- requests>=2.25.0
- pyyaml>=5.4.0
- click>=8.0.0
- jinja2>=3.0.0
- gitpython>=3.1.14

## Installation Methods

### Method 1: Standard Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LeoLLM/code-review-assistant-2.git
   cd code-review-assistant-2
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   
   On Linux/macOS:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   
   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the setup script**:
   ```bash
   python setup.py install
   ```

5. **Verify installation**:
   ```bash
   code-review-assistant --version
   ```

### Method 2: Using pip (Coming Soon)

```bash
pip install code-review-assistant
```

### Method 3: Docker Installation

1. **Pull the Docker image**:
   ```bash
   docker pull leollm/code-review-assistant:latest
   ```

2. **Run the container**:
   ```bash
   docker run -v $(pwd):/code -it leollm/code-review-assistant:latest
   ```

## Configuration

1. **Create a configuration file**:
   
   Create a file named `config.yaml` in your home directory under `.code-review-assistant/`:
   
   ```yaml
   # Basic configuration
   templates_dir: "./templates"
   output_dir: "./reviews"
   
   # GitHub integration (optional)
   github:
     token: "your-github-token"  # Generate from GitHub Developer Settings
     owner: "repository-owner"
     repo: "repository-name"
   
   # Review settings
   review:
     max_file_size: 1048576  # 1MB in bytes
     ignored_extensions: [".pyc", ".min.js", ".min.css"]
     ignored_dirs: ["node_modules", "venv", ".git"]
   ```

2. **Set up GitHub integration** (optional):
   
   a. Go to GitHub [Personal Access Tokens](https://github.com/settings/tokens)
   b. Generate a new token with the following permissions:
      - `repo` (Full control of private repositories)
      - `read:user` (Read access to user information)
   c. Copy the token to your configuration file

## Platform-Specific Instructions

### Windows

- Ensure Python is added to your PATH during installation
- For Git integration, install Git for Windows from [https://git-scm.com/download/win](https://git-scm.com/download/win)
- Consider using Windows Terminal for a better command-line experience

### macOS

- Install Python using Homebrew:
  ```bash
  brew install python
  ```
- Install Git (if not already installed):
  ```bash
  brew install git
  ```

### Linux (Ubuntu/Debian)

- Install Python and dependencies:
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv git
  ```

## Troubleshooting

### Common Issues

1. **"Command not found" error**:
   - Ensure the installation directory is in your PATH
   - Try running with the full path to the executable

2. **Import errors**:
   - Verify all dependencies are installed: `pip list | grep <package-name>`
   - Try reinstalling the package: `pip install --force-reinstall code-review-assistant`

3. **GitHub API errors**:
   - Check your token has the correct permissions
   - Verify the token is correctly set in your configuration file
   - Ensure you have internet connectivity

4. **Performance issues with large repositories**:
   - Increase the RAM allocation if using Docker
   - Consider using the `--limit-files` option to review only specific files

## Getting Help

If you encounter problems not covered in this guide:

1. Check the [GitHub Issues](https://github.com/LeoLLM/code-review-assistant-2/issues) page for similar problems
2. Open a new issue with details about your environment and the specific error
3. Join our community Discord for real-time support

## Next Steps

After installation, see the [User Guide](USER_GUIDE.md) for instructions on how to use the Code Review Assistant effectively.