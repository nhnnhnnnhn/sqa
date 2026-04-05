# pages/roadmap_page.py
# Page Object cho /roadmap (user side)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class RoadmapPage(BasePage):
    # ── Danh sách roadmap /roadmap ─────────────
    ROADMAP_ITEMS  = (By.CSS_SELECTOR,
        "[class*='roadmap'], [class*='Roadmap'], [class*='path'], [class*='Path']")
    FIRST_ROADMAP  = (By.CSS_SELECTOR,
        "[class*='roadmap']:first-child, [class*='path']:first-child")

    # ── Chi tiết roadmap /roadmap/[id] ────────
    ROADMAP_STEPS  = (By.CSS_SELECTOR,
        "[class*='step'], [class*='Step'], [class*='node'], li[class*='item']")
    ROADMAP_TITLE  = (By.CSS_SELECTOR,
        "h1, h2, [class*='title'], [class*='Title']")

    # ── Nội dung liên kết ─────────────────────
    LINKED_CONTENT = (By.CSS_SELECTOR,
        "a[href*='/practice'], a[href*='/flashcard'], a[href*='/document']")

    def open_roadmap_list(self):
        self.open("/roadmap")
        self.wait_for_url_contains("/roadmap")

    def get_roadmap_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.ROADMAP_ITEMS))
        except Exception:
            return 0

    def open_first_roadmap(self):
        items = self.wait.until(
            EC.presence_of_all_elements_located(self.ROADMAP_ITEMS)
        )
        if items:
            items[0].click()
            self.wait_for_url_contains("/roadmap/")

    def get_step_count(self) -> int:
        try:
            return len(self.driver.find_elements(*self.ROADMAP_STEPS))
        except Exception:
            return 0

    def has_linked_content(self) -> bool:
        return self.is_visible(self.LINKED_CONTENT, timeout=5)

    def get_title(self) -> str:
        try:
            return self.get_text(self.ROADMAP_TITLE)
        except Exception:
            return ""
