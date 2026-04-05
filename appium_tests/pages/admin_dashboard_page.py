# pages/admin_dashboard_page.py
# Page Object cho trang admin dashboard /admin/dashboard

from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from .base_page import BasePage
from config import ADMIN_BASE_URL


class AdminDashboardPage(BasePage):
    URL = f"{ADMIN_BASE_URL}/admin/dashboard"

    # Core sections
    TITLE_OVERVIEW = (By.XPATH, "//h1[contains(normalize-space(.), 'Tổng quan')]")
    TITLE_TIME_CHART = (By.XPATH, "//h1[contains(normalize-space(.), 'Biểu đồ theo thời gian')]")
    TITLE_ACTIVE_USERS = (By.XPATH, "//h1[contains(normalize-space(.), 'Người dùng hoạt động')]")
    TITLE_PIE = (By.XPATH, "//h1[contains(normalize-space(.), 'Biểu đồ tỉ lệ')]")
    TITLE_TABLE = (By.XPATH, "//h1[contains(normalize-space(.), 'Thống kê theo ngày')]")
    LOADING_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Đang tải dashboard')]")
    EMPTY_STATE_TEXT = (By.XPATH, "//*[contains(normalize-space(.), 'Chưa có dữ liệu')]")

    # Overview cards
    OVERVIEW_CARD_VALUE = (By.XPATH, "//h4/following-sibling::div[1]")
    REQUIRED_KPI_TITLES = [
        "Học sinh mới",
        "Số học sinh tham gia",
        "Bài thi đã nộp",
        "Điểm trung bình",
        "Đạt điểm chuẩn",
        "Môn phổ biến nhất",
    ]

    def open_dashboard(self):
        self.driver.get(self.URL)
        self.wait_for_url_contains("/admin/dashboard")

    def is_dashboard_page(self) -> bool:
        return "/admin/dashboard" in self.get_current_url()

    def wait_until_loaded(self, timeout: int = 25):
        self.wait_for_url_contains("/admin/dashboard", timeout=timeout)
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: "Đang tải dashboard" not in d.page_source
            )
        except Exception:
            # Một số môi trường render nhanh/chậm không ổn định text loading
            pass

    def has_required_sections(self) -> bool:
        return (
            self.is_visible(self.TITLE_OVERVIEW, timeout=8)
            and self.is_visible(self.TITLE_TIME_CHART, timeout=8)
            and self.is_visible(self.TITLE_ACTIVE_USERS, timeout=8)
            and self.is_visible(self.TITLE_PIE, timeout=8)
            and self.is_visible(self.TITLE_TABLE, timeout=8)
        )

    def has_required_kpi_cards(self) -> bool:
        for title in self.REQUIRED_KPI_TITLES:
            locator = (By.XPATH, f"//h4[contains(normalize-space(.), '{title}')]")
            if not self.is_visible(locator, timeout=5):
                return False
        return True

    def get_kpi_values(self) -> list[str]:
        values = []
        elements = self.driver.find_elements(*self.OVERVIEW_CARD_VALUE)
        for element in elements:
            text = (element.text or "").strip()
            if text:
                values.append(text)
        return values

    def chart_and_table_blocks_have_valid_content_state(self) -> bool:
        script = """
        const texts = Array.from(document.querySelectorAll('h1,h2,h3'));
        const sectionTitles = [
          'Biểu đồ theo thời gian',
          'Người dùng hoạt động',
          'Biểu đồ tỉ lệ',
          'Thống kê theo ngày'
        ];

        function normalize(text) {
          return (text || '').replace(/\\s+/g, ' ').trim();
        }

        function findSectionByTitle(title) {
          const heading = texts.find((el) => normalize(el.textContent).includes(title));
          if (!heading) return null;
          return heading.parentElement;
        }

        function hasVisualContent(section) {
          if (!section) return false;
          return !!section.querySelector('canvas, svg, table, .recharts-wrapper');
        }

        function hasEmptyState(section) {
          if (!section) return false;
          return normalize(section.innerText).includes('Chưa có dữ liệu');
        }

        return sectionTitles.every((title) => {
          const section = findSectionByTitle(title);
          return !!section && (hasVisualContent(section) || hasEmptyState(section));
        });
        """
        try:
            return bool(self.driver.execute_script(script))
        except Exception:
            return False

    def find_time_range_filter_control(self):
        candidates = self.driver.find_elements(
            By.CSS_SELECTOR,
            "select, input[type='date'], input[type='month'], button[aria-label*='time'], button[aria-label*='range']",
        )
        for element in candidates:
            try:
                if not element.is_displayed():
                    continue
            except Exception:
                continue

            name = " ".join(
                [
                    element.get_attribute("name") or "",
                    element.get_attribute("id") or "",
                    element.get_attribute("aria-label") or "",
                    element.get_attribute("placeholder") or "",
                    element.text or "",
                ]
            ).lower()

            if any(
                key in name
                for key in [
                    "time",
                    "range",
                    "period",
                    "date",
                    "ngày",
                    "tuần",
                    "tháng",
                    "năm",
                ]
            ):
                return element

            if element.tag_name.lower() == "select":
                options_text = " ".join(
                    opt.text.lower() for opt in element.find_elements(By.TAG_NAME, "option")
                )
                if any(
                    key in options_text
                    for key in [
                        "today",
                        "week",
                        "month",
                        "year",
                        "7 ngày",
                        "30 ngày",
                        "tuần",
                        "tháng",
                        "năm",
                        "quý",
                    ]
                ):
                    return element
        return None

    def change_to_another_time_range(self, control) -> bool:
        tag_name = (control.tag_name or "").lower()

        if tag_name == "select":
            picker = Select(control)
            options = picker.options
            if len(options) < 2:
                return False

            current_text = picker.first_selected_option.text.strip()
            for index, option in enumerate(options):
                if option.text.strip() != current_text:
                    picker.select_by_index(index)
                    return True
            return False

        if tag_name == "input":
            input_type = (control.get_attribute("type") or "").lower()
            if input_type == "month":
                new_value = (datetime.now() - timedelta(days=32)).strftime("%Y-%m")
                self.driver.execute_script(
                    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                    control,
                    new_value,
                )
                return True
            if input_type == "date":
                new_value = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
                self.driver.execute_script(
                    "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change', {bubbles: true}));",
                    control,
                    new_value,
                )
                return True

        if tag_name == "button":
            control.click()
            return True

        return False

    def get_time_chart_signature(self) -> str:
        script = """
        const heading = Array.from(document.querySelectorAll('h1,h2,h3'))
          .find((el) => (el.textContent || '').includes('Biểu đồ theo thời gian'));
        if (!heading) return '';
        const section = heading.closest('div') || heading.parentElement;
        if (!section) return '';
        const graphics = section.querySelectorAll('svg, path, canvas, .recharts-line, .recharts-dot').length;
        const text = (section.innerText || '').replace(/\\s+/g, ' ').trim();
        return `${graphics}|${text}`;
        """
        try:
            return self.driver.execute_script(script) or ""
        except Exception:
            return ""

    def block_dashboard_api_endpoints(self) -> bool:
        if not hasattr(self.driver, "execute_cdp_cmd"):
            return False

        blocked_urls = [
            "*://*/dashboard/card*",
            "*://*/dashboard/line*",
            "*://*/dashboard/active-users*",
            "*://*/dashboard/pie*",
            "*://*/dashboard/table*",
        ]
        try:
            self.driver.execute_cdp_cmd("Network.enable", {})
            self.driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": blocked_urls})
            self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})
            return True
        except Exception:
            return False

    def unblock_dashboard_api_endpoints(self):
        if not hasattr(self.driver, "execute_cdp_cmd"):
            return
        try:
            self.driver.execute_cdp_cmd("Network.setBlockedURLs", {"urls": []})
        except Exception:
            pass

    def get_visible_empty_state_texts(self) -> list[str]:
        texts = []
        elements = self.driver.find_elements(*self.EMPTY_STATE_TEXT)
        for element in elements:
            try:
                if not element.is_displayed():
                    continue
                text = (element.text or "").strip()
                if text and text not in texts:
                    texts.append(text)
            except Exception:
                continue
        return texts

    def get_viewport_metrics(self) -> dict:
        script = """
        return {
          innerWidth: window.innerWidth || 0,
          innerHeight: window.innerHeight || 0,
          scrollWidth: document.documentElement.scrollWidth || 0,
          scrollHeight: document.documentElement.scrollHeight || 0,
          scrollY: window.scrollY || document.documentElement.scrollTop || 0,
        };
        """
        return self.driver.execute_script(script)

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0);")
