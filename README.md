# 🤖 Automie: AI-Powered Social Media Automation Engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-green.svg)](https://playwright.dev/python/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



**Automie** is a decoupled, highly scalable social media automation framework built with Python. It combines the human-like browsing capabilities of **Playwright** with the generative power of **Google Gemini AI**, all wrapped in a sleek **Streamlit** control panel.

Forget rigid API limits. Automie uses session-based browser automation to manage multiple accounts across multiple platforms seamlessly.

## ✨ Why Automie?

Building micro-SaaS tools or managing personal brands requires consistent posting, but traditional API-based bots often sound robotic or face aggressive rate limits. Automie solves this by:
1. **Acting Human:** Uses Playwright to render real browser sessions (saving cookies/local storage) to avoid suspicious login attempts.
2. **Thinking Smart:** Integrates with Gemini AI to adapt your raw thoughts into platform-specific tones (e.g., short for X/Twitter, professional for LinkedIn).
3. **Being Extensible:** Features a pure **Plugin Architecture**. Want to add Facebook or Reddit? Just drop a new python file into the `plugins/` folder.

---

## 🏗 Architecture Overview



Automie operates on a decoupled architecture, ensuring the UI remains fast while heavy browser automation happens in the background:
* **The Control Panel (`app.py`):** A Streamlit web UI to draft ideas, communicate with the AI, and schedule posts into the database queue. Features a secure, password-protected entry.
* **The Brain (`core/ai_router.py`):** Evaluates prompts and formats the content specifically for the target platform.
* **The Engine (`worker.py` & `core/engine.py`):** A background worker meant to be run via OS Cronjobs. It fetches pending tasks from SQLite and executes them using Playwright.
* **The Plugins (`plugins/`):** Isolated logic for each social network.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
Clone the repository and set up your virtual environment:
```bash
git clone [https://github.com/cedonulfi/automie.git](https://github.com/cedonulfi/automie.git)
cd automie
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

```

Install the required dependencies and Playwright browsers:

```bash
pip install -r requirements.txt
playwright install chromium

```

### 3. Environment Configuration

Copy the template environment file and add your credentials:

```bash
cp .env.example .env

```

Edit `.env` to include your Google Gemini API key and a secure dashboard password:

```ini
GEMINI_API_KEY=your_gemini_api_key
DASHBOARD_PASSWORD=your_secure_password

```

### 4. Run the Dashboard

Fire up the Streamlit UI:

```bash
streamlit run app.py

```

*Note: Automie features **Graceful Degradation**. If your database is empty on the first run, the Task Queue will display mock data so you can visualize the UI immediately.*

---

## 🧩 Building a Plugin (For Contributors)

Automie loves contributions! Adding a new platform is incredibly easy. Just inherit from `BaseSocialPlugin`:

```python
# plugins/my_new_platform.py
from plugins.base_plugin import BaseSocialPlugin

class MyNewPlatformPlugin(BaseSocialPlugin):
    def verify_login(self, page):
        # Your logic to check if session is valid
        pass

    def post_content(self, page, content, media_path=None):
        # Your Playwright logic to fill the text area and click post
        return {"success": True, "message": "Posted!"}

```

Check the `Issues` tab for "Good First Issues" to start contributing!

---

## 🛡️ Security Note

Automie stores session state (`.json` files) locally. **Never** commit the `sessions/` directory or your `.env` file to version control. The included `.gitignore` handles this by default.

## 🗺️ Roadmap & Upcoming Features

Automie is actively evolving! Here is what is coming next:
- [ ] **Multi-Model AI Support:** Pluggable AI Factory to swap Gemini with OpenAI (GPT-4), Claude, or local LLMs.
- [ ] **Media Generation & Uploads:** Automatically generate images/videos (via DALL-E 3, Midjourney, etc.) and inject them directly into the Playwright browser using `page.set_input_files()`.
- [ ] **Advanced Scheduling:** Interactive calendar UI within Streamlit for long-term content planning.
- [ ] **Expanded Plugin Library:** Native support for Instagram, Facebook Pages, TikTok, and Reddit.

*Want to build one of these features? We welcome Pull Requests!*

## 📄 Licensee

This project is licensed under the MIT License - see the LICENSE file for details.
