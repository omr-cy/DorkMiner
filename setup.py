from setuptools import setup
from pathlib import Path

directory = Path(__file__).parent.resolve()
description = directory.joinpath("README.md").read_text(encoding="utf-8")
requirements = directory.joinpath("requirements.txt")

if requirements.exists():
    requirements = [
        line.strip() for line in requirements.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
else:
    requirements = []

setup(
    name="dorkminer",         
    python_requires=">=3.12",
    version="0.9",
    py_modules=["dorkminer"],  
    install_requires=requirements,
    entry_points={
        "console_scripts": ["dorkminer = dorkminer:cli",],
    },
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/omr-cy/DorkMiner", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license="MIT",
    author="Omar Ashraf",
)

