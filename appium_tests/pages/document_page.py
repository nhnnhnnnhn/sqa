# pages/document_page.py
# Page Object cho /document

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class DocumentPage(BasePage):
    # ── Trang danh sách /document ─────────────────
    DOCUMENT_ITEMS  = (By.CSS_SELECTOR, "[class*='document'], [class*='Document'], [class*='doc']")
    SEARCH_INPUT    = (By.CSS_SELECTOR, "input[type='search'], input[placeholder*='tìm'], input[placeholder*='search'], input[placeholder*='Tìm']")
    FILTER_SUBJECT  = (By.CSS_SELECTOR, "select[name*='subject'], [class*='filter'] select")

    # ── Xem tài liệu ────────────────────────────
    PDF_VIEWER      = (By.CSS_SELECTOR, "[class*='pdf'], canvas, iframe[src*='pdf']")
    DOCUMENT_TITLE  = (By.CSS_SELECTOR, "h1, h2, [class*='title'], [class*='Title']")
    ASK_INPUT       = (By.CSS_SELECTOR, "input[placeholder*='hỏi'], input[placeholder*='Ask'], textarea[placeholder*='hỏi']")
    ASK_BTN         = (By.CSS_SELECTOR, "button[class*='ask'], button[class*='send'], button[class*='Ask']")
    AI_RESPONSE     = (By.CSS_SELECTOR, "[class*='answer'], [class*='response'], [class*='chat']")

    def open_document_list(self):
        self.open("/document")
        self.wait_for_url_contains("/document")

    def get_document_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.DOCUMENT_ITEMS))
        except Exception:
            return 0

    def open_first_document(self):
        items = self.wait.until(
            EC.presence_of_all_elements_located(self.DOCUMENT_ITEMS)
        )
        if items:
            items[0].click()

    def search_document(self, keyword: str):
        self.type_text(self.SEARCH_INPUT, keyword)

    def get_visible_documents(self) -> list:
        try:
            return self.driver.find_elements(*self.DOCUMENT_ITEMS)
        except Exception:
            return []

    def is_pdf_viewer_shown(self) -> bool:
        return self.is_visible(self.PDF_VIEWER, timeout=10)

    def ask_ai(self, question: str):
        self.type_text(self.ASK_INPUT, question)
        self.click(self.ASK_BTN)
