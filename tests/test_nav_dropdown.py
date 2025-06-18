import pytest

@pytest.mark.playwright
def test_performance_sections_dropdown(adopt, server):
    page = adopt
    page.goto(f"{server}/performance")
    label = page.locator('label', has_text='Sections')
    label.click()
    dropdown = page.locator('ul.dropdown-content')
    dropdown.wait_for(state='visible')
    assert dropdown.locator('a', has_text='Phase').count() > 0
