import subprocess
import sys
from os import path

from setuptools import setup

__author__ = 'indrajit'
__email__ = 'eendroroy@gmail.com'

if sys.version_info[:2] < (3, 0):
    raise RuntimeError('Python version 3 required.')

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_packages(*args, **kwargs):
    return [
        'OHA',
        'OHA.assessments',
        'OHA.helpers',
        'OHA.helpers.calculators',
        'OHA.helpers.converters',
        'OHA.helpers.formatters',
        'OHA.helpers.measurements',
        'OHA.param_builders',
    ]


def version():
    __version = '0.2.2'
    __tag = 'b'
    if path.exists('.git'):
        __tag = 'git'
        __build = subprocess.check_output('git rev-list HEAD --count'.split()).decode().strip()
    else:
        __build = __tag
    return '%s.%s.%s' % (__version, __tag, __build)


setup(
    version=version(),
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,
)
