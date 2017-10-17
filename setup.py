from setuptools import setup, find_packages

setup(
    name="graphscii",
    version="0.1.0",
    packages=["graphscii"],
    description="A python library for making ascii-art into network graphs.",
    author="Peter Downs",
    author_email="antonlodder@gmail.com",
    url="https://github.com/AnjoMan/graphscii",
    download_url="https://github.com/AnjoMan/graphscii/archive/0.1.tar.gz",
    keywords=["graph", "network", "testing", "parser"],
    license="MIT",
    packages=find_package(exclude=["tests"],
    install_requires=[
        'networkx==1.11',
    ],
    extras_require={
        "test": ["pytest"],
    },
)
