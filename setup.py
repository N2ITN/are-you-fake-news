"""Packaging setup for are-you-fake-news project
c/o @lockefox
"""
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '-v',
            '-m',
            'not docker',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

    def run_tests(self):
        import shlex
        import pytest
        pytest_commands = []
        try:
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

class CITest(PyTest):
    """wrapper for quick-testing for devs"""
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc'
        ]

with open('README.rst', 'r', 'utf-8') as f:
    README = f.read()

setup(
    name='are-you-fake-news',
    description='Reviews and rates news sites looking for fake news',
    version='1.0.0',
    long_description=README,
    author='Zachary A Estela',
    author_email='zestela@gmail.com',
    url='https://github.com/N2ITN/are-you-fake-news',
    download_url='TODO',
    license='GNU General Public License v3.0',
    classifiers=[

    ],
    keywords='newspaper news machine-learning website',
    packages=find_packages(),
    package_data={
        '': ['LICENSE', 'README.rst'],
        'get_process_data': [
            'opensources/sources/sources.csv',
            'opensources/sources/sources.json',
        ],
    },
    install_requires=[
        'boto3',
        'flask',
        'gmplot',
        'numpy',
        'pandas',
        'pymongo',
        'tldextract',
        'wtforms',
    ],
    tests_require=[
        'pytest',
        'docker',
    ],
    extras_require={
        'dev': [
            'sphinx',
        ]
    },
    cmdclass={
        'test': PyTest,
        'citest': CITest,
    },
)
