import pytest

from autoextract_poet.page_inputs import AutoExtractHtml
from autoextract_poet.pages import AutoExtractWebPage, AutoExtractItemWebPage


@pytest.fixture
def auto_extract_html():
    url = "https://example.com"
    html = "<html><body><p>Hello!</p></body></html>"
    return AutoExtractHtml(url, html)


@pytest.mark.parametrize("cls", [AutoExtractWebPage, AutoExtractItemWebPage])
def test_auto_extract_web_page_family(auto_extract_html, cls):
    page = cls(auto_extract_html)
    assert  page.response == auto_extract_html
    assert page.css("html body p::text").get() == "Hello!"


def test_auto_extract_item_web_page(auto_extract_html):
    with pytest.raises(TypeError):
        AutoExtractItemWebPage(auto_extract_html).to_item()

    class ItemWebPage(AutoExtractItemWebPage):
        def to_item(self):
            return "yeah!"

    assert ItemWebPage(auto_extract_html).to_item() == "yeah!"
