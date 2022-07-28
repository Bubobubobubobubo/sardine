#!/usr/bin/env python3

from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()

setup(
    name="Bibu",
    version="0.0.1",
    description="MIDI Live Coding in Python",
    author="Raphaël Forment",
    author_email="raphael.forment@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers, Musicians",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(where="src"),
    python_requires=">=3.7, <4",
    install_requires=["mido", "rich", "uvloop", "ipython", "osc4py3"],
    # entry_points={  # Optional
    #     "console_scripts": [
    #         "sample=sample:main",
    #     ],
    # },
)
