PyClonal
========

A Jupyter Notebook to analyze T-cell Receptor Sequencing

Goal
----

-  Provide an interactive set of Jupyter notebooks for easily
   visualizing and analyzing TCR sequencing data using existing tools
   and methods.

Background
----------

-  T cells are immune cells that recognize their targets through the
   T-cell receptor (TCR) - a complex of highly variable cell-surface
   proteins. Analyzing the TCR repertoire in humans or mouse models can
   help us understand the development of the immune system and
   progression of disease.

-  There are a growing pool of biologists and clinicians that want to be
   able to analyze the mass amounts of data they are collecting, or that
   others have collected and published. These notebooks will provide a
   tool for this community to use and interact with T-cell receptor
   sequencing data.

-  There has been a lot of development of methods for analyzing T-cell
   receptor data, a lot of which borrows from the field of ecology and
   associated diversity analyses. However, the tools developed for these
   analyses are all in different locations and not easy to access! We
   are solving that problem here.

Installation
------------

Dependencies: ``pandas``, ``jupyter``, ``plotly``

For now the recommended way to install is using ``pipenv``:

-  install ``pipenv`` (`installation
   instructions <https://docs.pipenv.org/install/>`__)
-  clone ``PyClonal`` repo:

   ::

       $ git clone https://github.com/NCBI-Hackathons/PyClonal.git

-  create virtual environment inside ``PyClonal`` directory

   ::

       $ cd PyClonal
       $ pipenv --three

-  activate virtualenv and install ``PyClonal`` (this will install all
   necessary dependencies)

   ::

       $ pipenv shell
       $ pip install -e .

Resources and Existing TCR tools to gather from:
------------------------------------------------

-VDJ tools -https://vdjtools-doc.readthedocs.io/en/master/

-VDJviz: a versatile immune repertoire browser -https://vdjviz.cdr3.net/

-tcR
-https://cran.r-project.org/web/packages/tcR/vignettes/tcrvignette.html

-miXCR -https://mixcr.readthedocs.io/en/master/

-powerTCR -https://www.biorxiv.org/content/early/2018/04/07/297119

-ImmuneDB -http://immunedb.com/

-TraCeR -https://github.com/teichlab/tracer
