#!/usr/bin/env python3
"""
Setup script for Library Management System
"""

from setuptools import setup, find_packages

setup(
    name="library-management-system",
    version="1.0.0",
    description="Library Management System for CISC/CMPE 327 Assignment 2",
    author="Dazz0h",
    author_email="emmanueldawesome@gmail.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "Flask>=2.3.0",
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
    ],
    extras_require={
        "dev": [
            "flake8>=6.0.0",
            "bandit>=1.7.0",
            "safety>=2.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
