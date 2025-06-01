# Contributing to FluxPilot

Thank you for your interest in contributing to FluxPilot! We welcome contributions from everyone and appreciate your help in making this project better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Submitting Changes](#submitting-changes)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Features](#suggesting-features)

## 🤝 Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Set up the development environment** (see below)
4. **Create a branch** for your changes
5. **Make your changes** and test them
6. **Submit a pull request**

## 💡 How to Contribute

There are many ways to contribute:

- 🐛 **Report bugs** - Help us identify and fix issues
- 💡 **Suggest features** - Share ideas for new functionality
- 📖 **Improve documentation** - Help others understand the project
- 🔧 **Submit code** - Fix bugs or implement new features
- 🧪 **Test** - Help us ensure quality by testing features
- 🎨 **Design** - Improve the user interface and experience

## 🛠️ Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Setup Steps

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/dev-environment-launcher.git
   cd dev-environment-launcher
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python main.py
   ```

### Project Structure

```
dev-environment-launcher/
├── main.py                 # Main application entry point
├── profile_manager.py      # Profile creation and management
├── process_runner.py       # Process execution and monitoring
├── ports_checker.py        # Port monitoring and management
├── requirements.txt        # Dependencies
├── profiles.json          # User profiles (auto-generated)
├── README.md             # Project documentation
├── CONTRIBUTING.md       # This file
├── LICENSE              # MIT License
└── .gitignore          # Git ignore rules
```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines
- Use 4 spaces for indentation
- Line length should not exceed 88 characters
- Use meaningful variable and function names

### Code Quality

- Write clear, readable code with appropriate comments
- Use type hints where applicable
- Follow the existing code structure and patterns
- Ensure your code works on Windows, macOS, and Linux

### Example Code Style

```python
def process_profile_data(profile: dict) -> bool:
    """
    Process profile data and validate its structure.
    
    Args:
        profile: Dictionary containing profile information
        
    Returns:
        bool: True if processing successful, False otherwise
    """
    if not profile.get("name"):
        return False
    
    # Process steps
    steps = profile.get("steps", [])
    for step in steps:
        if not step.get("command"):
            return False
    
    return True
```

## 🔄 Submitting Changes

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them:
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a pull request** on GitHub

### Pull Request Guidelines

- **Clear title**: Summarize what your PR does
- **Description**: Explain the changes and why they're needed
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes
- **Documentation**: Update documentation if needed

### Example PR Description

```markdown
## Description
Add support for environment variables in profile commands

## Changes
- Added environment variable parsing in ProcessRunner
- Updated ProfileDialog to include environment variable input
- Added validation for environment variable syntax

## Testing
- Tested on Windows 10, macOS, and Ubuntu 20.04
- Verified environment variables are properly passed to subprocesses
- Tested with both valid and invalid environment variable syntax

## Screenshots
[Include screenshots if UI changes are involved]
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to reproduce**: Detailed steps to recreate the bug
3. **Expected behavior**: What you expected to happen
4. **Actual behavior**: What actually happened
5. **Environment**: OS, Python version, application version
6. **Screenshots**: If applicable
7. **Error messages**: Copy any error messages

### Bug Report Template

```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
A clear description of what you expected to happen.

## Actual Behavior
A clear description of what actually happened.

## Environment
- OS: [e.g. Windows 10, macOS 11.0, Ubuntu 20.04]
- Python Version: [e.g. 3.9.0]
- Application Version: [e.g. 1.0.0]

## Additional Context
Add any other context about the problem here.
```

## 💡 Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Check existing issues** to avoid duplicates
2. **Describe the problem** your feature would solve
3. **Describe the solution** you'd like to see
4. **Consider alternatives** and mention them
5. **Provide examples** of how it would be used

### Feature Request Template

```markdown
## Feature Description
A clear and concise description of the feature.

## Problem Statement
What problem does this feature solve?

## Proposed Solution
A clear description of what you want to happen.

## Alternatives Considered
Describe alternative solutions you've considered.

## Use Cases
Provide examples of how this feature would be used.

## Additional Context
Add any other context or screenshots about the feature request.
```

## 🏷️ Labels

We use labels to categorize issues and PRs:

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements or additions to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `question` - Further information is requested

## 🙏 Recognition

Contributors will be recognized in:

- The project's README
- Release notes for significant contributions
- GitHub's contributor graph

## 📞 Getting Help

If you need help:

1. Check the [README](README.md) for basic information
2. Look through existing [issues](https://github.com/yourusername/dev-environment-launcher/issues)
3. Create a new issue with the `question` label
4. Be patient and respectful when asking for help

Thank you for contributing to FluxPilot! 🚀 