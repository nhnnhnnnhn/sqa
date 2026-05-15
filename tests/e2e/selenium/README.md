# Selenium Tests

These tests use Python, pytest, and Selenium 4. Selenium Manager downloads the browser driver automatically. Edge is the default browser.

## Install

```powershell
cd tests/e2e/selenium
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Start the project

Run these in separate terminals before running Selenium:

```powershell
cd backend
npm run dev
```

```powershell
cd frontend_user
npm run dev
```

```powershell
cd frontend_admin
npm run dev
```

Defaults expected by the tests:

- user frontend: `http://localhost:3001`
- admin frontend: `http://localhost:3002`
- admin account: `admin@example.com` / `admin123`
- user account: `user_1@demo.edu.vn` / `123456`

Override them if your local seed data is different:

```powershell
$env:USER_BASE_URL="http://localhost:3001"
$env:ADMIN_BASE_URL="http://localhost:3002"
$env:USER_EMAIL="your-user@example.com"
$env:USER_PASSWORD="your-password"
$env:ADMIN_EMAIL="admin@example.com"
$env:ADMIN_PASSWORD="admin123"
```

## Run

```powershell
pytest -q
```

Edge is configured as the default browser. If Selenium cannot download EdgeDriver automatically, place `msedgedriver.exe` in `tests/e2e/selenium/drivers` or point to it explicitly:

```powershell
$env:EDGE_DRIVER_PATH="tests/e2e/selenium/drivers/msedgedriver.exe"
pytest -q
```

Run one module:

```powershell
pytest -q -m chatbot
pytest -q -m flashcards
pytest -q -m user_management
```

Run headless and create an HTML report:

```powershell
$env:HEADLESS="1"
pytest --html=reports/selenium-report.html --self-contained-html
```

Use another browser only if needed:

```powershell
$env:BROWSER="chrome"
pytest -q
```
