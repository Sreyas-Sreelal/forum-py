import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="forumpy",
    version="0.0.2",
    author="Sreyas Sreelal",
    author_email="sreyassreelal@gmail.com.com",
    description="An unofficial SA-MP forum api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sreyas-sreelal/forum-py",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ),
)