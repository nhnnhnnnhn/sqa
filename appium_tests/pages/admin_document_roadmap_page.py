# pages/admin_document_roadmap_page.py
# Page Object cho Admin Documents + Roadmap Management

from __future__ import annotations

import re
from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminDocumentRoadmapPage(BasePage):
    DOCUMENT_URL = f"{ADMIN_BASE_URL}/admin/documents"
    DOCUMENT_CREATE_URL = f"{ADMIN_BASE_URL}/admin/documents/create"
    ROADMAP_URL = f"{ADMIN_BASE_URL}/admin/roadmap"

    # -------------------------
    # Documents list
    # -------------------------
    DOCUMENT_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ TÀI LIỆU')]")
    ADD_DOCUMENT_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), '+ Thêm tài liệu')]")
    VECTORIZE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Vectorize')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='tên tài liệu'], input[placeholder*='Tên tài liệu']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    FILTER_TOGGLE = (By.XPATH, "//h2[contains(normalize-space(.), 'Bộ lọc')]")
    DOCUMENT_TABLE = (By.XPATH, "//table")
    DOCUMENT_EMPTY = (By.XPATH, "//*[contains(normalize-space(.), 'Không có tài liệu phù hợp')]")

    # -------------------------
    # Document create
    # -------------------------
    CREATE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Thêm tài liệu mới')]")
    CREATE_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Nhập tên tài liệu']")
    CREATE_SUBJECT_SELECT = (
        By.XPATH,
        "//label[contains(normalize-space(.), 'Môn học')]/following::select[1]",
    )
    CREATE_TOPIC_SELECT = (
        By.XPATH,
        "//label[contains(normalize-space(.), 'Chủ đề')]/following::select[1]",
    )
    CREATE_FILE_INPUT = (By.CSS_SELECTOR, "input[type='file']")
    CREATE_SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu tài liệu')]")

    # -------------------------
    # Roadmap
    # -------------------------
    ROADMAP_TITLE = (By.XPATH, "//h2[contains(normalize-space(.), 'QUẢN LÝ ROADMAP')]")
    ROADMAP_TITLE_INPUT = (By.CSS_SELECTOR, "textarea[name='title']")
    ROADMAP_DESC_INPUT = (By.CSS_SELECTOR, "textarea[name='description']")
    ROADMAP_TOPIC_SELECT = (By.CSS_SELECTOR, "select[name='topic_id']")
    ROADMAP_ADD_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Thêm')]")
    ROADMAP_SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu')]")

    NOTIFICATION = (
        By.CSS_SELECTOR,
        "[class*='noti'], [class*='popup'], [class*='notification'], [class*='warning'], [class*='error']",
    )

    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def _set_file_input(self, locator: tuple, file_path: str, timeout: int = 10):
        abs_path = str(Path(file_path).expanduser().resolve())
        if not Path(abs_path).is_file():
            raise FileNotFoundError(abs_path)

        input_el = WebDriverWait(self.driver, timeout).until(
            lambda d: d.find_element(*locator)
        )
        try:
            self.driver.execute_script(
                "arguments[0].style.display='block';"
                "arguments[0].style.visibility='visible';"
                "arguments[0].style.opacity='1';",
                input_el,
            )
        except Exception:
            pass
        input_el.send_keys(abs_path)

    # -------------------------
    # Documents list
    # -------------------------
    def open_document_management(self):
        self.driver.get(self.DOCUMENT_URL)
        self.wait_for_url_contains("/admin/documents")
        self.wait_for_visible(self.DOCUMENT_TITLE, timeout=15)

    def is_document_management_page(self) -> bool:
        url = self.get_current_url()
        return "/admin/documents" in url and "/create" not in url and "/admin/documents/" not in url

    def wait_until_document_page_loaded(self, timeout: int = 15):
        self.wait_for_url_contains("/admin/documents", timeout=timeout)
        self.wait_for_visible(self.DOCUMENT_TITLE, timeout=timeout)

    def is_table_or_empty_visible(self) -> bool:
        return self.is_visible(self.DOCUMENT_TABLE, timeout=5) or self.is_visible(self.DOCUMENT_EMPTY, timeout=5)

    def search_document(self, keyword: str):
        before = (self.driver.page_source or "").lower()
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        key = (keyword or "").strip().lower()
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: (d.page_source or "").lower() != before
                or key in (d.page_source or "").lower()
                or "không có tài liệu phù hợp" in (d.page_source or "").lower()
            )
        except Exception:
            pass

    def has_document_row(self, title: str, timeout: int = 6) -> bool:
        literal = self._xpath_literal(title)
        row = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]",
        )
        return self.is_visible(row, timeout=timeout)

    def get_document_count_on_current_page(self) -> int:
        rows = self.driver.find_elements(By.XPATH, "//table//tbody/tr[td]")
        if len(rows) == 1:
            text = (rows[0].text or "").lower()
            if "không có tài liệu phù hợp" in text:
                return 0
        return len(rows)

    def open_filter_panel(self):
        topic_group = (
            By.XPATH,
            "//div[contains(@class,'filter_group')][.//p[normalize-space()='Chủ đề']]",
        )
        if not self.is_visible(topic_group, timeout=1):
            self.click(self.FILTER_TOGGLE)
            self.wait_for_visible(topic_group, timeout=8)

    def apply_topic_filter(self, topic_title: str) -> bool:
        self.open_filter_panel()
        literal = self._xpath_literal(topic_title)
        topic_btn = (
            By.XPATH,
            f"//div[contains(@class,'filter_group')][.//p[normalize-space()='Chủ đề']]//button[contains(normalize-space(.), {literal})]",
        )
        if not self.is_visible(topic_btn, timeout=5):
            return False

        before = self.driver.page_source or ""
        self.click(topic_btn)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: (d.page_source or "") != before
            )
        except Exception:
            pass
        return True

    def select_document_checkbox_by_title(self, title: str) -> bool:
        literal = self._xpath_literal(title)
        checkbox = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]//input[@type='checkbox']",
        )
        if not self.is_visible(checkbox, timeout=6):
            return False

        el = self.wait_for_visible(checkbox, timeout=6)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        try:
            if not el.is_selected():
                el.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", el)
        return True

    def click_vectorize_selected(self):
        self.click(self.VECTORIZE_BUTTON)

    def get_vectorize_selected_count(self) -> int:
        text = (self.get_text(self.VECTORIZE_BUTTON) or "").strip()
        match = re.search(r"\((\d+)\)", text)
        if not match:
            return 0
        return int(match.group(1))

    # -------------------------
    # Document create
    # -------------------------
    def open_document_create(self):
        self.click(self.ADD_DOCUMENT_BUTTON)
        self.wait_for_url_contains("/admin/documents/create")
        self.wait_for_visible(self.CREATE_TITLE, timeout=12)

    def is_document_create_page(self) -> bool:
        return "/admin/documents/create" in self.get_current_url()

    def fill_document_form(self, *, title: str, subject_id: int, topic_id: int, file_path: str):
        self.type_text(self.CREATE_NAME_INPUT, title)

        subject_select = self.wait_for_visible(self.CREATE_SUBJECT_SELECT, timeout=8)
        Select(subject_select).select_by_value(str(subject_id))

        WebDriverWait(self.driver, 10).until(
            lambda d: len(Select(d.find_element(*self.CREATE_TOPIC_SELECT)).options) >= 2
        )
        topic_select = self.wait_for_visible(self.CREATE_TOPIC_SELECT, timeout=8)
        Select(topic_select).select_by_value(str(topic_id))

        self._set_file_input(self.CREATE_FILE_INPUT, file_path, timeout=8)

    def click_save_document(self):
        self.click(self.CREATE_SAVE_BUTTON)

    # -------------------------
    # Roadmap
    # -------------------------
    def open_roadmap_management(self):
        self.driver.get(self.ROADMAP_URL)
        self.wait_for_url_contains("/admin/roadmap")
        self.wait_for_visible(self.ROADMAP_TITLE, timeout=15)

    def is_roadmap_management_page(self) -> bool:
        return "/admin/roadmap" in self.get_current_url()

    def fill_roadmap_form(self, *, title: str, description: str, topic_id: int):
        self.type_text(self.ROADMAP_TITLE_INPUT, title)
        self.type_text(self.ROADMAP_DESC_INPUT, description)
        select_el = self.wait_for_visible(self.ROADMAP_TOPIC_SELECT, timeout=8)
        Select(select_el).select_by_value(str(topic_id))

    def submit_add_roadmap(self):
        self.click(self.ROADMAP_ADD_BUTTON)

    def submit_save_roadmap(self):
        self.click(self.ROADMAP_SAVE_BUTTON)

    def has_roadmap_row(self, description: str, timeout: int = 6) -> bool:
        literal = self._xpath_literal(description)
        row = (By.XPATH, f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]")
        return self.is_visible(row, timeout=timeout)

    def click_edit_roadmap_by_description(self, description: str):
        literal = self._xpath_literal(description)
        edit_btn = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]//span[contains(normalize-space(.), '...')]",
        )
        self.click(edit_btn)

    def click_delete_roadmap_by_description(self, description: str):
        literal = self._xpath_literal(description)
        delete_btn = (
            By.XPATH,
            f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]//span[normalize-space()='X']",
        )
        self.click(delete_btn)

    def wait_roadmap_row_removed(self, description: str, timeout: int = 10) -> bool:
        literal = self._xpath_literal(description)
        row = (By.XPATH, f"//table//tbody//tr[td[contains(normalize-space(.), {literal})]]")
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _d: not self.is_visible(row, timeout=1)
            )
            return True
        except Exception:
            return False

    # -------------------------
    # Shared notify
    # -------------------------
    def wait_notification_contains(self, text: str, timeout: int = 10) -> bool:
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

    def block_vectorize_api_endpoint(self) -> bool:
        if not hasattr(self.driver, "execute_cdp_cmd"):
            return False
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd(
                "Network.setBlockedURLs",
                {"urls": ["*://*/microservice/llm/vectorize*"]},
            )
            self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
            return True
        except Exception:
            return False

    def unblock_vectorize_api_endpoint(self):
        if not hasattr(self.driver, "execute_cdp_cmd"):
            return
        try:
            self.driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": []})
        except Exception:
            pass
