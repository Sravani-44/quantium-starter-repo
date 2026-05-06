
import pytest
from dash.testing.application_runners import import_app

def test_chart_renders(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    assert dash_duo.find_element("#sales-chart")