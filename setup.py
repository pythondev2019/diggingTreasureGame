import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="diggingTreasureGame",
    version="0.0.1",
    author="Python3 msu cmc course",
    author_email="jungmyung27@gmail.com",
    description="Python3 project for cmc msu course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pythondev2019/diggingTreasureGame",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
