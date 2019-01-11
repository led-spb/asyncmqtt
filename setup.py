#!/usr/bin/python
import setuptools
import paho_mqtt as module                  

setuptools.setup(
    name=module.name,
    version=module.version,
    author="Alexey Ponimash",
    author_email="alexey.ponimash@gmail.com",
    description="Tornado wrapper for paho_mqtt",
    url="https://github.com/led-spb/paho_async",
    packages=setuptools.find_packages(),
    install_requires=['paho_mqtt', 'tornado', ]
)