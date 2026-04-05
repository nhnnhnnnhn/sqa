# pages/admin_exam_management_page.py
# Page Object cho Admin Exam Schedule & Exam Management

from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminExamManagementPage(BasePage):
    SCHEDULE_URL = f"{ADMIN_BASE_URL}/admin/schedules"
    EXAM_URL = f"{ADMIN_BASE_URL}/admin/exams"
    CREATE_EXAM_URL = f"{ADMIN_BASE_URL}/admin/exams/create"

    # Schedule list page
    SCHEDULE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ LỊCH THI')]")
    ADD_SCHEDULE_BTN = (By.XPATH, "//button[contains(normalize-space(.), '+ Thêm lịch thi')]")
    SCHEDULE_MODAL_TITLE = (
        By.XPATH,
        "//h2[contains(normalize-space(.), 'Tạo lịch thi') or contains(normalize-space(.), 'Cập nhật lịch thi')]",
    )
    START_TIME_INPUT = (By.CSS_SELECTOR, "input[name='start_time']")
    END_TIME_INPUT = (By.CSS_SELECTOR, "input[name='end_time']")
    SCHEDULE_SUBMIT_BTN = (
        By.XPATH,
        "//button[contains(normalize-space(.), 'Tạo lịch thi') or contains(normalize-space(.), 'Cập nhật') or contains(normalize-space(.), 'Đang lưu')]",
    )
    FROM_DATE_INPUT = (By.XPATH, "(//label[contains(normalize-space(.), 'Từ ngày')]/following::input[@type='date'])[1]")
    TO_DATE_INPUT = (By.XPATH, "(//label[contains(normalize-space(.), 'Đến ngày')]/following::input[@type='date'])[1]")
    SCHEDULE_FILTER_BTN = (By.XPATH, "//button[normalize-space(.)='Lọc']")
    SCHEDULE_RESET_FILTER_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Đặt lại')]")
    SCHEDULE_FIRST_EDIT_BTN = (By.XPATH, "(//table//tbody//tr//button[contains(normalize-space(.), 'Sửa')])[1]")
    SCHEDULE_FIRST_ROW = (By.XPATH, "(//table//tbody//tr)[1]")

    # Exam list page
    EXAM_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ CUỘC THI')]")
    ADD_EXAM_BTN = (By.XPATH, "//button[contains(normalize-space(.), '+ Thêm bài thi')]")
    EXAM_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo tên đề thi']")
    EXAM_SEARCH_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    EXAM_EMPTY_ROW = (By.XPATH, "//td[contains(normalize-space(.), 'Không có bài thi phù hợp')]")

    # Create exam page
    CREATE_EXAM_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Tạo bài thi mới')]")
    EXAM_NAME_INPUT = (By.XPATH, "//label[contains(normalize-space(.), 'Tên bài thi')]/following::input[1]")
    EXAM_DESC_TEXTAREA = (By.XPATH, "//label[contains(normalize-space(.), 'Mô tả')]/following::textarea[1]")
    EXAM_TIME_LIMIT_INPUT = (
        By.XPATH,
        "//label[contains(normalize-space(.), 'Thời gian (phút)')]/following::input[1]",
    )
    EXAM_SUBJECT_SELECT = (By.XPATH, "//label[contains(normalize-space(.), 'Môn học')]/following::select[1]")
    EXAM_TOPIC_SELECT = (By.XPATH, "//label[contains(normalize-space(.), 'Chủ đề')]/following::select[1]")
    EXAM_SCHEDULE_SELECT = (By.XPATH, "//label[contains(normalize-space(.), 'Lịch thi')]/following::select[1]")
    SAVE_EXAM_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu bài thi')]")

    # Assign question page
    ASSIGN_QUESTION_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Tạo câu hỏi cho bài thi')]")
    ASSIGN_COMPLETE_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Hoàn thành')]")
    ASSIGN_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo nội dung câu hỏi']")
    ASSIGN_SEARCH_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    FIRST_ASSIGN_CHECKBOX = (By.XPATH, "(//input[@type='checkbox'])[1]")

    # Exam detail page
    EXAM_DETAIL_HEADER = (By.XPATH, "//div[contains(@class, 'exam_header')]//h2")
    CHANGE_QUESTION_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Thay đổi câu hỏi')]")

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

    def _row_by_exam_name_xpath(self, exam_name: str) -> str:
        literal = self._xpath_literal(exam_name)
        return f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]"

    def _set_datetime_local(self, locator: tuple, value: str):
        # value format: YYYY-MM-DDTHH:MM
        el = self.wait_for_visible(locator, timeout=10)
        self.driver.execute_script(
            """
            const input = arguments[0];
            const value = arguments[1];
            input.scrollIntoView({block: 'center'});
            input.removeAttribute('readonly');
            input.focus();
            input.value = '';
            input.value = value;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            input.dispatchEvent(new Event('blur', { bubbles: true }));
            """,
            el,
            value,
        )

        actual_value = (el.get_attribute("value") or "").strip()
        if actual_value != value:
            el.clear()
            el.send_keys(value)

    def _set_schedule_datetimes(self, start_time_local: str, end_time_local: str):
        start_el = self.wait_for_visible(self.START_TIME_INPUT, timeout=10)
        end_el = self.wait_for_visible(self.END_TIME_INPUT, timeout=10)
        self.driver.execute_script(
            """
            const nativeSetter = Object.getOwnPropertyDescriptor(
              window.HTMLInputElement.prototype,
              'value'
            ).set;

            function updateInput(input, value) {
              input.scrollIntoView({ block: 'center' });
              input.removeAttribute('readonly');
              input.focus();
              nativeSetter.call(input, value);
              input.dispatchEvent(new Event('input', { bubbles: true }));
              input.dispatchEvent(new Event('change', { bubbles: true }));
            }

            updateInput(arguments[0], arguments[2]);
            updateInput(arguments[1], arguments[3]);
            arguments[1].blur();
            """,
            start_el,
            end_el,
            start_time_local,
            end_time_local,
        )

        actual_start = (start_el.get_attribute("value") or "").strip()
        actual_end = (end_el.get_attribute("value") or "").strip()

        if actual_start != start_time_local:
            self._set_datetime_local(self.START_TIME_INPUT, start_time_local)
        if actual_end != end_time_local:
            self._set_datetime_local(self.END_TIME_INPUT, end_time_local)

        start_after = (self.wait_for_visible(self.START_TIME_INPUT, timeout=5).get_attribute("value") or "").strip()
        end_after = (self.wait_for_visible(self.END_TIME_INPUT, timeout=5).get_attribute("value") or "").strip()
        if start_after != start_time_local or end_after != end_time_local:
            raise AssertionError(
                f"Khong giu duoc gia tri schedule inputs: start={start_after}, end={end_after}"
            )

    # -------------------------
    # Schedule management
    # -------------------------
    def open_schedule_management(self):
        self.driver.get(self.SCHEDULE_URL)
        self.wait_for_url_contains("/admin/schedules")
        self.wait_for_visible(self.SCHEDULE_TITLE, timeout=12)

    def is_schedule_management_page(self) -> bool:
        return "/admin/schedules" in self.get_current_url() and "/detail/" not in self.get_current_url()

    def open_add_schedule_modal(self):
        self.click(self.ADD_SCHEDULE_BTN)
        self.wait_for_visible(self.SCHEDULE_MODAL_TITLE, timeout=10)

    def is_schedule_modal_visible(self) -> bool:
        return self.is_visible(self.SCHEDULE_MODAL_TITLE, timeout=4)

    def fill_schedule_times(self, start_time_local: str, end_time_local: str):
        self._set_schedule_datetimes(start_time_local, end_time_local)

    def submit_schedule(self):
        self.click(self.SCHEDULE_SUBMIT_BTN)

    def set_schedule_date_filter(self, from_date: str, to_date: str):
        # date format: YYYY-MM-DD
        from_el = self.wait_for_visible(self.FROM_DATE_INPUT, timeout=8)
        to_el = self.wait_for_visible(self.TO_DATE_INPUT, timeout=8)
        from_el.clear()
        from_el.send_keys(from_date)
        to_el.clear()
        to_el.send_keys(to_date)

    def apply_schedule_filter(self):
        self.click(self.SCHEDULE_FILTER_BTN)

    def reset_schedule_filter(self):
        self.click(self.SCHEDULE_RESET_FILTER_BTN)

    def click_first_schedule_edit(self):
        self.click(self.SCHEDULE_FIRST_EDIT_BTN)
        self.wait_for_visible(self.SCHEDULE_MODAL_TITLE, timeout=10)

    def is_any_schedule_row_visible(self) -> bool:
        return self.is_visible(self.SCHEDULE_FIRST_ROW, timeout=5)

    # -------------------------
    # Exam management
    # -------------------------
    def open_exam_management(self):
        self.driver.get(self.EXAM_URL)
        self.wait_for_url_contains("/admin/exams")
        self.wait_for_visible(self.EXAM_TITLE, timeout=12)

    def is_exam_management_page(self) -> bool:
        url = self.get_current_url()
        return "/admin/exams" in url and "/create" not in url and "/detail/" not in url

    def search_exam(self, keyword: str):
        self.type_text(self.EXAM_SEARCH_INPUT, keyword)
        self.click(self.EXAM_SEARCH_BTN)
        try:
            WebDriverWait(self.driver, 8).until(
                lambda d: keyword.lower() in (d.page_source or "").lower()
                or self.is_visible(self.EXAM_EMPTY_ROW, timeout=1)
            )
        except Exception:
            pass

    def has_exam_row(self, exam_name: str, timeout: int = 5) -> bool:
        locator = (By.XPATH, self._row_by_exam_name_xpath(exam_name))
        return self.is_visible(locator, timeout=timeout)

    def get_exam_status_text(self, exam_name: str) -> str:
        row_xpath = self._row_by_exam_name_xpath(exam_name)
        locator = (
            By.XPATH,
            f"{row_xpath}/td[7]",
        )
        return (self.get_text(locator) or "").strip()

    def toggle_exam_available_by_name(self, exam_name: str):
        row_xpath = self._row_by_exam_name_xpath(exam_name)
        edit_icon = (
            By.XPATH,
            f"{row_xpath}//span[contains(@class, 'editIcon')]",
        )
        before = self.get_exam_status_text(exam_name)
        self.click(edit_icon)
        WebDriverWait(self.driver, 10).until(
            lambda _d: self.get_exam_status_text(exam_name) != before
        )

    def delete_exam_by_name(self, exam_name: str):
        row_xpath = self._row_by_exam_name_xpath(exam_name)
        delete_btn = (
            By.XPATH,
            f"{row_xpath}//button[contains(normalize-space(.), 'Xóa')]",
        )
        self.click(delete_btn)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda _d: not self.has_exam_row(exam_name, timeout=1)
            )
        except Exception:
            pass

    def open_create_exam(self):
        self.click(self.ADD_EXAM_BTN)
        self.wait_for_url_contains("/admin/exams/create")
        self.wait_for_visible(self.CREATE_EXAM_TITLE, timeout=12)

    def fill_exam_form(
        self,
        *,
        exam_name: str,
        description: str,
        time_limit: int,
        subject_id: int,
        topic_id: int,
        schedule_id: int,
    ):
        self.type_text(self.EXAM_NAME_INPUT, exam_name)
        self.type_text(self.EXAM_DESC_TEXTAREA, description)
        self.type_text(self.EXAM_TIME_LIMIT_INPUT, str(time_limit))

        Select(self.wait_for_visible(self.EXAM_SUBJECT_SELECT, timeout=8)).select_by_value(str(subject_id))
        Select(self.wait_for_visible(self.EXAM_TOPIC_SELECT, timeout=8)).select_by_value(str(topic_id))
        Select(self.wait_for_visible(self.EXAM_SCHEDULE_SELECT, timeout=8)).select_by_value(str(schedule_id))

    def submit_create_exam(self):
        self.click(self.SAVE_EXAM_BTN)

    # -------------------------
    # Question assignment
    # -------------------------
    def open_exam_question_assignment(self, exam_id: int):
        self.driver.get(f"{ADMIN_BASE_URL}/admin/exams/create/{exam_id}/questions")
        self.wait_for_url_contains(f"/admin/exams/create/{exam_id}/questions")
        self.wait_for_visible(self.ASSIGN_QUESTION_TITLE, timeout=12)

    def search_question_to_assign(self, keyword: str):
        self.type_text(self.ASSIGN_SEARCH_INPUT, keyword)
        self.click(self.ASSIGN_SEARCH_BTN)

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
        self.click(self.ASSIGN_COMPLETE_BTN)

    # -------------------------
    # Exam detail
    # -------------------------
    def is_exam_detail_page(self, exam_id: int | None = None) -> bool:
        url = self.get_current_url()
        if exam_id is None:
            return "/admin/exams/detail/" in url
        return f"/admin/exams/detail/{exam_id}" in url

    def wait_exam_detail_loaded(self, timeout: int = 12):
        self.wait_for_visible(self.CHANGE_QUESTION_BTN, timeout=timeout)

    def page_contains_text(self, text: str) -> bool:
        return text.lower() in (self.driver.page_source or "").lower()

    # -------------------------
    # Notification
    # -------------------------
    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION, timeout=4)

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
