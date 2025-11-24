"""
SetBit Python SDK - Setup
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="setbit",
    version="0.1.0",
    author="SetBit",
    author_email="support@setbit.io",
    description="Python SDK for SetBit feature flags and A/B testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/setbit/setbit-python",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    keywords="feature-flags ab-testing experiments setbit",
    project_urls={
        "Documentation": "https://docs.setbit.io",
        "Source": "https://github.com/setbit/setbit-python",
        "Bug Reports": "https://github.com/setbit/setbit-python/issues",
    },
)
