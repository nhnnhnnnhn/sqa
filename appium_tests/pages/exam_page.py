# pages/exam_page.py
# Page Object cho các trang /exam, /exam/[id]/do, /exam/[id]/result/[history]

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class ExamPage(BasePage):
    # ── Trang danh sách đề thi /exam ─────────────
    EXAM_CARDS     = (By.CSS_SELECTOR, "[class*='examCard'], [class*='ExamCard'], [class*='card']")
    FIRST_EXAM_BTN = (By.CSS_SELECTOR, "[class*='examCard']:first-child, [class*='card']:first-child")
    START_EXAM_BTN = (By.CSS_SELECTOR, "button[class*='start'], a[href*='/do']")

    # ── Trang làm bài /exam/[id]/do ──────────────
    QUESTION_TEXT  = (By.CSS_SELECTOR, "[class*='question'], [class*='Question']")
    ANSWER_OPTIONS = (By.CSS_SELECTOR, "input[type='radio'], [class*='option'], [class*='Option']")
    NEXT_BTN       = (By.CSS_SELECTOR, "button[class*='next'], button[class*='Next']")
    SUBMIT_BTN     = (By.CSS_SELECTOR, "button[class*='submit'], button[class*='Submit'], button[class*='nop'], button[class*='Nop']")
    CONFIRM_SUBMIT = (By.CSS_SELECTOR, "button[class*='confirm'], button[class*='Confirm']")

    # ── Trang kết quả /exam/[id]/result/[id] ─────
    SCORE_DISPLAY  = (By.CSS_SELECTOR, "[class*='score'], [class*='Score'], [class*='result'], [class*='Result']")
    REVIEW_BTN     = (By.CSS_SELECTOR, "a[href*='/review'], button[class*='review']")
    BACK_HOME_BTN  = (By.CSS_SELECTOR, "a[href='/'], a[href='/exam']")

    def open_exam_list(self):
        self.open("/exam")
        self.wait_for_url_contains("/exam")

    def get_exam_count(self) -> int:
        try:
            cards = self.driver.find_elements(*self.EXAM_CARDS)
            return len(cards)
        except Exception:
            return 0

    def open_first_exam(self):
        """Click vào đề thi đầu tiên trong danh sách."""
        cards = self.wait.until(
            EC.presence_of_all_elements_located(self.EXAM_CARDS)
        )
        if cards:
            cards[0].click()

    def start_exam(self):
        """Click nút bắt đầu làm bài."""
        self.click(self.START_EXAM_BTN)
        self.wait_for_url_contains("/do")

    def answer_first_option(self):
        """Chọn đáp án đầu tiên của câu hiện tại."""
        options = self.wait.until(
            EC.presence_of_all_elements_located(self.ANSWER_OPTIONS)
        )
        if options:
            options[0].click()

    def answer_all_and_submit(self, max_questions: int = 40):
        """Lần lượt chọn đáp án đầu tiên rồi nộp bài."""
        for _ in range(max_questions):
            try:
                self.answer_first_option()
                # Thử click Next nếu có, nếu không có thì dừng
                if self.is_visible(self.NEXT_BTN, timeout=3):
                    self.click(self.NEXT_BTN)
                else:
                    break
            except Exception:
                break

        # Nộp bài
        self.click(self.SUBMIT_BTN)
        if self.is_visible(self.CONFIRM_SUBMIT, timeout=5):
            self.click(self.CONFIRM_SUBMIT)

    def is_result_page(self) -> bool:
        return "/result" in self.get_current_url()

    def get_score_text(self) -> str:
        return self.get_text(self.SCORE_DISPLAY)
