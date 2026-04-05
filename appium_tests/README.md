# Appium Test Suite – DATN Workspace

Bộ kiểm thử UI/E2E cho `frontend_user` (Next.js, port 3001) sử dụng **Appium 2.x** + **pytest** chạy trên Android emulator với Chrome browser.

---

## Cấu trúc thư mục

```
appium_tests/
├── config.py              # URL, credentials, Desired Capabilities
├── conftest.py            # Appium driver fixture (session-scoped)
├── requirements.txt       # Python dependencies
├── pages/                 # Page Object Model
│   ├── base_page.py       # Lớp cơ sở (wait helpers, click, type_text…)
│   ├── login_page.py      # /login
│   ├── dashboard_page.py  # / (trang chủ)
│   ├── exam_page.py       # /exam, /exam/[id]/do, /exam/[id]/result
│   ├── flashcard_page.py  # /flashcards, /flashcards/[id]/quiz|review
│   ├── practice_page.py   # /practice
│   └── document_page.py   # /document
├── tests/
│   ├── test_auth.py       # TC-AUTH-01 ~ 06
│   ├── test_exam.py       # TC-EXAM-01 ~ 07
│   ├── test_flashcard.py  # TC-FC-01   ~ 08
│   ├── test_practice.py   # TC-PR-01   ~ 05
│   └── test_document.py   # TC-DOC-01  ~ 06
└── screenshots/           # Auto-generated khi test FAIL
```

---

## Yêu cầu môi trường

| Thành phần | Phiên bản khuyến nghị |
|---|---|
| Python | 3.10+ |
| Node.js | 18+ |
| Appium | 2.x (`npm install -g appium`) |
| uiautomator2 driver | latest (`appium driver install uiautomator2`) |
| Android Studio / AVD | API 30+ (Chrome pre-installed) |
| ChromeDriver | tự động tải bởi Appium (`chromedriverAutodownload: true`) |

---

## Cài đặt

### 1. Cài Appium server

```bash
npm install -g appium
appium driver install uiautomator2
```

### 2. Tạo virtual environment & cài Python packages

```bash
cd appium_tests
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# hoặc: .venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### 3. Khởi động Android Emulator

Mở Android Studio → AVD Manager → Start emulator (API 30+, Google Play / Chrome).

### 4. Khởi động ứng dụng frontend

```bash
# Từ thư mục gốc datn_workspace
cd frontend_user
NEXT_PUBLIC_ENDPOINT_BACKEND=http://localhost:3000 npm run dev -- --port 3001
```

> **Lưu ý:** Trên Android emulator, `localhost` của máy host là `10.0.2.2`.
> `config.py` đã dùng `BASE_URL = "http://10.0.2.2:3001"` sẵn.

### 5. Khởi động Appium server

```bash
appium --port 4723
```

---

## Cấu hình

Chỉnh sửa `config.py` trước khi chạy:

```python
TEST_USER_EMAIL    = "user01@test.com"   # Email tài khoản test có trong DB
TEST_USER_PASSWORD = "123456"            # Password mặc định từ data.sql

DESIRED_CAPS = {
    "appium:deviceName": "Android Emulator",  # Thay bằng tên AVD thực tế
    ...
}
```

Để lấy tên device đúng:
```bash
adb devices   # xem danh sách thiết bị/emulator
```

---

## Chạy test

```bash
# Chạy tất cả tests
pytest tests/ -v

# Chạy theo module
pytest tests/test_auth.py -v
pytest tests/test_exam.py -v

# Sinh báo cáo HTML
pytest tests/ -v --html=reports/report.html --self-contained-html

# Chạy theo thứ tự (dùng pytest-ordering)
pytest tests/ -v -p ordering

# Chạy song song (cần pytest-xdist)
# pytest tests/ -n 2
```

---

## Danh sách Test Cases

### Authentication (`test_auth.py`)
| ID | Mô tả | Expected |
|---|---|---|
| TC-AUTH-01 | Trang login load thành công | URL chứa `/login`, form hiển thị |
| TC-AUTH-02 | Link Đăng ký hiển thị | Link tồn tại trên trang |
| TC-AUTH-03 | Đăng nhập sai email | Hiện thông báo lỗi |
| TC-AUTH-04 | Đăng nhập sai mật khẩu | Hiện thông báo lỗi |
| TC-AUTH-05 | Đăng nhập thành công | Redirect về `/` |
| TC-AUTH-06 | Truy cập `/login` khi đã đăng nhập | Ở lại domain |

### Exam (`test_exam.py`)
| ID | Mô tả | Expected |
|---|---|---|
| TC-EXAM-01 | Trang danh sách đề thi load | URL chứa `/exam` |
| TC-EXAM-02 | Có ít nhất 1 đề thi | count > 0 |
| TC-EXAM-03 | Mở đề thi đầu tiên | URL chứa `/exam/[id]` |
| TC-EXAM-04 | Bắt đầu làm bài – thấy câu hỏi | URL chứa `/do`, câu hỏi hiển thị |
| TC-EXAM-05 | Chọn đáp án | Không throw exception |
| TC-EXAM-06 | Nộp bài → trang kết quả | URL chứa `/result` |
| TC-EXAM-07 | Trang kết quả hiện điểm số | Score element hiển thị |

### Flashcard (`test_flashcard.py`)
| ID | Mô tả | Expected |
|---|---|---|
| TC-FC-01 | Trang danh sách deck load | URL chứa `/flashcards` |
| TC-FC-02 | Có ít nhất 1 deck | count > 0 |
| TC-FC-03 | Mở deck đầu tiên | URL chứa `/flashcards/[id]` |
| TC-FC-04 | Có nút Quiz / Review | Ít nhất 1 nút hiển thị |
| TC-FC-05 | Bắt đầu Quiz mode | URL chứa `/quiz` |
| TC-FC-06 | Trả lời câu hỏi Quiz | Không throw exception |
| TC-FC-07 | Bắt đầu Review mode | URL chứa `/review` |
| TC-FC-08 | Review mode hiển thị thẻ | Card element hiển thị |

### Practice (`test_practice.py`)
| ID | Mô tả | Expected |
|---|---|---|
| TC-PR-01 | Trang luyện tập load | URL chứa `/practice` |
| TC-PR-02 | Có nội dung / bộ lọc | count > 0 hoặc filter hiển thị |
| TC-PR-03 | Chọn đáp án | Không throw exception |
| TC-PR-04 | Kiểm tra đáp án | Giải thích hoặc kết quả hiển thị |
| TC-PR-05 | Chuyển câu tiếp theo | Vẫn ở `/practice` |

### Document (`test_document.py`)
| ID | Mô tả | Expected |
|---|---|---|
| TC-DOC-01 | Trang tài liệu load | URL chứa `/document` |
| TC-DOC-02 | Có ít nhất 1 tài liệu | count > 0 |
| TC-DOC-03 | Có ô tìm kiếm | Input hiển thị |
| TC-DOC-04 | Tìm kiếm tài liệu | Trả về list kết quả |
| TC-DOC-05 | Mở tài liệu đầu tiên | URL vẫn trong `/document` |
| TC-DOC-06 | Viewer hiển thị nội dung | PDF canvas hoặc tiêu đề hiển thị |

---

## Troubleshooting

**Appium không kết nối được emulator:**
```bash
adb kill-server && adb start-server
adb devices
```

**ChromeDriver version mismatch:**
Appium sẽ tự tải ChromeDriver phù hợp nhờ `chromedriverAutodownload: true` trong `config.py`.

**`10.0.2.2` không truy cập được app:**
- Đảm bảo `frontend_user` đang chạy trên máy host port 3001
- Kiểm tra firewall không chặn port 3001

**Test fail do selector không tìm thấy:**
Inspect DOM thực tế của app bằng `Appium Inspector` rồi cập nhật locator trong `pages/`.
Tải Appium Inspector tại: https://github.com/appium/appium-inspector/releases
