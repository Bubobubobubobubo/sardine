#!/usr/bin/env python3

from setuptools import setup, find_packages
import pathlib
here = pathlib.Path(__file__).parent.resolve()

setup(
    name="Sardine",
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
    install_requires=[
        "appdirs~=1.4",
        "mido~=1.2",
        "osc4py3~=1.0",
        "python-rtmidi~=1.4",
        "rich~=12.5"
    ],
    extras_require={"speed": ["uvloop"]},
)
