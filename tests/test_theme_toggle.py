import pytest

@pytest.mark.playwright
def test_theme_toggle_persists(adopt, server):
    page = adopt
    page.goto(server)
    html = page.locator('html')
    initial = html.get_attribute('data-theme') or 'light'
    page.click('#theme-toggle')
    page.wait_for_timeout(200)
    toggled = html.get_attribute('data-theme')
    assert toggled and toggled != initial
    page.reload()
    page.wait_for_load_state('networkidle')
    assert html.get_attribute('data-theme') == toggled
