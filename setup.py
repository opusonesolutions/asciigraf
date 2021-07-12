import os.path
from setuptools import setup

thisdir = os.path.abspath(os.path.dirname(__file__))
version = open(os.path.join(thisdir, 'asciigraf', 'VERSION')).read().strip()


def readme():
    with open("README.rst", 'r') as f:
        return f.read()


setup(
    name="asciigraf",
    version=version,
    packages=["asciigraf"],
    package_data={
        '': ['VERSION']
    },
    description="A python library for making ascii-art into network graphs.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=readme(),
    author="Opus One Solutions",
    author_email="rnd@opusonesolutions.com",
    url="https://github.com/opusonesolutions/asciigraf",
    keywords=["graph", "network", "testing", "parser"],
    license="MIT",
    install_requires=[
        "networkx>=1.11,<2.6; python_version < '3.7'",
        "colorama",
    ],
    extras_require={
        "test": ["pytest", "pytest-cov", "flake8"],
    },
)
