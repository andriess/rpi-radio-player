# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='rpi_radio_player',
    version='0.1.0',
    description='Software for my physical rpi radio player',
    long_description=readme,
    author='Andries Schaap',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

