# Contributing to DragDropWidgets

First off, thank you for considering contributing to DragDropWidgets! It's people like you that make DragDropWidgets such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for DragDropWidgets. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

**Before Submitting A Bug Report:**
- Check the documentation for a list of common questions and problems
- Ensure the bug was not already reported by searching on GitHub under Issues
- If you're unable to find an open issue addressing the problem, open a new one

**How Do I Submit A Bug Report?**

Bugs are tracked as GitHub issues. Create an issue and provide the following information:

- Use a clear and descriptive title
- Describe the exact steps which reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead and why
- Include screenshots and animated GIFs if possible

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain which behavior you expected to see instead
- Explain why this enhancement would be useful

### Your First Code Contribution

Unsure where to begin contributing? You can start by looking through these `beginner` and `help-wanted` issues:

- **Beginner issues** - issues which should only require a few lines of code, and a test or two
- **Help wanted issues** - issues which should be a bit more involved than `beginner` issues

### Pull Requests

The process described here has several goals:
- Maintain DragDropWidgets' quality
- Fix problems that are important to users
- Engage the community in working toward the best possible DragDropWidgets
- Enable a sustainable system for maintainers to review contributions

Please follow these steps to have your contribution considered by the maintainers:

1. Follow all instructions in the template
2. Follow the styleguides
3. After you submit your pull request, verify that all status checks are passing

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Setting up your development environment

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/dragdropwidgets.git
cd dragdropwidgets
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e .[dev]
```

4. Run tests to make sure everything is working:
```bash
pytest
```

### Development Workflow

1. Create a new branch for your feature or bugfix:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

2. Make your changes and add tests if needed

3. Run the test suite:
```bash
pytest
```

4. Run code formatting and linting:
```bash
black dragdropwidgets/
flake8 dragdropwidgets/
mypy dragdropwidgets/
```

5. Commit your changes:
```bash
git add .
git commit -m "Add your descriptive commit message"
```

6. Push to your fork and submit a pull request

## Styleguides

### Git Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Python Styleguide

- Follow PEP 8
- Use Black for code formatting
- Use type hints where appropriate
- Write docstrings for all public methods and classes

Example:
```python
def create_widget(widget_type: str, **kwargs) -> Optional[WidgetBase]:
    """Create a new widget of the specified type.
    
    Args:
        widget_type: The type of widget to create
        **kwargs: Additional arguments to pass to the widget constructor
        
    Returns:
        The created widget instance, or None if creation failed
        
    Raises:
        ValueError: If widget_type is not supported
    """
    pass
```

### Documentation Styleguide

- Use Markdown for documentation
- Include code examples where appropriate
- Keep lines to 80 characters when possible
- Use clear, concise language

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Ensure tests are independent and can run in any order
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases

### Test Structure

```python
def test_widget_creation():
    """Test that widgets are created correctly."""
    widget = DraggableButton("Test")
    assert widget.get_text() == "Test"
    assert widget.is_draggable is True

def test_widget_invalid_input():
    """Test that widgets handle invalid input gracefully."""
    with pytest.raises(ValueError):
        widget = DraggableButton("")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_widgets.py

# Run with coverage
pytest --cov=dragdropwidgets

# Run tests in parallel
pytest -n auto
```

## Creating New Widget Types

When creating new widget types, follow these guidelines:

1. Inherit from `DraggableWidget` or `WidgetBase`
2. Implement required methods (`clone`, `get_properties`, `set_properties`)
3. Add comprehensive docstrings
4. Include metadata for the widget factory
5. Write tests for all functionality
6. Update documentation

Example:
```python
class DraggableNewWidget(DraggableWidget):
    """A new type of draggable widget.
    
    This widget provides functionality for...
    """
    
    def __init__(self, initial_value="", parent=None):
        super().__init__(parent)
        # Implementation here
        
    def clone(self):
        """Create a copy of this widget."""
        # Implementation here
        
    def get_properties(self) -> Dict[str, Any]:
        """Get widget properties for serialization."""
        # Implementation here
        
    def set_properties(self, properties: Dict[str, Any]):
        """Set widget properties from serialized data."""
        # Implementation here
```

## Documentation

### Building Documentation

```bash
cd docs/
make html
```

### Adding Examples

When adding new examples:

1. Create a new file in `dragdropwidgets/examples/`
2. Include comprehensive comments
3. Add a main function that can be called directly
4. Update the README with information about the new example
5. Add console script entry in setup.py if appropriate

## Release Process

### Version Numbers

We use semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Incompatible API changes
- MINOR: New functionality in a backwards compatible manner
- PATCH: Backwards compatible bug fixes

### Preparing a Release

1. Update version number in `setup.py` and `__init__.py`
2. Update CHANGELOG.md with new features and fixes
3. Run full test suite
4. Create release notes
5. Tag the release
6. Build and upload to PyPI

## Community

### Getting Help

- GitHub Discussions for questions and general discussion
- GitHub Issues for bug reports and feature requests
- Email support for private matters

### Staying Informed

- Watch the repository for updates
- Follow our blog for major announcements
- Join our community chat

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes for their contributions
- Special recognition for significant contributions

Thank you for contributing to DragDropWidgets!