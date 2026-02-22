from plugins.base_plugin import BaseSocialPlugin
import time

class TwitterPlugin(BaseSocialPlugin):
    """
    Twitter/X integration for Automie.
    Handles specific DOM interactions for twitter.com.
    """

    def login(self, page, username, password):
        """
        Fallback manual login logic. 
        Usually skipped if session.json is valid.
        """
        page.goto("https://x.com/login")
        # Logic to fill username/password goes here
        # X.com login flow often involves multi-step forms
        pass

    def verify_login(self, page):
        """
        Check if the session is valid by looking for the profile icon or post button.
        """
        page.goto("https://x.com/home")
        try:
            # Wait for the main compose button to appear
            page.wait_for_selector('a[aria-label="Post"]', timeout=10000)
            return True
        except Exception:
            return False

    def post_content(self, page, content, media_path=None):
        """
        Executes the actual posting action on Twitter.
        """
        try:
            print("[*] Navigating to Twitter compose page...")
            page.goto("https://x.com/compose/tweet")
            
            # 1. Wait for the text area and fill it
            text_area_selector = 'div[data-testid="tweetTextarea_0"]'
            page.wait_for_selector(text_area_selector, state="visible")
            page.fill(text_area_selector, content)
            
            # 2. Add slight human-like delay
            time.sleep(2)
            
            # 3. Click the post button
            post_button_selector = 'button[data-testid="tweetButton"]'
            page.click(post_button_selector)
            
            # 4. Wait for the dialog to disappear (meaning post is sent)
            page.wait_for_selector(post_button_selector, state="hidden", timeout=10000)
            
            return {"success": True, "message": "Tweet posted successfully."}
            
        except Exception as e:
            return {"success": False, "message": f"Twitter post failed: {str(e)}"}