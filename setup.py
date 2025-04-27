#!/usr/bin/env python3
"""
Setup script for the Code File Organizer.

Copyright (c) 2023 Mahmoud Ashraf (SNO7E)
"""
from setuptools import setup, find_packages
import os
import re

# Read version from file_organizer.py
with open("file_organizer.py", "r") as f:
    version_match = re.search(r'^__version__ = ["\']([^"\']*)["\']', f.read(), re.MULTILINE)
    version = version_match.group(1) if version_match else "0.0.0"

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="code-file-organizer",
    version=version,
    description="A smart tool that automatically organizes code files into directories based on file type, project structure, and content analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mahmoud Ashraf (SNO7E)",
    author_email="github@sno7e.com",  # Replace with your actual email if needed
    url="https://github.com/SNO7E-G/code-file-organizer",
    py_modules=["file_organizer"],  # Single module, not a package
    entry_points={
        "console_scripts": [
            "code-organizer=file_organizer:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    install_requires=[],  # No external dependencies
    keywords="file organizer, code organization, directory structure",
    project_urls={
        "Bug Tracker": "https://github.com/SNO7E-G/code-file-organizer/issues",
        "Source Code": "https://github.com/SNO7E-G/code-file-organizer",
    },
    license="MIT",
) 