from setuptools import setup, find_packages

setup(
    name="phylactery",
    version="0.1.0",
    package_dir={"": "phylactery"},
    packages=find_packages(where="phylactery"),
    install_requires=[
        "cryptography>=41.0.0",
        "shamir-mnemonic>=0.1.0",
        "click>=8.1.0",
    ],
    entry_points={
        "console_scripts": [
            "phylactery=phylactery.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A secure file encryption system using Shamir's Secret Sharing and AES-256-GCM",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/phylactery",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
) 