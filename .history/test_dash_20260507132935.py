
import pytest
import os
from dash.testing.application_runners import import_app

# Set chromedriver path
os.environ["PATH"] = r"C:\Users\sravani3044\.wdm\drivers\chromedriver\win64\147.0.7727.117\chromedriver-win32" + os.pathsep + os.environ["PATH"]

# --- Test 1: Header exists on the page ---
def test_header_exists(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1", timeout=10)
    header = dash_duo.find_element("h1")
    assert header is not None
    assert "Pink Morsel" in header.text

# --- Test 2: Chart exists on the page ---
def test_chart_exists(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None

# --- Test 3: Radio buttons exist with all 5 options ---
def test_region_filter_exists(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    filter_div = dash_duo.find_element("#region-filter")
    assert filter_div is not None
    # Check all 5 options exist
    options = dash_duo.find_elements("#region-filter input")
    assert len(options) == 5

# --- Test 4: Selecting a region updates the chart ---
def test_region_filter_updates_chart(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    # Click the North radio button
    options = dash_duo.find_elements("#region-filter input")
    options[1].click()  # North is second option
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    chart = dash_duo.find_element("#sales-chart")
    assert chart is not None