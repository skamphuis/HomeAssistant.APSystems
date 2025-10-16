# Contributing to APSystems OpenAPI Integration

Thank you for your interest in contributing to the APSystems OpenAPI Home Assistant integration!

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Home Assistant development environment
- Git
- APSystems OpenAPI credentials for testing

### Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/HomeAssistant.APSystems.git
   cd HomeAssistant.APSystems
   ```

3. Create a development environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements_dev.txt  # If available
   ```

4. Link the integration to your Home Assistant development instance:
   ```bash
   ln -s $(pwd)/custom_components/apsystems_openapi ~/.homeassistant/custom_components/
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Home Assistant version
- Integration version
- Relevant log messages

### Suggesting Features

Feature requests are welcome! Please create an issue with:
- Clear description of the feature
- Use case and benefits
- Potential implementation approach (optional)

### Code Contributions

1. **Create an Issue First**: For significant changes, create an issue to discuss the change before starting work

2. **Create a Branch**: Create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**: Follow the coding guidelines below

4. **Test Your Changes**: Ensure all tests pass and the integration works

5. **Commit Your Changes**: Use clear, descriptive commit messages
   ```bash
   git commit -m "Add: Description of your change"
   ```

6. **Push to Your Fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**: Submit a PR with a clear description of changes

## Coding Guidelines

### Python Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where applicable
- Maximum line length: 100 characters (Home Assistant standard)
- Use f-strings for string formatting

### Code Structure

- Keep functions small and focused
- Use async/await for I/O operations
- Handle exceptions appropriately
- Add logging for debugging (use appropriate levels)

### Documentation

- Add docstrings to all public functions and classes
- Update README.md if adding features
- Update API.md for API changes
- Add examples to EXAMPLES.md for new features

### Naming Conventions

- Use descriptive variable names
- Constants: `UPPER_SNAKE_CASE`
- Functions/methods: `snake_case`
- Classes: `PascalCase`
- Private methods: `_leading_underscore`

## Testing

### Manual Testing

1. Install the integration in a test Home Assistant instance
2. Configure with real credentials
3. Verify sensors are created
4. Check sensor values update correctly
5. Test error handling (invalid credentials, network issues)
6. Check logs for warnings or errors

### Test Checklist

Before submitting a PR, ensure:
- [ ] Integration loads without errors
- [ ] Configuration flow works correctly
- [ ] Sensors are created and update
- [ ] Error handling works (test with invalid credentials)
- [ ] No new warnings in logs
- [ ] Documentation is updated
- [ ] Code follows style guidelines

## Code Review Process

1. Maintainer will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Areas for Contribution

We welcome contributions in these areas:

### New Features
- Additional sensor types
- Support for multiple systems
- Historical data access
- Device diagnostics
- Service calls for manual updates

### Improvements
- Better error messages
- Enhanced logging
- Performance optimizations
- Code refactoring
- Test coverage

### Documentation
- Additional examples
- Translation to other languages
- Tutorial videos/guides
- API documentation improvements

### Bug Fixes
- Fix reported issues
- Handle edge cases
- Improve error handling

## Release Process

1. Version bump in `manifest.json`
2. Update CHANGELOG.md
3. Create GitHub release
4. Tag with version number

## Questions?

- Open an issue for questions
- Check existing issues and PRs
- Review the API documentation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make this project better for everyone. Thank you for taking the time to contribute!
