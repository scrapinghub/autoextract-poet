from autoextract_poet.page_inputs import AutoExtractHtml
from autoextract_poet.pages import AutoExtractWebPage


def test_auto_extract_web_page():
    url = "https://example.com"
    html = "<html><body><p>Hello!</p></body></html>"
    response_data = AutoExtractHtml(url, html)
    page = AutoExtractWebPage(response_data)
    assert  page.response == response_data
    assert page.css("html body p::text").get() == "Hello!"
