from codecs import open

from setuptools import setup


# Get the long description from the relevant file
def get_long_description():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name='gsm0338',
    version='1.1.0',
    description='GSM 03.38 codec',
    long_description=get_long_description(),

    packages=['gsm0338'],

    extras_require={
        "testing": ['six', 'pytest', 'pytest-cov', 'pytest-flake8', 'pytest-timeout'],
    },

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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries',
    ],
)
