import attr

from autoextract_poet.page_inputs import AutoExtractHtml
from web_poet import Injectable, ItemPage
from web_poet.mixins import ResponseShortcutsMixin


@attr.s(auto_attribs=True)
class AutoExtractWebPage(Injectable, ResponseShortcutsMixin):
    """Base Page Object which requires :class:`~.AutoExtractHtml`
    and provides XPath / CSS shortcuts.

    Use this class as a base class for Page Objects which work on
    the browser HTML provided by AutoExtract.
    """
    response: AutoExtractHtml


@attr.s(auto_attribs=True)
class AutoExtractItemWebPage(AutoExtractWebPage, ItemPage):
    """:class:`AutoExtractWebPage` that requires the :meth:`to_item` method to
    be implemented.
    """
    pass
