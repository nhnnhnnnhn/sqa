# pages/flashcard_page.py
# Page Object cho /flashcards, /flashcards/[id], /flashcards/[id]/quiz, /flashcards/[id]/review

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class FlashcardPage(BasePage):
    # ── Danh sách deck /flashcards ────────────────
    DECK_CARDS     = (By.CSS_SELECTOR, "[class*='deck'], [class*='Deck'], [class*='card']")
    FIRST_DECK     = (By.CSS_SELECTOR, "[class*='deck']:first-child, [class*='card']:first-child")

    # ── Chi tiết deck /flashcards/[id] ───────────
    QUIZ_BTN       = (By.CSS_SELECTOR, "a[href*='/quiz'], button[class*='quiz'], button[class*='Quiz']")
    REVIEW_BTN     = (By.CSS_SELECTOR, "a[href*='/review'], button[class*='review'], button[class*='Review']")
    CARD_TERM      = (By.CSS_SELECTOR, "[class*='term'], [class*='Term'], [class*='front'], [class*='Front']")

    # ── Quiz mode /flashcards/[id]/quiz ──────────
    QUIZ_QUESTION  = (By.CSS_SELECTOR, "[class*='question'], [class*='Question']")
    QUIZ_OPTIONS   = (By.CSS_SELECTOR, "button[class*='option'], [class*='choice'], input[type='radio']")
    QUIZ_NEXT      = (By.CSS_SELECTOR, "button[class*='next'], button[class*='Next']")
    QUIZ_RESULT    = (By.CSS_SELECTOR, "[class*='result'], [class*='score'], [class*='complete']")

    # ── Review mode /flashcards/[id]/review ──────
    FLASHCARD_FACE = (By.CSS_SELECTOR, "[class*='card'], [class*='flashcard']")
    FLIP_BTN       = (By.CSS_SELECTOR, "button[class*='flip'], button[class*='Flip'], [class*='back'], [class*='Back']")
    KNOWN_BTN      = (By.CSS_SELECTOR, "button[class*='known'], button[class*='Know'], button[class*='correct']")
    UNKNOWN_BTN    = (By.CSS_SELECTOR, "button[class*='unknown'], button[class*='Again'], button[class*='wrong']")

    def open_flashcard_list(self):
        self.open("/flashcards")
        self.wait_for_url_contains("/flashcards")

    def get_deck_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.DECK_CARDS))
        except Exception:
            return 0

    def open_first_deck(self):
        decks = self.wait.until(
            EC.presence_of_all_elements_located(self.DECK_CARDS)
        )
        if decks:
            decks[0].click()
            self.wait_for_url_contains("/flashcards/")

    def start_quiz(self):
        self.click(self.QUIZ_BTN)
        self.wait_for_url_contains("/quiz")

    def start_review(self):
        self.click(self.REVIEW_BTN)
        self.wait_for_url_contains("/review")

    def answer_quiz_first_option(self):
        options = self.wait.until(
            EC.presence_of_all_elements_located(self.QUIZ_OPTIONS)
        )
        if options:
            options[0].click()

    def flip_card(self):
        self.click(self.FLIP_BTN)

    def mark_known(self):
        self.click(self.KNOWN_BTN)

    def mark_unknown(self):
        self.click(self.UNKNOWN_BTN)
