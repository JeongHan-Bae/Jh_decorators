from setuptools import setup, find_packages
import pathlib

# Read the contents of the README file
README = pathlib.Path(__file__).parent / "README.md"

setup(
    name='jh_decorators',
    version='0.1.0',
    description='A collection of decorators for adding documentation, logging, timing, and serialization '
                'functionalities to Python classes and functions.',
    author='JeongHan Bae',
    author_email='mastropseudo@gmail.com',
    url='https://github.com/JeongHan-Bae/Jh_decorators',
    packages=find_packages(),
    install_requires=[
        'pyyaml~=6.0',
        'xmltodict~=0.13.0',
        'rich~=13.0.0',
        'colorama~=0.4.4'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    long_description=README.read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
)
