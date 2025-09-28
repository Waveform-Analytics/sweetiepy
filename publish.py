#!/usr/bin/env python
"""
Simple script to publish package to PyPI using environment variables from .env file
"""

import os
import subprocess
from dotenv import load_dotenv

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the PyPI token
    token = os.getenv('TWINE_PASSWORD')
    if not token:
        print("ERROR: TWINE_PASSWORD not found in environment variables")
        print("Please add your PyPI API token to .env file:")
        print("TWINE_PASSWORD=your-pypi-api-token")
        return 1
    
    # Set environment variables for twine
    env = os.environ.copy()
    env['TWINE_USERNAME'] = '__token__'
    env['TWINE_PASSWORD'] = token
    
    # Run twine upload
    cmd = ['twine', 'upload', 'dist/sweetiepy-1.0.0*']
    result = subprocess.run(cmd, env=env)
    
    if result.returncode == 0:
        print("✅ Package published successfully to PyPI!")
    else:
        print("❌ Failed to publish package")
        return result.returncode
    
    return 0

if __name__ == "__main__":
    exit(main())