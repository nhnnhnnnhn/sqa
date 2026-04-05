# pages/base_page.py
# Lớp cơ sở cho tất cả Page Objects

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import BASE_URL, EXPLICIT_WAIT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, EXPLICIT_WAIT)

    # ── Navigation ──────────────────────────────
    def open(self, path: str = ""):
        self.driver.get(f"{BASE_URL}{path}")

    def get_current_url(self) -> str:
        return self.driver.current_url

    # ── Wait helpers ────────────────────────────
    def wait_for_visible(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_clickable(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    def wait_for_url_contains(self, fragment: str, timeout: int = EXPLICIT_WAIT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_contains(fragment)
        )

    def wait_for_url_to_be(self, url: str, timeout: int = EXPLICIT_WAIT):
        WebDriverWait(self.driver, timeout).until(
            EC.url_to_be(url)
        )

    # ── Element helpers ─────────────────────────
    def find(self, locator: tuple):
        return self.wait_for_visible(locator)

    def click(self, locator: tuple):
        self.wait_for_clickable(locator).click()

    def type_text(self, locator: tuple, text: str, clear: bool = True):
        el = self.wait_for_visible(locator)
        if clear:
            el.clear()
        el.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.wait_for_visible(locator).text

    def is_visible(self, locator: tuple, timeout: int = 5) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def scroll_to_element(self, locator: tuple):
        el = self.wait_for_visible(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)
        return el
