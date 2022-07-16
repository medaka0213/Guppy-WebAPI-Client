from setuptools import setup, find_packages

setup(
    name='vrw_web_client',
    version='1.1.1',
    packages=find_packages(),
    install_requires = [
        "requests"
    ]
)