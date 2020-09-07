from setuptools import setup, find_packages

from easydata import __version__ as version

setup(
    name='easydata',
    version=version,
    description='Data transformation and manipulation library',
    long_description=open('README.rst').read(),
    long_description_content_type="text/x-rst",
    author='Rok Grabnar',
    author_email='grabnarrok@gmail.com',
    url='https://github.com/sitegroove/easydata',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'dateparser',
        'easytxt',
        'furl',
        'ftfy',
        'jmespath',
        'price-parser',
        'pyquery',
        'xmltodict'
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
