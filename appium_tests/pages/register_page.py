# pages/register_page.py
# Page Object cho trang /register

from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class RegisterPage(BasePage):
    URL = f"{BASE_URL}/register"

    NAME_INPUT     = (By.CSS_SELECTOR, "input[name='name'], input[name='fullName'], input[name='user_name'], input[placeholder*='tên'], input[placeholder*='đăng nhập'], input[placeholder*='name']")
    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    CONFIRM_INPUT  = (By.CSS_SELECTOR, "input[name='confirmPassword'], input[name='confirm_password'], input[name='rePassword']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button[type='submit']")
    LOGIN_LINK     = (By.CSS_SELECTOR, "a[href='/login']")

    # Thông báo / lỗi
    NOTIFICATION   = (By.CSS_SELECTOR, "[class*='notification'], [class*='Notification'], [class*='toast'], [class*='error']")
    FIELD_ERROR    = (By.CSS_SELECTOR, "[class*='error'], [class*='invalid'], p[class*='help']")

    def open_register(self):
        self.open("/register")

    def fill_form(self, name: str, email: str, password: str, confirm: str = None):
        if self.is_visible(self.NAME_INPUT, timeout=3):
            self.type_text(self.NAME_INPUT, name)
        self.type_text(self.EMAIL_INPUT, email)
        self.type_text(self.PASSWORD_INPUT, password)
        if confirm and self.is_visible(self.CONFIRM_INPUT, timeout=3):
            self.type_text(self.CONFIRM_INPUT, confirm)

    def submit(self):
        self.click(self.SUBMIT_BTN)

    def register(self, name: str, email: str, password: str, confirm: str = None):
        self.open_register()
        self.fill_form(name, email, password, confirm or password)
        self.submit()

    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION, timeout=5)

    def get_notification_text(self) -> str:
        try:
            return self.get_text(self.NOTIFICATION)
        except Exception:
            return ""

    def has_field_error(self) -> bool:
        return self.is_visible(self.FIELD_ERROR, timeout=5)
