from setuptools import setup, find_packages

setup(
    name='calkumodules',
    version='0.1.0',
    description='A self made modules in Python',
    author='calKU',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
    ],
)