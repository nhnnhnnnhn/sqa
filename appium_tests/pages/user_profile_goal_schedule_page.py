# pages/user_profile_goal_schedule_page.py
# Page Object cho User Profile, Goals và Study Schedule

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import BASE_URL


class UserProfileGoalSchedulePage(BasePage):
    PROFILE_URL = f"{BASE_URL}/my-account"
    GOAL_URL = f"{BASE_URL}/my-account/user-goal"
    SCHEDULE_URL = f"{BASE_URL}/schedule/study"

    # -------------------------
    # Profile
    # -------------------------
    PROFILE_HEADING = (By.XPATH, "//*[contains(normalize-space(.), 'Hồ Sơ Của Tôi')]")
    PROFILE_SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu thay đổi')]")
    PROFILE_NAME_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    PROFILE_EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='email']")
    PROFILE_DOB_INPUT = (By.CSS_SELECTOR, "input[name='dob']")

    # -------------------------
    # Goals
    # -------------------------
    GOAL_TAB = (By.CSS_SELECTOR, "a[href='/my-account/user-goal']")
    GOAL_TARGET_INPUT = (By.CSS_SELECTOR, "input[name='target_score']")
    GOAL_DEADLINE_INPUT = (By.CSS_SELECTOR, "input[name='deadline']")
    GOAL_SUBJECT_SELECT = (By.CSS_SELECTOR, "select[name='subject_id']")
    GOAL_CREATE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tạo mục tiêu')]")
    GOAL_ROWS = (By.XPATH, "//table/tbody/tr")
    GOAL_ERROR_TEXT = (By.CSS_SELECTOR, "p[class*='error'], [class*='error']")

    # -------------------------
    # Schedule
    # -------------------------
    SCHEDULE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Danh sách lịch học')]")
    SCHEDULE_ADD_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tạo lịch học')]")
    SCHEDULE_MODAL_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Tạo lịch học mới')]")

    SCHEDULE_FORM_TITLE = (By.CSS_SELECTOR, "input[name='title']")
    SCHEDULE_FORM_DESCRIPTION = (By.CSS_SELECTOR, "textarea[name='description']")
    SCHEDULE_FORM_START = (By.CSS_SELECTOR, "input[name='start_time']")
    SCHEDULE_FORM_END = (By.CSS_SELECTOR, "input[name='end_time']")
    SCHEDULE_FORM_TARGET = (By.CSS_SELECTOR, "input[name='target_question']")
    SCHEDULE_FORM_SUBJECT = (By.CSS_SELECTOR, "select[name='subject_id']")

    SCHEDULE_CREATE_SUBMIT = (By.XPATH, "//button[contains(normalize-space(.), 'Tạo lịch học')]")
    SCHEDULE_EDIT_SUBMIT = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu')]")

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def _set_input_value_via_js(self, locator: tuple, value: str):
        element = self.wait_for_visible(locator, timeout=8)
        self.driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', {bubbles: true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
            element,
            value,
        )

    # -------------------------
    # Profile methods
    # -------------------------
    def open_profile(self):
        self.driver.get(self.PROFILE_URL)
        self.wait_for_url_contains("/my-account")
        self.wait_for_visible(self.PROFILE_HEADING, timeout=12)

    def is_profile_page(self) -> bool:
        return "/my-account" in self.get_current_url() and "/user-goal" not in self.get_current_url()

    def toggle_edit_field(self, field_name: str):
        script = """
        const field = arguments[0];
        const input = document.querySelector(`input[name="${field}"]`);
        if (!input) return false;
        const group = input.closest('div');
        if (!group) return false;
        const btn = group.querySelector('button');
        if (!btn) return false;
        btn.click();
        return true;
        """
        ok = bool(self.driver.execute_script(script, field_name))
        if not ok:
            raise RuntimeError(f"Không bật được mode edit cho field={field_name}")

    def set_profile_name(self, value: str):
        self.type_text(self.PROFILE_NAME_INPUT, value)

    def set_profile_email(self, value: str):
        self.type_text(self.PROFILE_EMAIL_INPUT, value)

    def set_profile_dob(self, value: str):
        self._set_input_value_via_js(self.PROFILE_DOB_INPUT, value)

    def submit_profile(self):
        self.click(self.PROFILE_SAVE_BUTTON)

    def wait_alert_and_accept(self, timeout: int = 8) -> str | None:
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            text = (alert.text or "").strip()
            alert.accept()
            return text
        except Exception:
            return None

    # -------------------------
    # Goal methods
    # -------------------------
    def open_goal_page(self):
        self.driver.get(self.GOAL_URL)
        self.wait_for_url_contains("/my-account/user-goal")
        self.wait_for_visible(self.GOAL_TARGET_INPUT, timeout=12)

    def is_goal_page(self) -> bool:
        return "/my-account/user-goal" in self.get_current_url()

    def get_goal_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.GOAL_ROWS))
        except Exception:
            return 0

    def get_first_subject_id(self) -> int | None:
        select_el = self.wait_for_visible(self.GOAL_SUBJECT_SELECT, timeout=8)
        select_obj = Select(select_el)
        for option in select_obj.options:
            value = (option.get_attribute("value") or "").strip()
            if value:
                try:
                    return int(value)
                except Exception:
                    continue
        return None

    def create_goal(self, *, target_score: str, deadline_local: str, subject_id: int):
        self.type_text(self.GOAL_TARGET_INPUT, target_score)
        self._set_input_value_via_js(self.GOAL_DEADLINE_INPUT, deadline_local)
        select_el = self.wait_for_visible(self.GOAL_SUBJECT_SELECT, timeout=8)
        Select(select_el).select_by_value(str(subject_id))
        self.click(self.GOAL_CREATE_BUTTON)

    def get_goal_error_text(self) -> str:
        try:
            element = self.wait_for_visible(self.GOAL_ERROR_TEXT, timeout=4)
            return (element.text or "").strip()
        except Exception:
            return ""

    # -------------------------
    # Schedule methods
    # -------------------------
    def open_schedule_page(self):
        self.driver.get(self.SCHEDULE_URL)
        self.wait_for_url_contains("/schedule/study")
        self.wait_for_visible(self.SCHEDULE_TITLE, timeout=12)

    def is_schedule_page(self) -> bool:
        return "/schedule/study" in self.get_current_url()

    def open_create_schedule_modal(self):
        self.click(self.SCHEDULE_ADD_BUTTON)
        self.wait_for_visible(self.SCHEDULE_MODAL_TITLE, timeout=10)

    def fill_schedule_form(
        self,
        *,
        title: str,
        description: str,
        start_local: str,
        end_local: str,
        target_question: int,
        subject_id: int,
    ):
        self.type_text(self.SCHEDULE_FORM_TITLE, title)
        self.type_text(self.SCHEDULE_FORM_DESCRIPTION, description)
        self._set_input_value_via_js(self.SCHEDULE_FORM_START, start_local)
        self._set_input_value_via_js(self.SCHEDULE_FORM_END, end_local)
        self.type_text(self.SCHEDULE_FORM_TARGET, str(target_question))
        select_el = self.wait_for_visible(self.SCHEDULE_FORM_SUBJECT, timeout=8)
        Select(select_el).select_by_value(str(subject_id))

    def submit_create_schedule(self):
        self.click(self.SCHEDULE_CREATE_SUBMIT)

    def submit_edit_schedule(self):
        self.click(self.SCHEDULE_EDIT_SUBMIT)

    def has_schedule_card(self, title: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(title)
        locator = (By.XPATH, f"//li[.//h3[contains(normalize-space(.), {literal})]]")
        return self.is_visible(locator, timeout=timeout)

    def open_edit_schedule_by_title(self, title: str):
        literal = self._xpath_literal(title)
        locator = (
            By.XPATH,
            f"//li[.//h3[contains(normalize-space(.), {literal})]]//span[contains(@class,'edit_icon')]",
        )
        self.click(locator)
        self.wait_for_visible(self.SCHEDULE_MODAL_TITLE, timeout=10)

    def get_schedule_form_subject_first_valid(self) -> int | None:
        select_el = self.wait_for_visible(self.SCHEDULE_FORM_SUBJECT, timeout=8)
        select_obj = Select(select_el)
        for option in select_obj.options:
            value = (option.get_attribute("value") or "").strip()
            if value:
                try:
                    return int(value)
                except Exception:
                    continue
        return None
