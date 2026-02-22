from plugins.base_plugin import BaseSocialPlugin
import time

class LinkedinPlugin(BaseSocialPlugin):
    """
    LinkedIn integration for Automie.
    Handles specific DOM interactions for linkedin.com.
    """

    def login(self, page, username, password):
        """Fallback manual login logic for LinkedIn."""
        page.goto("https://www.linkedin.com/login")
        pass

    def verify_login(self, page):
        """
        Check if the session is valid by looking for the global navigation profile picture.
        """
        page.goto("https://www.linkedin.com/feed/")
        try:
            page.wait_for_selector('.global-nav__me-photo', timeout=10000)
            return True
        except Exception:
            return False

    def post_content(self, page, content, media_path=None):
        """
        Executes the actual posting action on LinkedIn.
        """
        try:
            print("[*] Navigating to LinkedIn feed...")
            page.goto("https://www.linkedin.com/feed/")
            
            # 1. Click 'Start a post' button
            start_post_btn = 'button.share-box-feed-entry__trigger'
            page.wait_for_selector(start_post_btn, state="visible")
            page.click(start_post_btn)
            
            # 2. Wait for the modal text editor to appear and fill content
            editor_selector = 'div.ql-editor'
            page.wait_for_selector(editor_selector, state="visible")
            
            # Playwright's fill() sometimes struggles with complex rich-text editors.
            # Typing it mimics human behavior better for LinkedIn.
            page.type(editor_selector, content, delay=50) 
            
            time.sleep(2)
            
            # 3. Click the actual 'Post' button inside the modal
            submit_btn = 'button.share-actions__primary-action'
            page.click(submit_btn)
            
            # 4. Wait for the modal to close
            page.wait_for_selector(editor_selector, state="hidden", timeout=15000)
            
            return {"success": True, "message": "LinkedIn post published successfully."}
            
        except Exception as e:
            return {"success": False, "message": f"LinkedIn post failed: {str(e)}"}