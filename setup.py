from os import path
from codecs import open
from setuptools import setup


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def find_packages(*args, **kwargs):
    return ['OpenHealthAlgorithms', 'tests']

setup(
    name='openhealthalgorithms',
    version='0.1.0',
    description='An implementation of health algorithms.',
    long_description=long_description,
    url='https://github.com/openhealthalgorithms/openhealthalgorithms',
    author='OpenHealthAlgorithms',
    author_email='',
    license='Apache',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(),
    install_requires=[
        'numpy',
    ]
    # entry_points={
    #     'console_scripts': [
    #         'spike=spikes:main',
    #     ],
    # },
)
