# Contributing to React Project Automator 🤝

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to React Project Automator. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents 📑

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs-)
  - [Suggesting Enhancements](#suggesting-enhancements-)
  - [Pull Requests](#pull-requests-)
- [Development Setup](#development-setup-)
- [Style Guidelines](#style-guidelines-)
- [Git Commit Messages](#git-commit-messages-)
- [Project Structure](#project-structure-)

## Code of Conduct 📜

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute? 🤔

### Reporting Bugs 🐛

Before creating bug reports, please check the [issue list](issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots and animated GIFs if possible

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as [GitHub issues](issues). When creating an enhancement suggestion, please include:

- A clear and descriptive title
- A detailed description of the proposed enhancement
- Examples of how the enhancement would be used
- Why this enhancement would be useful to most users
- List any alternatives you've considered

### Pull Requests 🔄

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Setup 🛠️

1. Clone your fork of the repository

```bash
git clone https://github.com/YOUR_USERNAME/react-project-automator.git
```

2. Install Python dependencies

```bash
pip install -r requirements.txt
```

3. Install development dependencies

```bash
pip install -r requirements-dev.txt
```

4. Setup pre-commit hooks

```bash
pre-commit install
```

## Style Guidelines 📝

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where possible
- Write docstrings for all public methods
- Keep lines under 80 characters
- Use meaningful variable names

Example:

```python
def create_project(self, config: ProjectConfig) -> bool:
    """
    Create a new React project with the given configuration.

    Args:
        config (ProjectConfig): Project configuration object

    Returns:
        bool: True if project creation was successful
    """
    try:
        # Implementation
        return True
    except Exception as e:
        self.logger.error(f"Project creation failed: {str(e)}")
        return False
```

### Qt/UI Guidelines

- Use Qt Designer for complex UI layouts
- Follow Qt naming conventions
- Keep UI elements properly aligned
- Ensure proper spacing between elements
- Support both light and dark themes

## Git Commit Messages ✍️

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Examples:

```
feat: Add Git integration module
fix: Resolve package installation error (#123)
docs: Update installation instructions
style: Format code according to PEP 8
test: Add unit tests for project creation
```

## Project Structure 📁

```
react-project-automator/
├── src/
│   ├── ui/                 # UI related files
│   ├── core/              # Core functionality
│   ├── utils/             # Utility functions
│   └── config/            # Configuration files
├── tests/                 # Test files
├── docs/                  # Documentation
└── resources/             # Assets and resources
```

## Testing 🧪

- Write unit tests for new features
- Ensure all tests pass before submitting PR
- Add integration tests for UI components
- Test both success and failure cases

```bash
# Run tests
python -m pytest

# Run tests with coverage
python -m pytest --cov=src
```

## Documentation 📚

- Update README.md if needed
- Add docstrings to new classes and methods
- Update Wiki for significant changes
- Include code examples where appropriate

## Questions? 🤔

Don't hesitate to ask questions by:

- Opening an issue
- Joining our Discord server
- Sending an email to contributors@reactautomator.com

## Recognition 🌟

Contributors will be:

- Listed in our README
- Added to the Contributors page
- Credited in release notes

Thank you for contributing to React Project Automator! 🙏

---

Note: This contributing guide was inspired by the contributing guides of various open source projects including Atom and React.