import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class AIRouter:
    """
    AI Logic Layer.
    Uses Google Gemini to generate social media content and determine posting strategy.
    """
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing in .env file.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_post_content(self, topic, platform, tone="professional"):
        """
        Generates platform-specific content based on a topic.
        """
        prompt = (
            f"Write a social media post for {platform}. "
            f"Topic: {topic}. "
            f"Tone: {tone}. "
            f"Keep it engaging and within character limits. "
            f"Do not include hashtags unless necessary."
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"[ERROR] AI Generation failed: {e}")
            return topic  # Fallback to the raw topic if AI fails