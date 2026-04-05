# pages/login_page.py
# Page Object cho trang /login

from selenium.webdriver.common.by import By
from .base_page import BasePage
from config import BASE_URL


class LoginPage(BasePage):
    # Locators – khớp với Auth.tsx (input[name=email], input[name=password])
    URL = f"{BASE_URL}/login"

    EMAIL_INPUT    = (By.CSS_SELECTOR, "input[name='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[name='password']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button[type='submit']")
    REGISTER_LINK  = (By.CSS_SELECTOR, "a[href='/register']")

    # Thông báo thành công / lỗi do NotificationPopup render
    NOTIFICATION   = (By.CSS_SELECTOR, "[class*='notification'], [class*='Notification']")

    def open_login(self):
        self.open("/login")

    def enter_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def enter_password(self, password: str):
        self.type_text(self.PASSWORD_INPUT, password)

    def submit(self):
        self.click(self.SUBMIT_BTN)

    def login(self, email: str, password: str):
        """Thực hiện đăng nhập hoàn chỉnh và đợi redirect."""
        self.open_login()
        self.enter_email(email)
        self.enter_password(password)
        self.submit()

    def get_notification_text(self) -> str:
        return self.get_text(self.NOTIFICATION)

    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION)

    def click_register_link(self):
        self.click(self.REGISTER_LINK)
