import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "Spaceship",
    version = "0.0.4",
    author = "Sam Whang",
    author_email = "sangwoowhang@gmail.com",
    description = ("A sprite animation tutorial using bearlibterminal."),
    license = "MIT",
    keywords = "example documentation tutorial",
    url = "http://github.com/whitegreyblack/Spaceship.git",
    packages=['spaceship', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Terminal",
        "License :: OSI Approved :: MIT License",
    ],
)