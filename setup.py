from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
from codecs import open
from os import path
import sys

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            'test',
            '--pep8',
        ]
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name='gsm0338',
    version='1.0a1',
    description='GSM 03.38 codec',
    long_description=long_description,

    packages=find_packages(),
    install_requires=['six'],
    package_data={
        '': ['*.txt', '*.rst'],
        },

    tests_require=[
        'pytest',
        'pytest-pep8',
    ],
    cmdclass={'test': PyTest},

    # metadata for upload to PyPI
    author='David Schneider',
    author_email='david.schneider@postmail.ch',
    license='MIT',
    url='https://github.com/dsch/gsm0338',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries',
    ],
    )
