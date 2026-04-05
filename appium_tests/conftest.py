# conftest.py
# Appium session management – pytest fixtures dùng chung cho toàn bộ test suite

import pytest
from appium import webdriver
from appium.options.android.uiautomator2.base import UiAutomator2Options
from selenium.webdriver.support.ui import WebDriverWait

from config import APPIUM_SERVER_URL, DESIRED_CAPS, IMPLICIT_WAIT, EXPLICIT_WAIT, PAGE_LOAD_TIMEOUT


# ──────────────────────────────────────────────
# Session-level driver (dùng chung cả session)
# Mỗi lần chạy pytest chỉ mở browser 1 lần
# ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def driver():
    """Khởi tạo Appium WebDriver, yield cho tests, rồi quit sau khi xong."""
    options = UiAutomator2Options()
    for key, value in DESIRED_CAPS.items():
        options.set_capability(key, value)

    _driver = webdriver.Remote(
        command_executor=APPIUM_SERVER_URL,
        options=options,
    )
    _driver.implicitly_wait(IMPLICIT_WAIT)
    _driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)

    yield _driver

    _driver.quit()


# ──────────────────────────────────────────────
# Explicit wait helper
# ──────────────────────────────────────────────
@pytest.fixture(scope="session")
def wait(driver):
    """WebDriverWait gắn với driver, dùng lại trong các test."""
    return WebDriverWait(driver, EXPLICIT_WAIT)


# ──────────────────────────────────────────────
# Tự động chụp screenshot khi test FAIL
# ──────────────────────────────────────────────
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver_fixture = item.funcargs.get("driver")
        if driver_fixture:
            screenshot_name = f"screenshots/{item.nodeid.replace('/', '_').replace('::', '_')}.png"
            import os
            os.makedirs("screenshots", exist_ok=True)
            try:
                driver_fixture.save_screenshot(screenshot_name)
                print(f"\n[Screenshot saved] {screenshot_name}")
            except Exception as e:
                print(f"\n[Screenshot failed] {e}")
