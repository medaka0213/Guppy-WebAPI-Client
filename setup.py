from setuptools import setup, find_packages

setup(
    name='vrw_web_client',
    version='2.0.0',
    packages=find_packages(),
    install_requires = [
        "requests", "pydantic"
    ]
)