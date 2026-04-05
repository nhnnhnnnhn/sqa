# pages/admin_login_page.py
# Page Object cho trang đăng nhập admin /admin/login

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL, EXPLICIT_WAIT


class AdminLoginPage(BasePage):
    URL = f"{ADMIN_BASE_URL}/admin/login"

    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_BTN = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Đăng nhập')]")
    NOTIFICATION = (
        By.CSS_SELECTOR,
        "[class*='noti'], [class*='popup'], [class*='notification'], [class*='error'], [class*='warning']",
    )

    def open_login(self):
        self.driver.get(self.URL)
        self.wait_for_url_contains("/admin/login")

    def is_login_form_visible(self) -> bool:
        return (
            self.is_visible(self.LOGIN_TITLE, timeout=5)
            and self.is_visible(self.EMAIL_INPUT, timeout=5)
            and self.is_visible(self.PASSWORD_INPUT, timeout=5)
            and self.is_visible(self.SUBMIT_BTN, timeout=5)
        )

    def login(self, email: str, password: str):
        self.open_login()
        self.type_text(self.EMAIL_INPUT, email)
        password_input = self.wait_for_visible(self.PASSWORD_INPUT)
        password_input.clear()
        password_input.send_keys(password)
        self._submit_login_form(password_input)

    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION, timeout=5)

    def get_notification_text(self) -> str:
        try:
            return self.get_text(self.NOTIFICATION)
        except Exception:
            return ""

    def _submit_login_form(self, password_input):
        current_url = self.get_current_url()

        try:
            password_input.send_keys(Keys.ENTER)
            if self._login_result_observed(current_url, timeout=3):
                return
        except Exception:
            pass

        try:
            submit_button = WebDriverWait(self.driver, EXPLICIT_WAIT).until(
                EC.presence_of_element_located(self.SUBMIT_BTN)
            )
            self.driver.execute_script(
                """
                const button = arguments[0];
                const form = button.closest("form");
                if (form && typeof form.requestSubmit === "function") {
                    form.requestSubmit();
                    return;
                }
                if (form) {
                    form.submit();
                    return;
                }
                button.click();
                """,
                submit_button,
            )
            if self._login_result_observed(current_url, timeout=3):
                return
        except Exception:
            pass

        self.click(self.SUBMIT_BTN)

    def _login_result_observed(self, old_url: str, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.current_url != old_url or self.is_notification_visible()
            )
            return True
        except Exception:
            return False
