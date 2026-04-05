# pages/user_flashcards_chatbot_roadmap_page.py
# Page Object cho Flashcards, Chatbot, Documents và Roadmap (user side)

from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .base_page import BasePage
from config import BASE_URL


class UserFlashcardsChatbotRoadmapPage(BasePage):
    FLASHCARDS_URL = f"{BASE_URL}/flashcards"
    DOCUMENT_URL = f"{BASE_URL}/document"
    ROADMAP_URL = f"{BASE_URL}/roadmap"

    # -------------------------
    # Flashcard deck list
    # -------------------------
    FLASHCARD_LIST_TITLE = (
        By.XPATH,
        "//h2[contains(normalize-space(.), 'Danh sách bộ thẻ ghi nhớ đã tạo')]",
    )
    FLASHCARD_CREATE_DECK_CARD = (By.XPATH, "//div[contains(normalize-space(.), 'Tạo danh sách từ')]")
    FLASHCARD_DECK_FORM_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Tạo list từ')]")
    FLASHCARD_DECK_TITLE_INPUT = (By.CSS_SELECTOR, "input[name='title']")
    FLASHCARD_DECK_DESC_TEXTAREA = (By.CSS_SELECTOR, "textarea[name='description']")
    FLASHCARD_DECK_SAVE_BUTTON = (By.XPATH, "//button[normalize-space(.)='Lưu']")

    # -------------------------
    # Flashcard deck detail
    # -------------------------
    FLASHCARD_ADD_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Thêm flashcard')]")
    FLASHCARD_DELETE_DECK_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Xoá')]")
    FLASHCARD_PRACTICE_LINK = (By.XPATH, "//a[contains(normalize-space(.), 'Luyện tập Flashcard')]")
    FLASHCARD_REVIEW_LINK = (By.XPATH, "//a[contains(normalize-space(.), 'Ôn tập Flashcard')]")
    FLASHCARD_TOTAL_WORDS = (By.XPATH, "//span[contains(normalize-space(.), 'Tổng số từ')]/preceding-sibling::span[1]")
    FLASHCARD_TOTAL_DONE = (By.XPATH, "//span[contains(normalize-space(.), 'Số từ đã học')]/preceding-sibling::span[1]")

    FLASHCARD_ADD_MODAL_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Tạo flashcard')]")
    FLASHCARD_FRONT_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Nhập mặt trước']")
    FLASHCARD_BACK_TEXTAREA = (By.CSS_SELECTOR, "textarea[placeholder*='Nhập mặt sau']")
    FLASHCARD_ADD_SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu')]")

    # -------------------------
    # Flashcard quiz
    # -------------------------
    QUIZ_TITLE = (By.XPATH, "//h2[contains(normalize-space(.), 'Luyện tập Flashcard')]")
    QUIZ_SUBMIT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Nộp bài')]")
    QUIZ_RESULT_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Bạn đúng')]")

    # -------------------------
    # Flashcard review
    # -------------------------
    REVIEW_COUNTER = (By.XPATH, "//*[contains(normalize-space(.), 'Thẻ') and contains(normalize-space(.), '/')]")
    REVIEW_CARD = (By.CSS_SELECTOR, "div[class*='card']")
    REVIEW_FRONT_TEXT = (By.CSS_SELECTOR, "div[class*='cardContent'][class*='front']")
    REVIEW_CONTROLS = (By.CSS_SELECTOR, "div[class*='controls'] button")

    # -------------------------
    # Document list / viewer
    # -------------------------
    DOCUMENT_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Tài liệu của tôi')]")
    DOCUMENT_SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Bạn muốn tìm kiếm']")
    DOCUMENT_SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    DOCUMENT_VIEWER_TITLE = (By.XPATH, "//*[contains(normalize-space(.), 'Xem tài liệu')]")

    # -------------------------
    # Mini chat
    # -------------------------
    CHAT_OPEN_BUTTON = (By.CSS_SELECTOR, "button[class*='chatButton']")
    CHAT_CONTAINER = (By.CSS_SELECTOR, "div[class*='chatBox']")
    CHAT_HEADER = (By.XPATH, "//*[contains(normalize-space(.), 'Trợ lý hỗ trợ')]")
    CHAT_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Nhập tin nhắn']")
    CHAT_SEND_BUTTON = (By.CSS_SELECTOR, "button[class*='sendBtn']")
    CHAT_BOT_MESSAGE = (By.CSS_SELECTOR, "div[class*='message'][class*='bot']")
    CHAT_ANY_MESSAGE = (By.CSS_SELECTOR, "div[class*='message']")
    CHAT_SOURCE_PANEL = (By.CSS_SELECTOR, "div[class*='sourcePanel']")

    # -------------------------
    # Roadmap
    # -------------------------
    ROADMAP_CARD = (By.CSS_SELECTOR, "div[class*='roadmapCard']")
    ROADMAP_TITLE = (By.CSS_SELECTOR, "h2[class*='roadmapTitle']")
    ROADMAP_STEP_TITLE = (By.CSS_SELECTOR, "h3[class*='stepTitle']")
    ROADMAP_SUBSTEP_BUTTON = (By.CSS_SELECTOR, "button[class*='subStepButton']")
    ROADMAP_PANEL = (By.CSS_SELECTOR, "div[class*='panelSubStep']")
    ROADMAP_SUBSTEP_CONTENT = (By.CSS_SELECTOR, "div[class*='subStepContent']")

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    # -------------------------
    # Flashcards
    # -------------------------
    def open_flashcards_page(self):
        self.driver.get(self.FLASHCARDS_URL)
        self.wait_for_url_contains("/flashcards")
        self.wait_for_visible(self.FLASHCARD_LIST_TITLE, timeout=12)

    def open_create_deck_modal(self):
        self.click(self.FLASHCARD_CREATE_DECK_CARD)
        self.wait_for_visible(self.FLASHCARD_DECK_FORM_TITLE, timeout=10)

    def create_deck(self, *, title: str, description: str):
        self.type_text(self.FLASHCARD_DECK_TITLE_INPUT, title)
        self.type_text(self.FLASHCARD_DECK_DESC_TEXTAREA, description)
        self.click(self.FLASHCARD_DECK_SAVE_BUTTON)

    def has_deck_card(self, title: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(title)
        locator = (
            By.XPATH,
            f"//div[contains(@class,'deckCard')][.//h3[contains(normalize-space(.), {literal})]]",
        )
        return self.is_visible(locator, timeout=timeout)

    def open_deck_by_title(self, title: str):
        literal = self._xpath_literal(title)
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'deckCard')][.//h3[contains(normalize-space(.), {literal})]])[1]",
        )
        self.click(locator)
        self.wait_for_visible(self.FLASHCARD_ADD_BUTTON, timeout=12)

    def open_add_flashcard_modal(self):
        self.click(self.FLASHCARD_ADD_BUTTON)
        self.wait_for_visible(self.FLASHCARD_ADD_MODAL_TITLE, timeout=8)

    def add_flashcard(self, *, front: str, back: str):
        self.type_text(self.FLASHCARD_FRONT_INPUT, front)
        self.type_text(self.FLASHCARD_BACK_TEXTAREA, back)
        self.click(self.FLASHCARD_ADD_SAVE_BUTTON)

    def wait_alert_and_accept(self, timeout: int = 8) -> str | None:
        try:
            alert = WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            text = (alert.text or "").strip()
            alert.accept()
            return text
        except Exception:
            return None

    def get_total_words_value(self) -> int | None:
        try:
            return int((self.get_text(self.FLASHCARD_TOTAL_WORDS) or "").strip())
        except Exception:
            return None

    def get_total_done_value(self) -> int | None:
        try:
            return int((self.get_text(self.FLASHCARD_TOTAL_DONE) or "").strip())
        except Exception:
            return None

    def open_quiz_mode(self):
        self.click(self.FLASHCARD_PRACTICE_LINK)
        self.wait_for_visible(self.QUIZ_TITLE, timeout=12)

    def open_review_mode(self):
        self.click(self.FLASHCARD_REVIEW_LINK)
        self.wait_for_visible(self.REVIEW_COUNTER, timeout=12)

    def choose_first_quiz_option_for_each_question(self):
        script = """
        const cards = Array.from(document.querySelectorAll("div[class*='card']"));
        let clicked = 0;
        cards.forEach((card) => {
          const btn = card.querySelector("button[class*='option']");
          if (btn && !btn.disabled) {
            btn.click();
            clicked += 1;
          }
        });
        return clicked;
        """
        result = self.driver.execute_script(script)
        return int(result or 0)

    def submit_quiz(self):
        self.click(self.QUIZ_SUBMIT_BUTTON)
        self.wait_for_visible(self.QUIZ_RESULT_TEXT, timeout=15)

    def get_quiz_result_text(self) -> str:
        return (self.get_text(self.QUIZ_RESULT_TEXT) or "").strip()

    def get_review_counter_text(self) -> str:
        return (self.get_text(self.REVIEW_COUNTER) or "").strip()

    def get_review_front_text(self) -> str:
        return (self.get_text(self.REVIEW_FRONT_TEXT) or "").strip()

    def click_review_shuffle(self):
        locator = (By.XPATH, "(//div[contains(@class,'controls')]//button)[2]")
        self.click(locator)

    def click_review_next(self):
        locator = (By.XPATH, "(//div[contains(@class,'controls')]//button)[3]")
        self.click(locator)

    def delete_current_deck(self):
        self.click(self.FLASHCARD_DELETE_DECK_BUTTON)

    # -------------------------
    # Documents
    # -------------------------
    def open_document_list(self):
        self.driver.get(self.DOCUMENT_URL)
        self.wait_for_url_contains("/document")
        self.wait_for_visible(self.DOCUMENT_TITLE, timeout=12)

    def search_document(self, keyword: str):
        self.type_text(self.DOCUMENT_SEARCH_INPUT, keyword)
        self.click(self.DOCUMENT_SEARCH_BUTTON)

    def has_document_card(self, title: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(title)
        locator = (By.XPATH, f"//div[contains(@class,'card')][.//h3[contains(normalize-space(.), {literal})]]")
        return self.is_visible(locator, timeout=timeout)

    def open_document_link_by_title(self, title: str):
        literal = self._xpath_literal(title)
        locator = (
            By.XPATH,
            f"(//div[contains(@class,'card')][.//h3[contains(normalize-space(.), {literal})]]//a[contains(normalize-space(.), 'Xem tài liệu')])[1]",
        )
        self.click(locator)

    def switch_to_latest_window(self):
        handles = self.driver.window_handles
        if handles:
            self.driver.switch_to.window(handles[-1])

    def wait_document_viewer_title_contains(self, extension: str, timeout: int = 12) -> bool:
        ext = (extension or "").strip().upper()
        needle = f"Xem tài liệu ({ext})".lower()
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: needle in (d.page_source or "").lower()
            )
            return True
        except Exception:
            return False

    # -------------------------
    # Mini chat
    # -------------------------
    def open_chat_widget(self):
        if self.is_visible(self.CHAT_CONTAINER, timeout=2):
            return
        self.click(self.CHAT_OPEN_BUTTON)
        self.wait_for_visible(self.CHAT_CONTAINER, timeout=10)
        self.wait_for_visible(self.CHAT_HEADER, timeout=10)

    def get_chat_message_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.CHAT_ANY_MESSAGE))
        except Exception:
            return 0

    def get_chat_bot_message_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.CHAT_BOT_MESSAGE))
        except Exception:
            return 0

    def send_chat_message(self, text: str):
        self.type_text(self.CHAT_INPUT, text)
        self.click(self.CHAT_SEND_BUTTON)

    def send_chat_empty(self):
        self.click(self.CHAT_SEND_BUTTON)

    def wait_new_bot_message(self, previous_bot_count: int, timeout: int = 30) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _d: self.get_chat_bot_message_count() > previous_bot_count
            )
            return True
        except Exception:
            return False

    def get_last_bot_message_text(self) -> str:
        try:
            nodes = self.driver.find_elements(*self.CHAT_BOT_MESSAGE)
            if not nodes:
                return ""
            return (nodes[-1].text or "").strip()
        except Exception:
            return ""

    def has_source_panel(self, timeout: int = 8) -> bool:
        return self.is_visible(self.CHAT_SOURCE_PANEL, timeout=timeout)

    # -------------------------
    # Roadmap
    # -------------------------
    def open_roadmap_page(self):
        self.driver.get(self.ROADMAP_URL)
        self.wait_for_url_contains("/roadmap")
        self.wait_for_visible(self.ROADMAP_CARD, timeout=12)

    def has_roadmap_title(self, text: str, timeout: int = 8) -> bool:
        literal = self._xpath_literal(text)
        locator = (By.XPATH, f"//h2[contains(@class,'roadmapTitle')][contains(normalize-space(.), {literal})]")
        return self.is_visible(locator, timeout=timeout)

    def click_first_step_title(self):
        self.click(self.ROADMAP_STEP_TITLE)

    def click_first_substep_button(self):
        self.click(self.ROADMAP_SUBSTEP_BUTTON)

    def is_step_panel_visible(self, timeout: int = 8) -> bool:
        return self.is_visible(self.ROADMAP_PANEL, timeout=timeout)

    def is_substep_content_visible(self, timeout: int = 8) -> bool:
        return self.is_visible(self.ROADMAP_SUBSTEP_CONTENT, timeout=timeout)
