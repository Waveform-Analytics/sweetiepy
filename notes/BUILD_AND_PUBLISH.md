# Build and Publish Process

This document outlines the complete process for building and publishing new versions of the `loopy-basic` package to PyPI.

## Prerequisites

- PyPI API token stored in `.env` file as `TWINE_PASSWORD`
- `uv` package manager installed
- Dev dependencies installed: `uv sync --extra dev`

## Quick Reference

For experienced developers who just need the commands:

```bash
# 1. Update version in pyproject.toml
# 2. Build and publish
uv run python -m build
uv run python publish.py
```

## Step-by-Step Process

### 1. Update Version Number

Edit `pyproject.toml` and increment the version number:

```toml
[project]
name = "loopy-basic"
version = "0.2.1"  # <- Update this
```

Follow semantic versioning:
- **Patch** (0.2.0 → 0.2.1): Bug fixes, small improvements
- **Minor** (0.2.0 → 0.3.0): New features, backwards compatible
- **Major** (0.2.0 → 1.0.0): Breaking changes

### 2. Build the Package

```bash
uv run python -m build
```

This creates distribution files in the `dist/` directory:
- `loopy_basic-X.Y.Z.tar.gz` (source distribution)
- `loopy_basic-X.Y.Z-py3-none-any.whl` (wheel)

### 3. Publish to PyPI

#### Option A: Using the Publish Script (Recommended)

```bash
uv run python publish.py
```

This script:
- Loads the PyPI token from `.env` file
- Automatically uploads to PyPI
- Provides clear success/error messages

#### Option B: Using Twine Directly

```bash
# Load environment variables from .env
source .env

# Upload using twine
uv run twine upload dist/loopy_basic-X.Y.Z* --username __token__
```

### 4. Verify Publication

After successful upload, verify the package is available:
- **PyPI URL**: `https://pypi.org/project/loopy-basic/X.Y.Z/`
- **Install test**: `pip install loopy-basic==X.Y.Z`

## Configuration Files

### `.env` File Structure

Your `.env` file should contain:

```bash
# MongoDB credentials
MONGODB_USERNAME=your_username
MONGODB_PW=your_password
MONGODB_URI=your_connection_string
MONGODB_DATABASE=your_database

# PyPI publishing token
TWINE_PASSWORD=pypi-AgEI...your-token-here
```

**Important**: The `.env` file is gitignored for security.

### PyPI Token Setup

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Create a new API token for this project
3. Copy the token (starts with `pypi-`)
4. Add to `.env` file as `TWINE_PASSWORD=your-token`

## Troubleshooting

### Common Issues

**"Package already exists"**
- You're trying to upload the same version twice
- Increment the version number in `pyproject.toml`

**"Invalid token"**
- Check that `TWINE_PASSWORD` is correctly set in `.env`
- Verify the token hasn't expired
- Ensure the token has upload permissions

**"Build fails"**
- Run `uv sync --extra dev` to install build dependencies
- Check that `pyproject.toml` is valid

### Clean Build

If you encounter issues, clean previous builds:

```bash
rm -rf dist/ build/ *.egg-info/
uv run python -m build
```

## Automation Ideas

For future enhancement, consider:

1. **GitHub Actions**: Automate publishing on git tags
2. **Pre-commit hooks**: Automatic version bumping
3. **Changelog generation**: Auto-update based on commits

## Release Checklist

- [ ] Update version number in `pyproject.toml`
- [ ] Test package locally: `uv run python -m src.loopy.data.cgm`
- [ ] Run build: `uv run python -m build`
- [ ] Publish: `uv run python publish.py`
- [ ] Verify on PyPI: Check package page loads
- [ ] Test installation: `pip install loopy-basic==X.Y.Z` in clean environment
- [ ] Update documentation if needed

## Recent Releases

### v0.2.0 (Latest)
- Added `MergedDataAccess` for CGM + pump settings correlation
- New analysis capabilities for time-synchronized data
- Enhanced pattern analysis tools

### v0.1.3
- Basic CGM and pump data access
- MongoDB connection management
- Initial analysis utilities