# pages/admin_subject_topic_practice_page.py
# Page Object cho Subject, Topic & Practice (Bank) Management

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminSubjectTopicPracticePage(BasePage):
    TOPIC_SUBJECT_URL = f"{ADMIN_BASE_URL}/admin/topic_subject"
    PRACTICE_URL = f"{ADMIN_BASE_URL}/admin/bank"
    CREATE_PRACTICE_URL = f"{ADMIN_BASE_URL}/admin/bank/create"

    # Topic & Subject page
    PAGE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ MÔN & CHUYÊN ĐỀ')]")
    SUBJECT_TAB = (By.XPATH, "//button[contains(normalize-space(.), 'Môn học')]")
    TOPIC_TAB = (By.XPATH, "//button[contains(normalize-space(.), 'Chủ đề')]")

    SUBJECT_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Tên môn học...']")
    SUBJECT_TYPE_SELECT = (By.XPATH, "(//h2[contains(normalize-space(.), 'Môn học')]/following::select)[1]")
    SUBJECT_ADD_BUTTON = (By.XPATH, "//h2[contains(normalize-space(.), 'Môn học')]/following::button[contains(normalize-space(.), 'Thêm')][1]")

    TOPIC_TITLE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Tiêu đề...']")
    TOPIC_DESC_INPUT = (By.CSS_SELECTOR, "input[placeholder='Mô tả...']")
    TOPIC_SUBJECT_SELECT = (By.XPATH, "(//h2[contains(normalize-space(.), 'Chủ đề')]/following::select)[1]")
    TOPIC_ADD_BUTTON = (By.XPATH, "//h2[contains(normalize-space(.), 'Chủ đề')]/following::button[contains(normalize-space(.), 'Thêm')][1]")

    # Practice management list
    PRACTICE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ LUYỆN TẬP')]")
    ADD_PRACTICE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), '+ Thêm bài luyện tập')]")
    PRACTICE_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo tên đề thi']")
    PRACTICE_SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")

    # Create practice page
    CREATE_PRACTICE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Tạo ngân hàng câu hỏi')]")
    PRACTICE_DESC_TEXTAREA = (By.XPATH, "//label[contains(normalize-space(.), 'Mô tả')]/following::textarea[1]")
    PRACTICE_TIME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), 'Thời gian (phút)')]/following::input[1]")
    PRACTICE_SUBJECT_SELECT = (By.XPATH, "//label[contains(normalize-space(.), 'Môn học')]/following::select[1]")
    PRACTICE_TOPIC_SELECT = (By.XPATH, "//label[contains(normalize-space(.), 'Chủ đề')]/following::select[1]")
    PRACTICE_SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu ngân hàng')]")

    # Practice assign question page
    ASSIGN_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Thêm câu hỏi vào ngân hàng')]")
    ASSIGN_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo nội dung câu hỏi']")
    ASSIGN_SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    ASSIGN_COMPLETE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Hoàn thành')]")
    FIRST_ASSIGN_CHECKBOX = (By.XPATH, "(//input[@type='checkbox'])[1]")

    # Practice detail page
    DETAIL_EDIT_QUESTION_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Chỉnh sửa câu hỏi')]")

    # Generic notification
    NOTIFICATION = (
        By.CSS_SELECTOR,
        "[class*='noti'], [class*='popup'], [class*='notification'], [class*='warning'], [class*='error']",
    )

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # -------------------------
    # Topic/Subject
    # -------------------------
    def open_topic_subject_management(self):
        self.driver.get(self.TOPIC_SUBJECT_URL)
        self.wait_for_url_contains("/admin/topic_subject")
        self.wait_for_visible(self.PAGE_TITLE, timeout=12)

    def is_topic_subject_page(self) -> bool:
        return "/admin/topic_subject" in self.get_current_url()

    def switch_to_subject_tab(self):
        self.click(self.SUBJECT_TAB)

    def switch_to_topic_tab(self):
        self.click(self.TOPIC_TAB)

    def create_subject(self, name: str, subject_type: int = 1):
        self.type_text(self.SUBJECT_NAME_INPUT, name)
        select_el = self.wait_for_visible(self.SUBJECT_TYPE_SELECT, timeout=8)
        Select(select_el).select_by_value(str(subject_type))
        self.click(self.SUBJECT_ADD_BUTTON)

    def has_subject_row(self, subject_name: str, timeout: int = 5) -> bool:
        locator = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {self._xpath_literal(subject_name)})]]",
        )
        return self.is_visible(locator, timeout=timeout)

    def create_topic(self, title: str, description: str, subject_id: int):
        self.type_text(self.TOPIC_TITLE_INPUT, title)
        self.type_text(self.TOPIC_DESC_INPUT, description)
        select_el = self.wait_for_visible(self.TOPIC_SUBJECT_SELECT, timeout=8)
        Select(select_el).select_by_value(str(subject_id))
        self.click(self.TOPIC_ADD_BUTTON)

    def has_topic_row(self, topic_title: str, timeout: int = 5) -> bool:
        locator = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {self._xpath_literal(topic_title)})]]",
        )
        return self.is_visible(locator, timeout=timeout)

    # -------------------------
    # Practice list
    # -------------------------
    def open_practice_management(self):
        self.driver.get(self.PRACTICE_URL)
        self.wait_for_url_contains("/admin/bank")
        self.wait_for_visible(self.PRACTICE_TITLE, timeout=12)

    def is_practice_management_page(self) -> bool:
        url = self.get_current_url()
        return "/admin/bank" in url and "/create" not in url and "/detail/" not in url

    def search_practice(self, keyword: str):
        self.type_text(self.PRACTICE_SEARCH_INPUT, keyword)
        self.click(self.PRACTICE_SEARCH_BUTTON)
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: keyword.lower() in (d.page_source or "").lower()
                or "không có bài thi phù hợp" in (d.page_source or "").lower()
            )
        except Exception:
            pass

    def _practice_row_xpath(self, description: str) -> str:
        literal = self._xpath_literal(description)
        return f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]"

    def has_practice_row(self, description: str, timeout: int = 5) -> bool:
        return self.is_visible((By.XPATH, self._practice_row_xpath(description)), timeout=timeout)

    def get_practice_topic_text(self, description: str) -> str:
        locator = (By.XPATH, f"{self._practice_row_xpath(description)}/td[5]")
        return (self.get_text(locator) or "").strip()

    def delete_practice_by_description(self, description: str):
        delete_btn = (
            By.XPATH,
            f"{self._practice_row_xpath(description)}//button[contains(normalize-space(.), 'Xoá')]",
        )
        self.click(delete_btn)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda _d: not self.has_practice_row(description, timeout=1)
            )
        except Exception:
            pass

    # -------------------------
    # Create practice
    # -------------------------
    def open_create_practice(self):
        self.click(self.ADD_PRACTICE_BUTTON)
        self.wait_for_url_contains("/admin/bank/create")
        self.wait_for_visible(self.CREATE_PRACTICE_TITLE, timeout=12)

    def fill_practice_form(
        self,
        *,
        description: str,
        time_limit: int,
        subject_id: int,
        topic_id: int,
    ):
        self.type_text(self.PRACTICE_DESC_TEXTAREA, description)
        self.type_text(self.PRACTICE_TIME_INPUT, str(time_limit))
        Select(self.wait_for_visible(self.PRACTICE_SUBJECT_SELECT, timeout=8)).select_by_value(str(subject_id))
        Select(self.wait_for_visible(self.PRACTICE_TOPIC_SELECT, timeout=8)).select_by_value(str(topic_id))

    def submit_create_practice(self):
        self.click(self.PRACTICE_SAVE_BUTTON)

    # -------------------------
    # Assign question
    # -------------------------
    def open_practice_question_assignment(self, bank_id: int):
        self.driver.get(f"{ADMIN_BASE_URL}/admin/bank/create/{bank_id}/questions")
        self.wait_for_url_contains(f"/admin/bank/create/{bank_id}/questions")
        self.wait_for_visible(self.ASSIGN_TITLE, timeout=12)

    def search_question_to_assign(self, keyword: str):
        self.type_text(self.ASSIGN_SEARCH_INPUT, keyword)
        self.click(self.ASSIGN_SEARCH_BUTTON)

    def select_question_for_assignment(self, keyword: str | None = None) -> bool:
        if keyword:
            literal = self._xpath_literal(keyword)
            checkbox = (
                By.XPATH,
                f"(//div[contains(@class,'question_card')][.//*[contains(normalize-space(.), {literal})]]//input[@type='checkbox'])[1]",
            )
            if self.is_visible(checkbox, timeout=6):
                self.click(checkbox)
                return True

        if self.is_visible(self.FIRST_ASSIGN_CHECKBOX, timeout=6):
            self.click(self.FIRST_ASSIGN_CHECKBOX)
            return True
        return False

    def complete_question_assignment(self):
        self.click(self.ASSIGN_COMPLETE_BUTTON)

    # -------------------------
    # Practice detail
    # -------------------------
    def is_practice_detail_page(self, bank_id: int | None = None) -> bool:
        url = self.get_current_url()
        if bank_id is None:
            return "/admin/bank/detail/" in url
        return f"/admin/bank/detail/{bank_id}" in url

    def wait_practice_detail_loaded(self, timeout: int = 12):
        self.wait_for_visible(self.DETAIL_EDIT_QUESTION_BUTTON, timeout=timeout)

    def page_contains_text(self, text: str) -> bool:
        return text.lower() in (self.driver.page_source or "").lower()

    # -------------------------
    # Notification
    # -------------------------
    def wait_notification_contains(self, text: str, timeout: int = 8) -> bool:
        needle = (text or "").strip().lower()
        if not needle:
            return False
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: needle in (d.page_source or "").lower()
            )
            return True
        except Exception:
            return False
