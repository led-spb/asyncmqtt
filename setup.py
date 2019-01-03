#!/usr/bin/python
import setuptools
                  

setuptools.setup(
    name="asyncmqtt",
    version="0.0.1",
    author="Alexey Ponimash",
    author_email="alexey.ponimash@gmail.com",
    description="Tornado wrapper for paho_mqtt",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/led-spb/asyncmqtt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
       'paho_mqtt',
       'tornado',
    ]
)