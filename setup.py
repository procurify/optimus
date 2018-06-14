from setuptools import setup

# Package meta-data.
NAME = 'optimus'
DESCRIPTION = 'A schema transformation tool.'
URL = 'https://github.com/procurify/optimus'
EMAIL = 'nav@navaulakh.com'
AUTHOR = 'Nav Aulakh'
VERSION = '0.1.0'

# What packages are required for this module to be executed?
REQUIRED = [
    'jsonschema==2.6.0',
    'jsonpath-rw==1.4.0',
    'arrow==0.12.1'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires='>=2.7',
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
