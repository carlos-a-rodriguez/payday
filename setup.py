"""A setuptools based setup module."""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="payday",
    version="0.1.0",
    description="Calculate Pay Day",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/carlos_rodriguez/payday",
    author="Carlos Andres Rodriguez",
    author_email="carlos.rodriguez@protonmail.ch",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="payday,paycheck",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    python_requires=">=3.6, <4",
    install_requires=["holidays", "numpy", "python-dateutil", "wheel"],
    extras_require={
        "dev": [],
        "test": [],
    },
    project_urls={
        "Bug Reports": "https://gitlab.com/carlos_rodriguez/payday/-/issues",
        "Source": "https://gitlab.com/carlos_rodriguez/payday",
    },
)
