=========
Changelog
=========

0.3 (2021-08-04)
----------------

* Support for all API page types at the moment
* Introduction of ``_unknown_fields_dict`` and ``AutoExtractAdapter``. Allows
  to extend items with custom attributes and to include in the output
  the returned attributes not yet supported by the existing definitions.
* Initial documentation

0.2.2 (2021-05-29)
------------------

* Page classes for Article, Product and ProductList introduced

0.2.1 (2021-01-27)
------------------

* ``AdditionalProperty`` value as optional to match ``unified-schema``

0.2.0 (2020-12-30)
------------------

* ``AutoExtractProductListData`` page input and ``ProductList`` item
* ``from_dict`` of items no longer fail on unknown attributes,
  they're ignored now
* List attributes now default to ``[]`` instead of ``None``
* CI is switched to github actions
* Python 3.9 is added to CI

0.1.0 (2020-11-19)
------------------

* ``AutoExtractHtml`` page input
* ``AutoExtractWebPage`` and ``AutoExtractItemWebPage`` base page objects

0.0.1 (2020-08-18)
------------------

Initial release.

* Article and Product page inputs
* Article and Product items (and their dependencies)
