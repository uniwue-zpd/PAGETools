import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PAGETools",
    version="0.1",
    license="MIT License",
    author="Maximilian Nöth",
    author_email="maximilian.noeth@uni-wuerzburg.de",
    description="Toolset to perform various operations on PAGE XML datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/maxnth/PAGETools",
    packages=setuptools.find_packages(),
    install_requires=[
        "opencv-python",
        "lxml",
        "numpy",
        "click",
        "deskew"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "pagetools-extract-lines = pagetools.cli.transformations.extract_lines:main",
        ]
    },
    keywords=["PAGE XML", "OCR", "optical character recognition"],
    python_requires='>=3.6',
)
