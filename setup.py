import os
import sys

from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
        'requests',
]

setup(
    name='generic_api_client',
    version='0.0.1',
    author='Chase Yakaboski',
    author_email='chase.th@dartmouth.edu',
    description='A generic python api wrapper  application.',
    packages=find_packages(),
    install_requires=REQUIRED_PACKAGES,
    python_requires='>=3.6'
)

