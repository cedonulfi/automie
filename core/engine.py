import os
from playwright.sync_api import sync_playwright

class AutomieEngine:
    """
    Core Automation Engine.
    Manages browser instances, contexts, and session persistence.
    """
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None

    def start_browser(self):
        """Starts the Playwright browser instance."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        return self.browser

    def get_context(self, session_file):
        """
        Creates a browser context using a saved session state (cookies).
        If the file doesn't exist, returns a fresh context.
        """
        if os.path.exists(session_file):
            return self.browser.new_context(storage_state=session_file)
        else:
            print(f"[WARN] Session file {session_file} not found. Starting fresh.")
            return self.browser.new_context()

    def stop_browser(self):
        """Closes the browser and stops Playwright."""
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()