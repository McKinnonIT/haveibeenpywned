from setuptools import setup, find_packages

VERSION = "0.2.93"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="haveibeenpywned",
    version=VERSION,
    author="Sam Neal",
    author_email="sam.w.neal@gmail.com",
    description="A simple python wrapper for the www.haveibeenpwned.com API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scv-m/haveibeenpywned",
    download_url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=["ratelimit", "requests",],
)
