from codecs import open

from setuptools import setup


# Get the long description from the relevant file
def get_long_description():
    with open('README.rst', encoding='utf-8') as f:
        return f.read()


setup(
    name='gsm0338',
    version='1.2.0',
    description='GSM 03.38 codec',
    long_description=get_long_description(),
    long_description_content_type='text/x-rst',

    packages=['gsm0338'],

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
    ],

    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    project_urls={
        'Bug Reports': 'https://github.com/dsch/gsm0338/issues',
        'Source': 'https://github.com/dsch/gsm0338',
        'Continuous Integration': 'https://travis-ci.org/dsch/gsm0338',
    },
)
