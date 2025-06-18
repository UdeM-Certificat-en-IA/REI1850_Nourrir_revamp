import pytest

@pytest.mark.playwright
def test_navbar_transparency(adopt, server):
    page = adopt
    page.goto(server)
    nav = page.locator('nav')
    assert 'bg-opacity-90' not in nav.get_attribute('class')
    page.evaluate('window.scrollTo(0, 600)')
    page.wait_for_timeout(300)
    assert 'bg-opacity-90' in nav.get_attribute('class')
