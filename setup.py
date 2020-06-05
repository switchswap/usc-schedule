import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usc-schedule",
    version="1.0.1",
    author="Swapnil Patel",
    author_email="swapnil@usc.edu",
    description="A USC Class Schedule API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/switchswap/USC-schedule",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Topic :: Education",
        "Topic :: Internet",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires='>=3.6',
)
