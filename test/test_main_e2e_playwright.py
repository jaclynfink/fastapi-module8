import os
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from playwright.sync_api import expect, sync_playwright


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _wait_for_server(base_url: str, timeout_seconds: float = 15.0) -> None:
    deadline = time.time() + timeout_seconds
    health_url = f"{base_url}/health"

    while time.time() < deadline:
        try:
            with urlopen(health_url, timeout=1.0) as response:
                if response.status == 200:
                    return
        except URLError:
            time.sleep(0.2)

    raise RuntimeError(f"Server did not become ready at {health_url}")


@pytest.fixture(scope="module")
def live_server_url():
    port = _find_free_port()
    base_url = f"http://127.0.0.1:{port}"

    env = os.environ.copy()
    env["PYTHONPATH"] = str(os.getcwd()) + os.pathsep + env.get("PYTHONPATH", "")

    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
    )

    try:
        _wait_for_server(base_url)
        yield base_url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()


@pytest.fixture(scope="module")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            yield page
        finally:
            page.close()
            browser.close()


def test_home_page_loads(browser_page, live_server_url):
    browser_page.goto(live_server_url)

    expect(browser_page.locator("h1")).to_have_text("Hello World")
    expect(browser_page.locator("h2")).to_have_text("Calculator")


@pytest.mark.parametrize(
    "button_name,a,b,expected_value",
    [
        ("Add", "2", "3", 5.0),
        ("Subtract", "9", "4", 5.0),
        ("Multiply", "6", "7", 42.0),
        ("Divide", "8", "2", 4.0),
    ],
)
def test_calculator_operations(browser_page, live_server_url, button_name, a, b, expected_value):
    browser_page.goto(live_server_url)

    browser_page.fill("#a", a)
    browser_page.fill("#b", b)
    browser_page.get_by_role("button", name=button_name).click()

    result_locator = browser_page.locator("#result")
    expect(result_locator).to_contain_text("Calculation Result:")
    result_text = result_locator.inner_text()
    result_value = float(result_text.split(":", 1)[1].strip())
    assert result_value == expected_value


def test_divide_by_zero_shows_error(browser_page, live_server_url):
    browser_page.goto(live_server_url)

    browser_page.fill("#a", "5")
    browser_page.fill("#b", "0")
    browser_page.get_by_role("button", name="Divide").click()

    expect(browser_page.locator("#result")).to_have_text("Error: Cannot divide by zero!")
