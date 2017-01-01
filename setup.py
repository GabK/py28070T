from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Py28070T',

    version='1.0.0',

    description='Python driver for Nexxtech RF power outlets (using 28070T RF transmitter)',
    long_description=long_description,

    url='https://github.com/GabK/py28070T',

    author='Gabriel Kenderessy',
    author_email='g@brie.lk',

    license='Apache-2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: System :: Hardware :: Hardware Drivers',

        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='28070T nexxtech py28070T power outlet',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['RPi.GPIO'],
    entry_points={
        'console_scripts': [
            'py28070T=py28070T:main',
        ],
    },
)