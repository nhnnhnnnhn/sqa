# pages/profile_page.py
# Page Object cho trang hồ sơ cá nhân /my-account, mục tiêu /goals, lịch học /schedule

from selenium.webdriver.common.by import By
from .base_page import BasePage


class ProfilePage(BasePage):
    # ── Hồ sơ cá nhân /my-account ────────────────
    DISPLAY_NAME_INPUT = (By.CSS_SELECTOR, "input[name='name'], input[name='displayName'], input[name='fullName']")
    EMAIL_INPUT        = (By.CSS_SELECTOR, "input[name='email']")
    SAVE_BTN           = (By.CSS_SELECTOR, "button[type='submit'], button[class*='save'], button[class*='Save']")
    NOTIFICATION       = (By.CSS_SELECTOR, "[class*='notification'], [class*='Notification'], [class*='toast']")
    FIELD_ERROR        = (By.CSS_SELECTOR, "[class*='error'], [class*='invalid']")

    # ── Mục tiêu điểm số /goals ────────────────
    ADD_GOAL_BTN       = (By.CSS_SELECTOR, "button[class*='add'], button[class*='Add'], a[href*='add']")
    GOAL_SCORE_INPUT   = (By.CSS_SELECTOR, "input[name='score'], input[name='target'], input[type='number']")
    GOAL_DEADLINE_INPUT= (By.CSS_SELECTOR, "input[name='deadline'], input[type='date']")
    GOAL_SUBJECT_SELECT= (By.CSS_SELECTOR, "select[name='subject'], select[name='subjectId']")
    GOAL_SAVE_BTN      = (By.CSS_SELECTOR, "button[type='submit'], button[class*='save']")
    GOAL_ITEMS         = (By.CSS_SELECTOR, "[class*='goal'], [class*='Goal']")

    # ── Lịch học /schedule ─────────────────────
    ADD_SCHEDULE_BTN   = (By.CSS_SELECTOR, "button[class*='add'], button[class*='Add'], [class*='create']")
    SCHEDULE_ITEMS     = (By.CSS_SELECTOR, "[class*='schedule'], [class*='Schedule'], [class*='event']")
    SCHEDULE_OVERLAP_MSG = (By.CSS_SELECTOR, "[class*='overlap'], [class*='conflict'], [class*='error']")

    def open_profile(self):
        self.open("/my-account")
        self.wait_for_url_contains("/my-account")

    def open_goals(self):
        self.open("/goals")
        self.wait_for_url_contains("/goals")

    def open_schedule(self):
        self.open("/schedule")
        self.wait_for_url_contains("/schedule")

    def update_display_name(self, name: str):
        self.type_text(self.DISPLAY_NAME_INPUT, name)

    def update_email(self, email: str):
        self.type_text(self.EMAIL_INPUT, email)

    def save_profile(self):
        self.click(self.SAVE_BTN)

    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION, timeout=5)

    def get_notification_text(self) -> str:
        try:
            return self.get_text(self.NOTIFICATION)
        except Exception:
            return ""

    def has_field_error(self) -> bool:
        return self.is_visible(self.FIELD_ERROR, timeout=5)

    # ── Goal helpers ──
    def add_goal(self, score: str, deadline: str = None):
        if self.is_visible(self.ADD_GOAL_BTN, timeout=5):
            self.click(self.ADD_GOAL_BTN)
        if self.is_visible(self.GOAL_SCORE_INPUT, timeout=5):
            self.type_text(self.GOAL_SCORE_INPUT, score)
        if deadline and self.is_visible(self.GOAL_DEADLINE_INPUT, timeout=3):
            self.type_text(self.GOAL_DEADLINE_INPUT, deadline)
        if self.is_visible(self.GOAL_SAVE_BTN, timeout=5):
            self.click(self.GOAL_SAVE_BTN)

    def get_goal_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.GOAL_ITEMS))
        except Exception:
            return 0

    # ── Schedule helpers ──
    def get_schedule_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.SCHEDULE_ITEMS))
        except Exception:
            return 0

    def has_overlap_warning(self) -> bool:
        return self.is_visible(self.SCHEDULE_OVERLAP_MSG, timeout=5)
