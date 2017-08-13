from distutils.core import setup

from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='lcom',
    packages=find_packages(exclude=['tests']),
    version='0.1.0',
    description='Lack of cohesion of methods metric',
    long_description=readme,
    author='Michal Wachowski',
    author_email='wachowski.michal@gmail.com',
    url='https://github.com/potfur/lcom',
    download_url='https://github.com/potfur/lcom/archive/0.1.0.tar.gz',
    keywords=[
        'cohesion',
        'code metrics',
        'code quality',
        'lcom',
        'lcom4'
    ],
    install_requires=[
        'click',
        'terminaltables'
    ],
    test_suite='tests',
    tests_require=[
        'pytest',
        'mock',
        'flake8',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'console_scripts': ['lcom=src.command:cmd'],
    }
)
