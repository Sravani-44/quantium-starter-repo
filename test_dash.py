
import pytest
import os
from dash.testing.application_runners import import_app
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

# Auto-install correct chromedriver for your Chrome version
driver_path = ChromeDriverManager().install()
os.environ["PATH"] = os.path.dirname(driver_path) + os.pathsep + os.environ["PATH"]

def test_chart_renders(dash_duo):
    app = import_app("app")
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    assert dash_duo.find_element("#sales-chart")