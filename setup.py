#! /usr/bin/env python


import os

from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as stream:
        return stream.read()


setup(
    name="CoLiW",
    version="0.1",
    description="Command Line for Web",
    long_description=read("README.md"),
    url="https://github.com/cmin764/coliw.git",
    license="MIT",
    author='Cosmin "cmiN" Poieana',
    author_email="cmin764@gmail.com",
    packages=["coliw"],
    include_package_data=True,
    zip_safe=False,
    install_requires=read("requirements.txt").splitlines()
)
