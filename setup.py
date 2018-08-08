import os
from setuptools import find_packages, setup


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
            "sample_input_files/*.tsv",
            "sample_input_files/*.txt"
        ]}

setup(
    name="PyClonal",
    version=extract_version(),
    author="NCBI Hackathon, Michelle Miron, Ilya Shamovsky , Britney Martinez, Filip Cvetkovski, Ben Busby, Avi, and Kevin",
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
    long_description=open("README.rst").read(),
    # numpy is here to make installing easier... Needs to be at the
    # last position, as that's the first installed with
    # "python setup.py install"
    install_requires = ['pandas', 'plotly', 'jupyter', 'scipy', 'seaborn'],

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
