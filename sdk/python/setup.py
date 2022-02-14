from setuptools import setup

with open("./requirements.txt") as requirements_file:
    requirements = requirements_file.readlines()


setup(
    name='jeyn',
    version='0.0.1',
    packages=['jeyn'],
    install_requires=requirements,
)
