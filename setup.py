#!/usr/bin/env python3

"""
Setup script for DragDropWidgets library
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")

setup(
    name="dragdropwidgets",
    version="1.0.0",
    author="DragDropWidgets Team",
    author_email="team@dragdropwidgets.com",
    description="Professional Python library for creating interactive GUI interfaces with drag and drop support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dragdropwidgets/dragdropwidgets",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Desktop Environment",
        "Framework :: Qt",
    ],
    keywords=[
        "gui", "drag-drop", "widgets", "pyside6", "qt", "interface", 
        "desktop", "ui", "ux", "dashboard", "visual", "editor"
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "sphinx",
            "sphinx-rtd-theme",
        ],
        "examples": [
            "matplotlib",
            "numpy",
            "pillow",
        ]
    },
    entry_points={
        "console_scripts": [
            "dragdrop-hello=dragdropwidgets.examples.hello_world:main",
            "dragdrop-dashboard=dragdropwidgets.examples.dashboard:main",
        ],
    },
    include_package_data=True,
    package_data={
        "dragdropwidgets": [
            "examples/*.py",
            "utils/*.py",
            "widgets/*.py",
            "core/*.py",
        ],
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/dragdropwidgets/dragdropwidgets/issues",
        "Documentation": "https://dragdropwidgets.readthedocs.io/",
        "Source": "https://github.com/dragdropwidgets/dragdropwidgets",
        "Funding": "https://github.com/sponsors/dragdropwidgets",
    },
)