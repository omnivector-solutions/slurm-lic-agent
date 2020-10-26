#!/usr/bin/python3
from setuptools import find_packages, setup


setup(
    name='slurm-lic-agent',
    packages=find_packages(where='.'),
    version='0.0.1',
    license='MIT',
    long_description=open('README.md', 'r').read(),
    url='https://github.com/omnivector-solutions/slurm-lic-agent',
    install_requires=['websockets'],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['slurm-lic-agent=slurm_lic_agent.main:main'],
    },
)
