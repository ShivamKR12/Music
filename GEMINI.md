# Project Rules & Guidelines

These rules must be strictly followed when working on this workspace:

## 1. API Documentation First
**Always read the API markdown files** before making any changes related to the core libraries. Do not guess API methods or configuration options. Use the specific tool to read these files when needed:
- `music_app/kivy_api.md` (for Kivy UI and Core API)
- `music_app/kivymd_api.md` (for KivyMD Material Design components)
- `music_app/ytdlp_api.md` (for yt-dlp downloading and extraction options)

## 2. Assess Overall Impact
**Check and read all relevant code** before modifying any existing file. 
- You must understand the overall architecture and how your proposed changes will impact other interconnected files (e.g., how modifying a model affects the controller and the views).
- Use code search and file reading tools to trace where functions and classes are being utilized across the app before editing them.

## 3. Architecture & Structure
- **Maintain MVC/Modular Structure:** Keep business logic, UI definitions (Views), and Controllers separate. Do not pollute UI widgets with complex background logic.
- **Asynchronous Execution:** Heavy operations (like downloading videos or fetching metadata via `yt-dlp`) must never block the main Kivy UI thread. Always use asynchronous tasks, threading, or Kivy's `Clock`.

## 4. Coding Standards
- **Follow PEP 8:** Write clean, readable, and consistent Python code.
- **Preserve Documentation:** Maintain all existing comments and docstrings. If a function is updated, update its docstring to reflect the new behavior.
- **Robust Error Handling:** Always anticipate and catch potential errors (network failures, invalid URLs, missing files) to prevent the app from crashing.

## 5. Safe Modifications
- Use scratch scripts to safely test logic (e.g., scraping, parsing, or library behavior) before modifying the actual application files.
- Keep file modifications atomic and heavily focused on the user's explicit request.

