# pages/admin_user_page.py
# Page Object cho trang quản lý người dùng admin /admin/users

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminUserPage(BasePage):
    URL = f"{ADMIN_BASE_URL}/admin/users"

    TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ NGƯỜI DÙNG')]")
    LOADING_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Đang tải danh sách người dùng')]")
    USER_TABLE = (By.CSS_SELECTOR, "table")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo tên hoặc email']")
    APPLY_FILTER_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Áp dụng')]")
    RESET_FILTER_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Đặt lại')]")
    EMPTY_ROW = (By.XPATH, "//table//tbody//td[contains(normalize-space(.), 'Không có người dùng')]")
    PAGINATION = (By.CSS_SELECTOR, "[class*='pagination']")
    ACTIVE_PAGE = (By.CSS_SELECTOR, "[class*='pagination'] button[class*='activePage']")

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def open_user_management(self):
        self.driver.get(self.URL)
        self.wait_for_url_contains("/admin/users")

    def is_user_management_page(self) -> bool:
        return "/admin/users" in self.get_current_url()

    def wait_until_loaded(self, timeout: int = 20):
        self.wait_for_url_contains("/admin/users", timeout=timeout)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "Đang tải danh sách người dùng" not in d.page_source
            )
        except Exception:
            pass

    def is_table_or_empty_visible(self) -> bool:
        return self.is_visible(self.USER_TABLE, timeout=8) or self.is_visible(self.EMPTY_ROW, timeout=5)

    def _get_data_rows(self):
        rows = self.driver.find_elements(By.XPATH, "//table//tbody//tr")
        data_rows = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 8:
                data_rows.append(row)
        return data_rows

    def get_user_count_on_current_page(self) -> int:
        if self.is_visible(self.EMPTY_ROW, timeout=2):
            return 0
        return len(self._get_data_rows())

    def get_all_emails_on_current_page(self) -> list[str]:
        emails = []
        for row in self._get_data_rows():
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 3:
                email = (cells[2].text or "").strip()
                if email:
                    emails.append(email)
        return emails

    def search_user(self, keyword: str):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.APPLY_FILTER_BTN)
        self.wait_until_loaded(timeout=12)

    def reset_filter(self):
        self.click(self.RESET_FILTER_BTN)
        self.wait_until_loaded(timeout=12)

    def has_user_row(self, email: str, timeout: int = 3) -> bool:
        locator = (
            By.XPATH,
            f"//table//tbody//tr[td[3][contains(normalize-space(.), {self._xpath_literal(email)})]]",
        )
        return self.is_visible(locator, timeout=timeout)

    def _get_user_row(self, email: str, timeout: int = 8):
        locator = (
            By.XPATH,
            f"//table//tbody//tr[td[3][contains(normalize-space(.), {self._xpath_literal(email)})]]",
        )
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def get_status_label_by_email(self, email: str) -> str:
        row = self._get_user_row(email)
        cells = row.find_elements(By.TAG_NAME, "td")
        status_text = (cells[5].text or "").strip()
        if "Hoạt động" in status_text:
            return "Hoạt động"
        if "Bị khoá" in status_text:
            return "Bị khoá"
        return status_text

    def get_role_label_by_email(self, email: str) -> str:
        row = self._get_user_row(email)
        cells = row.find_elements(By.TAG_NAME, "td")
        role_text = (cells[6].text or "").strip()
        if "Admin" in role_text:
            return "Admin"
        if "Người dùng" in role_text:
            return "Người dùng"
        return role_text

    def toggle_available_by_email(self, email: str) -> tuple[str, str]:
        before = self.get_status_label_by_email(email)
        row = self._get_user_row(email)
        cells = row.find_elements(By.TAG_NAME, "td")
        edit_btn = cells[5].find_element(By.CSS_SELECTOR, "span[class*='editIcon']")
        edit_btn.click()

        WebDriverWait(self.driver, 10).until(
            lambda _d: self.get_status_label_by_email(email) != before
        )
        after = self.get_status_label_by_email(email)
        return before, after

    def change_role_by_email(self, email: str, role_value: str) -> tuple[str, str]:
        before = self.get_role_label_by_email(email)
        row = self._get_user_row(email)
        cells = row.find_elements(By.TAG_NAME, "td")
        edit_btn = cells[6].find_element(By.CSS_SELECTOR, "span[class*='editIcon']")
        edit_btn.click()

        select_el = WebDriverWait(self.driver, 8).until(
            lambda _d: cells[6].find_element(By.TAG_NAME, "select")
        )
        Select(select_el).select_by_value(role_value)

        expected = "Admin" if role_value == "ADMIN" else "Người dùng"
        WebDriverWait(self.driver, 10).until(
            lambda _d: expected in self.get_role_label_by_email(email)
        )
        after = self.get_role_label_by_email(email)
        return before, after

    def delete_user_by_email(self, email: str):
        row = self._get_user_row(email)
        cells = row.find_elements(By.TAG_NAME, "td")
        delete_btn = cells[7].find_element(By.XPATH, ".//button[contains(normalize-space(.), 'Xóa')]")
        delete_btn.click()

        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert.accept()
        except Exception:
            pass

        WebDriverWait(self.driver, 10).until(
            lambda _d: not self.has_user_row(email, timeout=1)
        )

    def get_current_page(self) -> int:
        try:
            active = self.driver.find_element(*self.ACTIVE_PAGE)
            return int((active.text or "1").strip())
        except Exception:
            return 1

    def has_multiple_pages(self) -> bool:
        try:
            page_buttons = self.driver.find_elements(
                By.XPATH,
                "//div[contains(@class, 'pagination')]//button[normalize-space(text())!='']",
            )
            page_numbers = []
            for btn in page_buttons:
                text = (btn.text or "").strip()
                if text.isdigit():
                    page_numbers.append(int(text))
            return max(page_numbers) > 1 if page_numbers else False
        except Exception:
            return False

    def go_to_next_page(self) -> bool:
        before = self.get_current_page()
        next_btn = self.driver.find_element(
            By.XPATH,
            "//div[contains(@class, 'pagination')]//button[last()]",
        )
        if next_btn.get_attribute("disabled"):
            return False

        next_btn.click()
        WebDriverWait(self.driver, 10).until(
            lambda _d: self.get_current_page() != before
        )
        return True
