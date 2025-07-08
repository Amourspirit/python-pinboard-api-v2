#!/usr/bin/env python3
"""
Simple test runner script for the Pinboard API tests.

Copyright (c) 2025 :Barry-Thomas-Paul: Moss
Licensed under the MIT License - see LICENSE file for details.
"""

import subprocess
import sys
import os


def run_tests():
    """Run the test suite."""
    print("Running Pinboard API tests...")
    print("=" * 50)

    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    try:
        # Run pytest with verbose output
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_pinboard_api.py",
                "-v",
                "--tb=short",
            ],
            check=True,
        )

        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        return True

    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Some tests failed!")
        print(f"Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Make sure you have pytest installed:")
        print("pip install pytest")
        return False


def run_coverage():
    """Run tests with coverage report."""
    print("Running tests with coverage...")
    print("=" * 50)

    try:
        # Run pytest with coverage
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/test_pinboard_api.py",
                "--cov=pbapi2",
                "--cov-report=term-missing",
                "-v",
            ],
            check=True,
        )

        print("\n" + "=" * 50)
        print("✅ Tests completed with coverage report!")
        return True

    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 50)
        print("❌ Tests failed!")
        return False
    except FileNotFoundError:
        print("❌ pytest-cov not found. Install it with:")
        print("pip install pytest-cov")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--coverage":
        success = run_coverage()
    else:
        success = run_tests()

    sys.exit(0 if success else 1)
