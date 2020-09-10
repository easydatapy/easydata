import re
from setuptools import setup, find_packages


(__version__, ) = re.findall(r"__version__.*\s*=\s*[\"]([^']+)[\"]",
                             open('easydata/__init__.py').read())


setup(
    name='easydata',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'dateparser',
        'easytxt',
        'furl',
        'ftfy',
        'jmespath',
        'price-parser',
        'pyquery',
        'pyyaml',
        'xmltodict'
    ]
)
