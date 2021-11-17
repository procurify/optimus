from setuptools import setup

# Package meta-data.
NAME = "optimus"
DESCRIPTION = "A schema transformation tool."
URL = "https://github.com/procurify/optimus"
EMAIL = "nav@navaulakh.com"
AUTHOR = "Nav Aulakh"
VERSION = "0.1.2"
PACKAGES = ["optimus"]

# What packages are required for this module to be executed?
REQUIRED = ["jsonschema==3.1.1", "jsonpath-rw==1.4.0", "arrow==0.15.2"]

setup(
    name=NAME,
    version=VERSION,
    packages=PACKAGES,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    python_requires=">=3.7",
    install_requires=REQUIRED,
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
