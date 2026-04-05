# pages/admin_question_page.py
# Page Object cho Admin Question Management (/admin/questions)

from __future__ import annotations

from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminQuestionPage(BasePage):
    URL = f"{ADMIN_BASE_URL}/admin/questions"
    CREATE_URL = f"{ADMIN_BASE_URL}/admin/questions/create"

    # Question list
    TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'QUẢN LÝ CÂU HỎI')]")
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[placeholder*='Tìm theo nội dung câu hỏi']")
    SEARCH_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Tìm kiếm')]")
    TYPE_FILTER = (
        By.XPATH,
        "//select[option[contains(normalize-space(.), 'Tất cả loại câu hỏi')]]",
    )
    STATUS_FILTER = (
        By.XPATH,
        "//select[option[contains(normalize-space(.), 'Tất cả trạng thái')]]",
    )
    ADD_QUESTION_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), '+ Thêm câu hỏi')]")
    JSON_LIST_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Danh sách JSON')]")
    DOCX_INPUT = (By.CSS_SELECTOR, "input[type='file'][accept='.docx']")

    QUESTION_CARD_TITLE = (By.XPATH, "//h2[starts-with(normalize-space(.), 'Câu ')]")
    DELETE_BUTTON = (By.XPATH, "(//button[contains(normalize-space(.), 'Xoá')])[1]")
    CANCEL_CONFIRM_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Không')]")

    # Create page
    CREATE_TITLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Tạo câu hỏi')]")
    QUESTION_CONTENT_TEXTAREA = (
        By.XPATH,
        "//label[contains(normalize-space(.), 'Nội dung câu hỏi')]/following::textarea[1]",
    )
    TYPE_SINGLE_RADIO = (By.XPATH, "//label[normalize-space()='Trắc nghiệm']/input[@type='radio']")
    TYPE_MULTI_RADIO = (By.XPATH, "//label[normalize-space()='Đúng / Sai']/input[@type='radio']")
    TYPE_ESSAY_RADIO = (By.XPATH, "//label[normalize-space()='Tự luận']/input[@type='radio']")
    ESSAY_ANSWER_TEXTAREA = (
        By.CSS_SELECTOR,
        "textarea[placeholder*='Nhập đáp án mẫu hoặc hướng dẫn chấm']",
    )
    SAVE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Lưu câu hỏi')]")
    QUESTION_IMAGE_INPUT = (
        By.XPATH,
        "(//label[contains(normalize-space(.), 'Hình ảnh câu hỏi')]/following::input[@type='file'])[1]",
    )
    ANSWER_IMAGE_INPUT = (
        By.XPATH,
        "(//label[contains(normalize-space(.), 'Hình ảnh đáp án')]/following::input[@type='file'])[1]",
    )

    # JSON parser
    JSON_MODAL_TITLE = (By.XPATH, "//h2[contains(normalize-space(.), 'Danh sách json')]")
    JSON_FILE_FIRST_ROW = (By.XPATH, "(//tbody/tr)[1]")
    IMPORT_SELECTED_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Import câu hỏi')]")
    IMPORT_SINGLE_BUTTON = (By.XPATH, "(//button[contains(normalize-space(.), 'Import')])[1]")

    # Generic notify
    NOTIFICATION = (
        By.CSS_SELECTOR,
        "[class*='noti'], [class*='popup'], [class*='notification'], [class*='warning'], [class*='error']",
    )

    # -------------------------
    # Shared helpers
    # -------------------------
    def _xpath_literal(self, value: str) -> str:
        if "'" not in value:
            return f"'{value}'"
        if '"' not in value:
            return f'"{value}"'
        parts = value.split("'")
        return "concat(" + ", \"'\", ".join(f"'{part}'" for part in parts) + ")"

    def _wait_present(self, locator: tuple, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def _set_file_input(self, locator: tuple, file_path: str, timeout: int = 10):
        abs_path = str(Path(file_path).expanduser().resolve())
        if not Path(abs_path).is_file():
            raise FileNotFoundError(abs_path)

        input_el = self._wait_present(locator, timeout=timeout)
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

    def _get_question_card_texts(self) -> list[str]:
        script = """
        const headings = Array.from(document.querySelectorAll('h2'))
          .filter((h) => /^\\s*Câu\\s+\\d+/i.test((h.textContent || '').trim()));
        const texts = [];
        for (const h of headings) {
          let container = h;
          for (let i = 0; i < 6; i++) {
            const parent = container.parentElement;
            if (!parent) break;
            const hasDelete = Array.from(parent.querySelectorAll('button'))
              .some((b) => /x[oó]a/i.test(b.textContent || ''));
            container = parent;
            if (hasDelete) break;
          }
          const text = (container.innerText || '').replace(/\\s+/g, ' ').trim();
          if (text) texts.push(text);
        }
        return texts;
        """
        try:
            return self.driver.execute_script(script) or []
        except Exception:
            return []

    def _list_signature(self) -> str:
        texts = self._get_question_card_texts()
        return "||".join(texts)

    def _wait_list_change(self, before_signature: str, timeout: int = 12):
        if not before_signature:
            return
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda _d: self._list_signature() != before_signature
            )
        except Exception:
            pass

    # -------------------------
    # Question list page
    # -------------------------
    def open_question_management(self):
        self.driver.get(self.URL)
        self.wait_for_url_contains("/admin/questions")
        self.wait_for_visible(self.TITLE, timeout=12)

    def navigate_to_question_management(self):
        navigation_attempts = [
            lambda: self.driver.execute_script("window.location.href = arguments[0];", self.URL),
            lambda: self.driver.execute_script("window.location.assign(arguments[0]);", self.URL),
            lambda: self.driver.execute_script("window.location.replace(arguments[0]);", self.URL),
            lambda: self.driver.get(self.URL),
        ]

        last_error = None
        for attempt in navigation_attempts:
            try:
                attempt()
                self.wait_for_url_contains("/admin/questions", timeout=10)
                self.wait_for_visible(self.TITLE, timeout=12)
                return
            except Exception as exc:
                last_error = exc

        if last_error:
            raise last_error

    def is_question_management_page(self) -> bool:
        url = self.get_current_url()
        return "/admin/questions" in url and "/create" not in url and "/file-parser/" not in url

    def wait_until_loaded(self, timeout: int = 15):
        self.wait_for_url_contains("/admin/questions", timeout=timeout)
        self.wait_for_visible(self.TITLE, timeout=timeout)

    def search_question(self, keyword: str):
        before = self._list_signature()
        self.type_text(self.SEARCH_INPUT, keyword)
        self.click(self.SEARCH_BUTTON)
        self._wait_list_change(before_signature=before, timeout=12)

    def set_type_filter(self, type_value: int | str):
        before = self._list_signature()
        select_el = self.wait_for_visible(self.TYPE_FILTER, timeout=8)
        Select(select_el).select_by_value(str(type_value))
        self._wait_list_change(before_signature=before, timeout=12)

    def set_status_filter(self, status_value: str):
        before = self._list_signature()
        select_el = self.wait_for_visible(self.STATUS_FILTER, timeout=8)
        Select(select_el).select_by_value(str(status_value))
        self._wait_list_change(before_signature=before, timeout=12)

    def get_selected_type_filter(self) -> str:
        select_el = self.wait_for_visible(self.TYPE_FILTER, timeout=8)
        return Select(select_el).first_selected_option.get_attribute("value")

    def get_selected_status_filter(self) -> str:
        select_el = self.wait_for_visible(self.STATUS_FILTER, timeout=8)
        return Select(select_el).first_selected_option.get_attribute("value")

    def get_question_card_count(self) -> int:
        return len(self.driver.find_elements(*self.QUESTION_CARD_TITLE))

    def has_question_card_containing(self, keyword: str) -> bool:
        key = (keyword or "").strip().lower()
        if not key:
            return False
        for text in self._get_question_card_texts():
            if key in text.lower():
                return True
        return False

    def click_add_question(self):
        self.click(self.ADD_QUESTION_BUTTON)
        self.wait_for_url_contains("/admin/questions/create")

    def delete_first_visible_question(self):
        self.click(self.DELETE_BUTTON)

    def close_delete_confirmation_if_visible(self):
        if self.is_visible(self.CANCEL_CONFIRM_BUTTON, timeout=2):
            self.click(self.CANCEL_CONFIRM_BUTTON)

    # -------------------------
    # Create page
    # -------------------------
    def open_create_question(self):
        self.driver.get(self.CREATE_URL)
        self.wait_for_url_contains("/admin/questions/create")
        self.wait_for_visible(self.CREATE_TITLE, timeout=12)

    def is_create_page(self) -> bool:
        return "/admin/questions/create" in self.get_current_url()

    def fill_question_content(self, content: str):
        self.type_text(self.QUESTION_CONTENT_TEXTAREA, content)

    def choose_single_choice_type(self):
        self.click(self.TYPE_SINGLE_RADIO)

    def choose_multiple_choice_type(self):
        self.click(self.TYPE_MULTI_RADIO)

    def choose_essay_type(self):
        self.click(self.TYPE_ESSAY_RADIO)

    def fill_answer(self, index: int, content: str):
        locator = (By.CSS_SELECTOR, f"input[placeholder='Đáp án {index}']")
        self.type_text(locator, content)

    def set_single_correct_answer(self, index: int):
        locator = (By.XPATH, f"(//input[@name='correctAnswer'])[{index}]")
        self.click(locator)

    def set_multiple_correct_answers(self, indexes: list[int]):
        for index in indexes:
            locator = (
                By.XPATH,
                f"(//input[@placeholder='Đáp án {index}']/following::input[@type='radio'][1])",
            )
            element = self.wait_for_visible(locator, timeout=8)
            if not element.is_selected():
                element.click()

    def fill_essay_sample_answer(self, answer_text: str):
        self.type_text(self.ESSAY_ANSWER_TEXTAREA, answer_text)

    def attach_question_image(self, file_path: str):
        self._set_file_input(self.QUESTION_IMAGE_INPUT, file_path)

    def attach_answer_image(self, file_path: str):
        self._set_file_input(self.ANSWER_IMAGE_INPUT, file_path)

    def save_question(self):
        self.click(self.SAVE_BUTTON)

    # -------------------------
    # DOCX / JSON import
    # -------------------------
    def upload_docx(self, file_path: str) -> bool:
        try:
            self._set_file_input(self.DOCX_INPUT, file_path, timeout=8)
            return True
        except Exception:
            return False

    def open_json_list_modal(self):
        self.click(self.JSON_LIST_BUTTON)

    def is_json_list_modal_visible(self) -> bool:
        return self.is_visible(self.JSON_MODAL_TITLE, timeout=6)

    def open_first_json_file(self):
        self.click(self.JSON_FILE_FIRST_ROW)
        self.wait_for_url_contains("/admin/file-parser/json/", timeout=15)

    def is_json_parser_page(self) -> bool:
        return "/admin/file-parser/json/" in self.get_current_url()

    def select_first_importable_json_question(self) -> bool:
        script = """
        const wrappers = Array.from(document.querySelectorAll('div')).filter((d) => {
          const hasTitle = Array.from(d.querySelectorAll('span'))
            .some((s) => /^\\s*Câu\\s+\\d+/i.test(s.textContent || ''));
          const hasDeleteQuestionBtn = Array.from(d.querySelectorAll('button'))
            .some((b) => (b.textContent || '').includes('Xoá câu hỏi'));
          return hasTitle && hasDeleteQuestionBtn;
        });

        for (const wrap of wrappers) {
          const topCheckbox = wrap.querySelector('input[type="checkbox"]');
          if (!topCheckbox) continue;

          const answerChoices = Array.from(
            wrap.querySelectorAll('input[type="radio"], input[type="checkbox"]')
          ).filter((el) => el !== topCheckbox);

          const hasAtLeastOneCorrect = answerChoices.some((el) => el.checked);
          if (!hasAtLeastOneCorrect) continue;

          if (!topCheckbox.checked) {
            topCheckbox.click();
          }
          return true;
        }
        return false;
        """
        try:
            return bool(self.driver.execute_script(script))
        except Exception:
            return False

    def import_selected_json_questions(self):
        self.click(self.IMPORT_SELECTED_BUTTON)

    def import_first_json_question(self):
        self.click(self.IMPORT_SINGLE_BUTTON)

    # -------------------------
    # Notification helpers
    # -------------------------
    def is_notification_visible(self) -> bool:
        return self.is_visible(self.NOTIFICATION, timeout=4)

    def wait_notification_contains(self, text: str, timeout: int = 8) -> bool:
        needle = text.strip().lower()
        if not needle:
            return False
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: needle in (d.page_source or "").lower()
            )
            return True
        except Exception:
            return False
