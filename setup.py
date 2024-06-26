"""Setuptools configuration."""

import setuptools  # type: ignore

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements: list[str] = []
test_requirements: list[str] = []

setuptools.setup(
    name="sageleaf",
    version="0.0.1",
    author="Petar Peychev",
    author_email="petarpeychev@gmail.com",
    description="short description.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="placeholder",
    python_requires=">=3.12",
    install_requires=requirements,
    tests_require=test_requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "sageleaf = sageleaf.main:main",
        ],
    },
)
