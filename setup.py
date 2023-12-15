from setuptools import setup, find_packages

# Read the version number from a file
with open("VERSION") as version_file:
    version = version_file.read().strip()

# Read the requirements from a file
with open("VERSION") as requirements_file:
    requirements = requirements_file.read().splitlines()

setup(
    name="espn-toilet",
    version=version,
    author="Shawn Johnson",
    author_email="11654145+brthurr@users.noreply.github.com",
    description="ESPN Fantasy Football losers bracket app",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/brthurr/espn-toilet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
