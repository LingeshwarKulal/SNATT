"""
SNATT - Smart Network Automation and Troubleshooting Tool
Setup configuration
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="snatt",
    version="0.1.0",
    author="SNATT Development Team",
    author_email="support@snatt.dev",
    description="Smart Network Automation and Troubleshooting Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/snatt",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "customtkinter>=5.2.0",
        "pillow>=10.0.0",
        "netmiko>=4.3.0",
        "napalm>=4.1.0",
        "paramiko>=3.3.1",
        "scapy>=2.5.0",
        "pysnmp>=4.4.12",
        "pandas>=2.1.0",
        "openpyxl>=3.1.2",
        "reportlab>=4.0.4",
        "matplotlib>=3.7.2",
        "keyring>=24.2.0",
        "cryptography>=41.0.3",
        "requests>=2.31.0",
        "apscheduler>=3.10.4",
        "colorlog>=6.7.0",
        "click>=8.1.6",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "snatt=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
