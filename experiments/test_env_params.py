#!/usr/bin/env python3
"""
Test script to verify TEMPERATURE and FOLDER_NAME parameters work correctly.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import llm_runner
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv


def test_env_loading():
    """Test that TEMPERATURE and FOLDER_NAME can be loaded from .env"""
    load_dotenv()

    temperature = float(os.getenv('TEMPERATURE', '0.3'))
    folder_name = os.getenv('FOLDER_NAME', 'output')

    print(f"✓ TEMPERATURE loaded: {temperature} (type: {type(temperature).__name__})")
    print(f"✓ FOLDER_NAME loaded: {folder_name} (type: {type(folder_name).__name__})")

    # Test with custom values
    os.environ['TEMPERATURE'] = '0.7'
    os.environ['FOLDER_NAME'] = 'custom_output'

    temperature = float(os.getenv('TEMPERATURE', '0.3'))
    folder_name = os.getenv('FOLDER_NAME', 'output')

    print(f"\n✓ TEMPERATURE with custom value: {temperature}")
    print(f"✓ FOLDER_NAME with custom value: {folder_name}")

    assert temperature == 0.7, "Temperature should be 0.7"
    assert folder_name == 'custom_output', "Folder name should be 'custom_output'"

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    test_env_loading()
