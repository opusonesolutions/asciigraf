from setuptools import setup


def readme():
    with open("README.md", 'r') as f:
        return f.read()


setup(
    name="asciigraf",
    version="0.1.1",
    packages=["asciigraf"],
    description="A python library for making ascii-art into network graphs.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    long_description=readme(),
    author="Anton Lodder",
    author_email="antonlodder@gmail.com",
    url="https://github.com/AnjoMan/asciigraf",
    keywords=["graph", "network", "testing", "parser"],
    license="MIT",
    install_requires=[
        'networkx==1.11',
    ],
    extras_require={
        "test": ["pytest"],
    },
)
