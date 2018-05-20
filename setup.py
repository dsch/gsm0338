import sys
from codecs import open
from os import path

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


class PyTest(TestCommand):

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            'py.test',
            '--flake8',
        ]
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='gsm0338',
    version='1.1.0',
    description='GSM 03.38 codec',
    long_description=long_description,

    packages=find_packages(),
    install_requires=[],
    package_data={
        '': ['*.rst'],
    },

    tests_require=[
        'six',
        'pytest',
        'pytest-flake8',
    ],
    cmdclass={'test': PyTest},

    # metadata for upload to PyPI
    author='David Schneider',
    author_email='schneidav81@gmail.com',
    license='MIT',
    url='https://github.com/dsch/gsm0338',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
)
