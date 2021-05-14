import setuptools

setuptools.setup(
    name="pseudocoder-willwill2will",
    version="0.0.1",
    author="William Charlton",
    author_email="author@example.com",
    description="A small example package",
    long_description="...",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires='tatsu'
)
