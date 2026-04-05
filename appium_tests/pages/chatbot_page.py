# pages/chatbot_page.py
# Page Object cho chatbot / RAG interface

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class ChatbotPage(BasePage):
    # ── Input & send ──────────────────────────
    MESSAGE_INPUT  = (By.CSS_SELECTOR,
        "input[placeholder*='hỏi'], input[placeholder*='Ask'], "
        "textarea[placeholder*='hỏi'], textarea[placeholder*='message'], "
        "input[class*='chat'], textarea[class*='chat']")
    SEND_BTN       = (By.CSS_SELECTOR,
        "button[type='submit'], button[class*='send'], button[class*='Send'], "
        "button[aria-label*='send'], button[aria-label*='Send']")

    # ── Trả lời / bubble ─────────────────────
    AI_RESPONSE    = (By.CSS_SELECTOR,
        "[class*='answer'], [class*='response'], [class*='bot'], "
        "[class*='assistant'], [class*='message']")

    # ── Nguồn tham khảo ──────────────────────
    SOURCES_SECTION= (By.CSS_SELECTOR,
        "[class*='source'], [class*='reference'], [class*='citation']")

    # ── Validation / lỗi ─────────────────────
    EMPTY_WARNING  = (By.CSS_SELECTOR,
        "[class*='error'], [class*='warning'], [class*='notification']")

    # ── Loading indicator ─────────────────────
    LOADING        = (By.CSS_SELECTOR,
        "[class*='loading'], [class*='spinner'], [class*='thinking']")

    def open_chatbot(self):
        self.open("/chatbot")
        self.wait_for_url_contains("/chatbot")

    def send_message(self, text: str):
        self.type_text(self.MESSAGE_INPUT, text)
        self.click(self.SEND_BTN)

    def try_send_empty(self):
        """Cố gửi tin nhắn rỗng (không nhập gì)."""
        if self.is_visible(self.SEND_BTN, timeout=5):
            self.click(self.SEND_BTN)

    def wait_for_response(self, timeout: int = 30) -> bool:
        """Chờ AI phản hồi, trả về True nếu xuất hiện bubble trả lời."""
        try:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.AI_RESPONSE)
            )
            return True
        except Exception:
            return False

    def get_last_response_text(self) -> str:
        try:
            msgs = self.driver.find_elements(*self.AI_RESPONSE)
            return msgs[-1].text if msgs else ""
        except Exception:
            return ""

    def is_sources_visible(self) -> bool:
        return self.is_visible(self.SOURCES_SECTION, timeout=5)

    def is_loading(self) -> bool:
        return self.is_visible(self.LOADING, timeout=3)

    def is_empty_warning_shown(self) -> bool:
        return self.is_visible(self.EMPTY_WARNING, timeout=5)
