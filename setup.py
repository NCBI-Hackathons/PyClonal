import os
from setuptools import find_packages, setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()


def extract_version():
    """
    Extracts version values from the main matplotlib __init__.py and
    returns them as a dictionary.
    """
    with open('pyclonal/__init__.py') as fd:
        for line in fd.readlines():
            if (line.startswith('__version__')):
                exec(line.strip())
    return locals()["__version__"]


def get_package_data():
    return {
        'pyclonal':
        [
            "jupyter_notebooks/*.ipynb",
            "sample_input_files/*.csv",
            "sample_input_files/Mixcr/*.txt",
            "sample_input_files/changeo/*.tsv",
            "sample_input_files/vdjtools/*.txt",
            "sample_input_files/ImmunoSeq/*.tsv",
        ]}

setup(
    name="PyClonal",
    version=extract_version(),
    author="NCBI Hackathon, Michelle Miron, Ilya Shamovsky , Britney Martinez, Filip Cvetkovski, Ben Busby, Kevin Modzelewski, and Avi",
    author_email="miron.michelle@gmail.com",
    url="https://github.com/NCBI-Hackathons/PyClonal.git",
    license="MIT",
    packages=find_packages(),
    package_dir={"pyclonal": "pyclonal"},
    package_data=get_package_data(),
    entry_points={
        'console_scripts': ['pcl=pyclonal.pcl:main'],
        },
    description="A Jupyter Notebook pipeline to analyze T-cell Receptor Sequencing",
    # run pandoc --from=markdown --to=rst --output=README.rst README.md
    long_description=read_md('README.md'),
    # numpy is here to make installing easier... Needs to be at the
    # last position, as that's the first installed with
    # "python setup.py install"
    install_requires = ['pandas', 'jupyter', 'scipy', 'seaborn'],

    classifiers=['Intended Audience :: Science/Research',
                 'Programming Language :: Python',
                 'Topic :: Scientific/Engineering :: Bio-Informatics',
                 'Topic :: Scientific/Engineering :: Visualization',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX',
                 'Operating System :: Unix',
                 'Operating System :: MacOS',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6'],
    zip_safe=False)
