import subprocess
import sys
from os import path

from setuptools import setup

if sys.version_info[:2] < (3, 0):
    raise RuntimeError("Python version 3 required.")

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_packages(*args, **kwargs):
    return ['OHA', 'OHA.param_builders', 'tests']


def version():
    __version = '0.2.1'
    __tag = 'git'
    if path.exists('.git'):
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
    ],
    include_package_data=True
)
