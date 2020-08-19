from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="haveibeenpywned",  # Replace with your own username
    version="0.1",
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
