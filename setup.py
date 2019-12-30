import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usc-schedule",
    version="0.0.1",
    author="Swapnil Patel",
    author_email="swapnil@usc.edu",
    description="A USC Class Schedule API wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TrickRoom/USC-schedule",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)