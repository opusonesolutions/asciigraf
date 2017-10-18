from setuptools import setup

setup(
    name="asciigraf",
    version="0.1.0",
    packages=["asciigraf"],
    description="A python library for making ascii-art into network graphs.",
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
