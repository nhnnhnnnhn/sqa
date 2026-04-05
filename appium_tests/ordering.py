"""
Compatibility shim cho lệnh `pytest -p ordering`.

Plugin chính từ package `pytest-ordering` có module là `pytest_ordering`.
File này cho phép giữ nguyên command cũ của team.
"""

pytest_plugins = ("pytest_ordering",)
