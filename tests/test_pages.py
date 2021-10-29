import pytest

from autoextract_poet import AutoExtractHtml, AutoExtractItemWebPage, AutoExtractWebPage


@pytest.fixture
def auto_extract_html():
    url = "https://example.com"
    html = "<html><body><p>Hello!</p></body></html>"
    return AutoExtractHtml(url, html)


class ConcreteItemWebPage(AutoExtractItemWebPage):
    def to_item(self):
        return "yeah!"


@pytest.mark.parametrize("cls", [AutoExtractWebPage, ConcreteItemWebPage])
def test_auto_extract_web_page_family(auto_extract_html, cls):
    page = cls(auto_extract_html)
    assert page.response == auto_extract_html
    assert page.css("html body p::text").get() == "Hello!"


def test_auto_extract_item_web_page(auto_extract_html):
    with pytest.raises(TypeError):
        AutoExtractItemWebPage(auto_extract_html).to_item()
    assert ConcreteItemWebPage(auto_extract_html).to_item() == "yeah!"
