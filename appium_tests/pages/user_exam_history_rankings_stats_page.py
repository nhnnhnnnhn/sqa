# pages/user_exam_history_rankings_stats_page.py
# Page Object cho Exams, History, Rankings và User Statistics

from __future__ import annotations

import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from config import BASE_URL


class UserExamHistoryRankingsStatsPage(BasePage):
    EXAM_LIST_URL = f"{BASE_URL}/exam"
    HISTORY_URL = f"{BASE_URL}/my-account/history"
    ANALYTICS_URL = f"{BASE_URL}/analytics"

    EXAM_LIST_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Danh sách đề thi thử')]")
    EXAM_EMPTY_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Không có đề thi')]")

    FILTER_TOGGLE = (By.XPATH, "//h2[contains(normalize-space(.), 'Bộ lọc')]")
    FILTER_APPLY_BTN = (By.XPATH, "//button[contains(normalize-space(.), 'Lọc kết quả')]")

    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Bạn muốn tìm kiếm']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")

    START_EXAM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Bắt đầu thi')]")
    QUESTION_BOX = (By.CSS_SELECTOR, "div[class*='questionBox']")
    FIRST_RADIO_OPTION = (By.XPATH, "(//input[@type='radio'])[1]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Nộp bài')]")
    CONFIRM_YES_BUTTON = (By.XPATH, "//button[normalize-space(.)='Có']")

    RESULT_TITLE = (By.XPATH, "//h3[contains(normalize-space(.), 'Kết quả bài thi')]")
    RESULT_SCORE_VALUE = (By.XPATH, "//*[contains(normalize-space(.), 'Điểm')]/following::b[1]")

    RANK_TABLE_HEADER = (By.XPATH, "//th[contains(normalize-space(.), 'Hạng')]")
    RANK_INFO_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Cách tính thứ hạng')]")
    MY_RANK_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Thành tích của bạn')]")

    HISTORY_TAB_EXAM = (By.XPATH, "//button[contains(normalize-space(.), 'Lịch sử làm cuộc thi')]")
    HISTORY_TITLE = (By.XPATH, "//h2[contains(normalize-space(.), 'Lịch sử làm bài')]")
    HISTORY_EMPTY_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Bạn chưa làm bài thi nào')]")

    ANALYTICS_HEADING = (By.XPATH, "//h1[normalize-space(.)='Analytics']")
    ANALYTICS_PLACEHOLDER = (By.XPATH, "//*[contains(normalize-space(.), 'Trang analytics đang được hoàn thiện')]")

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def _set_local_storage_item(self, key: str, value: str):
        self.driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            key,
            value,
        )

    # -------------------------
    # Navigation
    # -------------------------
    def open_exam_list(self):
        self.driver.get(self.EXAM_LIST_URL)
        self.wait_for_url_contains("/exam")
        self.wait_for_visible(self.EXAM_LIST_TITLE, timeout=12)

    def open_exam_review_rank(self, exam_id: int):
        self.driver.get(f"{BASE_URL}/exam/{exam_id}/review/rank")
        self.wait_for_url_contains(f"/exam/{exam_id}/review/rank")
        self.wait_for_visible(self.START_EXAM_BUTTON, timeout=12)

    def open_exam_do_page(self, exam_id: int):
        self.driver.get(f"{BASE_URL}/exam/{exam_id}/do")
        self.wait_for_url_contains(f"/exam/{exam_id}/do")
        self.wait_for_visible(self.QUESTION_BOX, timeout=12)

    def open_history_page(self):
        self.driver.get(self.HISTORY_URL)
        self.wait_for_url_contains("/my-account/history")
        self.wait_for_visible(self.HISTORY_TAB_EXAM, timeout=12)
        self.click(self.HISTORY_TAB_EXAM)

    def open_analytics_page(self):
        self.driver.get(self.ANALYTICS_URL)
        self.wait_for_url_contains("/analytics")
        self.wait_for_visible(self.ANALYTICS_HEADING, timeout=12)

    # -------------------------
    # Local storage helpers
    # -------------------------
    def set_exam_context(self, *, exam_id: int, exam_name: str, time_limit: int, subject_type: int):
        payload = {
            "exam_id": int(exam_id),
            "exam_name": exam_name,
            "time_limit": int(time_limit),
            "subject_type": int(subject_type),
        }
        self._set_local_storage_item("exam", json.dumps(payload))

    def set_exam_resume_state(
        self,
        *,
        exam_id: int,
        answers: dict,
        time_left: int,
        user_name: str,
    ):
        payload = {
            "answers": answers,
            "timeLeft": int(time_left),
            "userName": user_name,
        }
        self._set_local_storage_item(f"exam_doing_{exam_id}", json.dumps(payload))

    def get_exam_resume_state(self, exam_id: int) -> dict:
        raw = self.driver.execute_script(
            "return window.localStorage.getItem(arguments[0]);",
            f"exam_doing_{exam_id}",
        )
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except Exception:
            return {}

    def clear_exam_resume_state(self, exam_id: int):
        self.driver.execute_script(
            "window.localStorage.removeItem(arguments[0]);",
            f"exam_doing_{exam_id}",
        )

    # -------------------------
    # Exam list + filter/search
    # -------------------------
    def has_exam_card(self, exam_name: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(exam_name)
        locator = (By.XPATH, f"//div[contains(@class,'card')][.//h2[contains(normalize-space(.), {literal})]]")
        return self.is_visible(locator, timeout=timeout)

    def click_exam_card_by_name(self, exam_name: str):
        literal = self._xpath_literal(exam_name)
        locator = (By.XPATH, f"(//div[contains(@class,'card')][.//h2[contains(normalize-space(.), {literal})]])[1]")
        self.click(locator)

    def search_exam(self, keyword: str):
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)

    def ensure_filter_open(self):
        if self.is_visible(self.FILTER_APPLY_BTN, timeout=2):
            return
        self.click(self.FILTER_TOGGLE)
        self.wait_for_visible(self.FILTER_APPLY_BTN, timeout=8)

    def choose_filter_subject(self, subject_name: str):
        literal = self._xpath_literal(subject_name)
        locator = (
            By.XPATH,
            (
                "//div[contains(@class,'filter_group')][.//p[contains(normalize-space(.), 'Môn học')]]"
                f"//button[contains(normalize-space(.), {literal})]"
            ),
        )
        self.click(locator)

    def choose_filter_topic(self, topic_title: str):
        literal = self._xpath_literal(topic_title)
        locator = (
            By.XPATH,
            (
                "//div[contains(@class,'filter_group')][.//p[contains(normalize-space(.), 'Chủ đề')]]"
                f"//button[contains(normalize-space(.), {literal})]"
            ),
        )
        self.click(locator)

    def apply_filter(self):
        self.click(self.FILTER_APPLY_BTN)

    # -------------------------
    # Do exam + result
    # -------------------------
    def click_start_exam(self):
        self.click(self.START_EXAM_BUTTON)

    def wait_do_page_loaded(self, exam_id: int, timeout: int = 15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: f"/exam/{exam_id}/do" in d.current_url
        )
        self.wait_for_visible(self.QUESTION_BOX, timeout=timeout)

    def answer_first_single_choice(self):
        self.click(self.FIRST_RADIO_OPTION)

    def is_first_single_choice_checked(self) -> bool:
        try:
            option = self.wait_for_visible(self.FIRST_RADIO_OPTION, timeout=6)
            return bool(option.is_selected())
        except Exception:
            return False

    def submit_exam(self):
        self.click(self.SUBMIT_BUTTON)

    def confirm_submit_if_needed(self):
        if self.is_visible(self.CONFIRM_YES_BUTTON, timeout=2):
            self.click(self.CONFIRM_YES_BUTTON)

    def wait_result_page_loaded(self, exam_id: int, timeout: int = 20):
        WebDriverWait(self.driver, timeout).until(
            lambda d: f"/exam/{exam_id}/result/" in d.current_url
        )
        self.wait_for_visible(self.RESULT_TITLE, timeout=timeout)

    def get_result_score_text(self) -> str:
        try:
            return (self.get_text(self.RESULT_SCORE_VALUE) or "").strip()
        except Exception:
            return ""

    # -------------------------
    # Ranking + history + analytics
    # -------------------------
    def wait_ranking_loaded(self, timeout: int = 12):
        self.wait_for_visible(self.RANK_TABLE_HEADER, timeout=timeout)
        self.wait_for_visible(self.RANK_INFO_TITLE, timeout=timeout)

    def has_history_exam_card(self, exam_name: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(exam_name)
        locator = (
            By.XPATH,
            f"//div[contains(@class,'list')]//div[contains(@class,'card')][.//*[contains(normalize-space(.), {literal})]]",
        )
        return self.is_visible(locator, timeout=timeout)

    def click_history_exam_card(self, exam_name: str):
        literal = self._xpath_literal(exam_name)
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'list')]//div[contains(@class,'card')][.//*[contains(normalize-space(.), {literal})]])[1]",
        )
        self.click(locator)

    def wait_text_in_page(self, text: str, timeout: int = 8) -> bool:
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
