import setuptools

long_description = open('README.md').read()

setuptools.setup(
    name="pykuna",
    version="0.5.0",
    author="Mark Coombes",
    author_email="mark@markcoombes.ca",
    description="Python3 library for interacting with the Kuna camera mobile API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marthoc/pykuna",
    packages=['pykuna'],
    install_requires=['aiohttp', 'asyncio', 'async_timeout'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
)
