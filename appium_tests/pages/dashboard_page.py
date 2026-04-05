# pages/dashboard_page.py
# Page Object cho trang chủ (/) sau khi đăng nhập

from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class DashboardPage(BasePage):
    URL = BASE_URL

    # Nav links – điều chỉnh selector nếu cần sau khi inspect DOM thực tế
    NAV_EXAM       = (By.CSS_SELECTOR, "a[href='/exam']")
    NAV_PRACTICE   = (By.CSS_SELECTOR, "a[href='/practice']")
    NAV_FLASHCARDS = (By.CSS_SELECTOR, "a[href='/flashcards']")
    NAV_DOCUMENT   = (By.CSS_SELECTOR, "a[href='/document']")
    NAV_ANALYTICS  = (By.CSS_SELECTOR, "a[href='/analytics']")
    NAV_SCHEDULE   = (By.CSS_SELECTOR, "a[href='/schedule']")
    NAV_ROADMAP    = (By.CSS_SELECTOR, "a[href='/roadmap']")
    NAV_ACCOUNT    = (By.CSS_SELECTOR, "a[href='/my-account']")

    # Nội dung trang chủ – chứa tên người dùng hoặc greeting
    GREETING       = (By.CSS_SELECTOR, "h1, h2, [class*='greeting'], [class*='welcome']")

    def open_dashboard(self):
        self.open("/")

    def is_logged_in(self) -> bool:
        """Kiểm tra đã đăng nhập: URL phải thuộc BASE_URL và không phải /login."""
        current = self.get_current_url()
        is_on_app = BASE_URL in current
        is_on_login = "/login" in current
        return is_on_app and not is_on_login

    def go_to_exam(self):
        self.click(self.NAV_EXAM)
        self.wait_for_url_contains("/exam")

    def go_to_practice(self):
        self.click(self.NAV_PRACTICE)
        self.wait_for_url_contains("/practice")

    def go_to_flashcards(self):
        self.click(self.NAV_FLASHCARDS)
        self.wait_for_url_contains("/flashcards")

    def go_to_document(self):
        self.click(self.NAV_DOCUMENT)
        self.wait_for_url_contains("/document")

    def go_to_analytics(self):
        self.click(self.NAV_ANALYTICS)
        self.wait_for_url_contains("/analytics")
