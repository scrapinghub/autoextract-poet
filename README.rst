================
autoextract-poet
================

.. image:: https://img.shields.io/pypi/v/autoextract-poet.svg
   :target: https://pypi.python.org/pypi/autoextract-poet
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/autoextract-poet.svg
   :target: https://pypi.python.org/pypi/autoextract-poet
   :alt: Supported Python Versions

.. image:: https://github.com/scrapinghub/autoextract-poet/workflows/tox/badge.svg
   :target: https://github.com/scrapinghub/autoextract-poet/actions
   :alt: Build Status

.. image:: https://codecov.io/github/scrapinghub/autoextract-poet/coverage.svg?branch=master
   :target: https://codecov.io/gh/scrapinghub/autoextract-poet
   :alt: Coverage report

``autoextract-poet`` contains common item definitions.
Such items can be extracted automatically using `Zyte AutoExtract API`_
(you can use `scrapy-poet`_ and `scrapy-autoextract`_ for this).

License is BSD 3-clause.

* Documentation: https://autoextract-poet.readthedocs.io/
* Source code: https://github.com/scrapinghub/autoextract-poet
* Issue tracker: https://github.com/scrapinghub/autoextract-poet/issues

.. _`scrapy-poet`: https://scrapy-poet.readthedocs.io/en/stable/
.. _`scrapy-autoextract`: https://github.com/scrapinghub/scrapy-autoextract
.. _`Zyte AutoExtract API`: https://docs.zyte.com/automatic-extraction.html


Developing
**********

Setup your local Python environment via:

1. `pip install -r requirements-dev.txt`
2. `pre-commit install`

Now everytime you perform a `git commit`, these tools will run against the staged files:

* `black`
* `isort`
* `flake8`

You can also directly invoke `pre-commit run --all-files` to run them without performing a commit.
