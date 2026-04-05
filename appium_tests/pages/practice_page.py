# pages/practice_page.py
# Page Object cho /practice (luyện tập câu hỏi theo ngân hàng)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class PracticePage(BasePage):
    # ── Trang /practice ──────────────────────────
    SUBJECT_FILTER  = (By.CSS_SELECTOR, "select[name*='subject'], [class*='filter'] select, [class*='subject']")
    TOPIC_FILTER    = (By.CSS_SELECTOR, "select[name*='topic'], [class*='topic']")
    QUESTION_CARDS  = (By.CSS_SELECTOR, "[class*='question'], [class*='Question'], [class*='bank']")
    PRACTICE_BTNS   = (By.CSS_SELECTOR, "button[class*='practice'], a[href*='practice'], button[class*='start']")

    # ── Trong khi luyện tập ──────────────────────
    QUESTION_TEXT   = (By.CSS_SELECTOR, "[class*='question'], [class*='Question']")
    ANSWER_OPTIONS  = (By.CSS_SELECTOR, "input[type='radio'], [class*='option'], [class*='choice']")
    CHECK_BTN       = (By.CSS_SELECTOR, "button[class*='check'], button[class*='Check'], button[class*='confirm']")
    NEXT_BTN        = (By.CSS_SELECTOR, "button[class*='next'], button[class*='Next']")
    EXPLANATION     = (By.CSS_SELECTOR, "[class*='explanation'], [class*='Explanation'], [class*='solution']")

    # ── Kết quả ──────────────────────────────────
    RESULT_DISPLAY  = (By.CSS_SELECTOR, "[class*='result'], [class*='score'], [class*='complete']")

    def open_practice(self):
        self.open("/practice")
        self.wait_for_url_contains("/practice")

    def get_question_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.QUESTION_CARDS))
        except Exception:
            return 0

    def select_first_answer(self):
        options = self.wait.until(
            EC.presence_of_all_elements_located(self.ANSWER_OPTIONS)
        )
        if options:
            options[0].click()

    def check_answer(self):
        if self.is_visible(self.CHECK_BTN, timeout=5):
            self.click(self.CHECK_BTN)

    def go_next(self):
        if self.is_visible(self.NEXT_BTN, timeout=5):
            self.click(self.NEXT_BTN)

    def is_explanation_shown(self) -> bool:
        return self.is_visible(self.EXPLANATION, timeout=5)
