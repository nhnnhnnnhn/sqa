# config.py
# Cấu hình chung cho Appium test suite

# ──────────────────────────────────────────────
# URL ứng dụng
# Khi chạy trên Android emulator, localhost của máy host = 10.0.2.2
# ──────────────────────────────────────────────
BASE_URL = "http://localhost:3001"
ADMIN_BASE_URL = "http://localhost:3002"


TEST_USER_EMAIL    = "user1@example.com"     # U1
TEST_USER_PASSWORD = "User123!"              # U1

ADMIN_EMAIL    = "admin@example.com"         # A1
ADMIN_PASSWORD = "admin123"

USER1_EMAIL    = "user11@example.com"         # U1
USER1_PASSWORD = "User123!"

USER2_EMAIL    = "user2@example.com"         # U2
USER2_PASSWORD = "User123!"

# Tài khoản sai (dùng cho test negative)
WRONG_EMAIL    = "notexist@test.com"
WRONG_PASSWORD = "wrongpass"

# Email chưa tồn tại (E1) – dùng timestamp khi chạy thực tế
NEW_USER_EMAIL    = "newuser+autotest@example.com"
NEW_USER_PASSWORD = "NewUser123!"
NEW_USER_NAME     = "Auto Tester"

# Email đã tồn tại (E2)
EXISTING_EMAIL = USER1_EMAIL

# ──────────────────────────────────────────────
# Từ khóa tìm kiếm
# ──────────────────────────────────────────────
SEARCH_KEYWORD         = "Toán"           # KW1 – keyword hợp lệ
SEARCH_KEYWORD_SPECIAL = "' OR 1=1 --"   # KW2 – chuỗi injection
SEARCH_KEYWORD_LONG    = "A" * 210        # Chuỗi vượt giới hạn

# ──────────────────────────────────────────────
# Appium server
# ──────────────────────────────────────────────
APPIUM_SERVER_URL = "http://127.0.0.1:4723"

# ──────────────────────────────────────────────
# Desired Capabilities – Android Chrome
# Thay DEVICE_NAME / UDID nếu dùng real device
# ──────────────────────────────────────────────
DESIRED_CAPS = {
    "platformName":          "Android",
    "appium:automationName": "uiautomator2",
    "appium:deviceName":     "emulator-5554",
    "appium:browserName":    "Chrome",
    "appium:newCommandTimeout":    120,
    "appium:nativeWebScreenshot":  True,
}

# ──────────────────────────────────────────────
# Timeout (giây)
# ──────────────────────────────────────────────
IMPLICIT_WAIT     = 10   # driver.implicitly_wait
EXPLICIT_WAIT     = 15   # WebDriverWait timeout
PAGE_LOAD_TIMEOUT = 30
