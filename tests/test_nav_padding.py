import pytest

@pytest.mark.playwright
def test_navbar_padding_changes_on_scroll(adopt, server):
    page = adopt
    page.goto(server)
    nav = page.locator('nav')
    cls = nav.get_attribute('class')
    assert 'py-6' in cls
    page.evaluate('window.scrollTo(0, 600)')
    page.wait_for_timeout(300)
    cls_after = nav.get_attribute('class')
    assert 'py-2' in cls_after
