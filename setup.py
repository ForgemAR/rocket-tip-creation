import sys
from setuptools import setup, find_packages

setup(
    name = "ConeGen",
    version = "1.0",
    packages = find_packages(),
    install_requires = ['solidpython', 'sympy'],
    author = "Diez B. Roggisch",
    author_email = "deets@web.de",
    description = "A package to generate a rocket tip cone for the FAR.",
    license = "GPL",
    entry_points = {
        'console_scripts': [
            'cone-gen = conegen:main',
        ],
    }
)
