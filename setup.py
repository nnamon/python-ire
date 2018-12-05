# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from python_ire.version import __version__

setup(
    name='python-ire',
    version=__version__,
    author='amon',
    author_email='amon@nandynarwhals.org',
    description='This provides a python wrapper around the IRE Irator API.',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
        'setuptools',
    ],
    tests_require=[
        'pytest',
        'tox<=2.9.1',
    ],
    install_requires=[
        'Sphinx>=1.7.0',
    ],
    entry_points={
        'console_scripts': [
        ],
    },
    url='https://github.com/nnamon/python-ire'
)
