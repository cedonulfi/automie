import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="Automie Dashboard", page_icon="🤖", layout="wide")

def check_password():
    """
    Returns `True` if the user has entered the correct master password.
    Utilizes Streamlit's session_state to keep the user authenticated.
    """
    # Fetch password from .env, default to 'admin' if not set (for local testing)
    master_password = os.getenv("DASHBOARD_PASSWORD", "admin")

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == master_password:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Clear the password from memory for security
        else:
            st.session_state["password_correct"] = False

    # First run, initialize session state
    if "password_correct" not in st.session_state:
        st.markdown("### 🔒 Restricted Access")
        st.markdown("Please enter the master password to access the Automie Control Panel.")
        st.text_input("Master Password", type="password", on_change=password_entered, key="password")
        return False
    
    # Incorrect password entered
    elif not st.session_state["password_correct"]:
        st.markdown("### 🔒 Restricted Access")
        st.text_input("Master Password", type="password", on_change=password_entered, key="password")
        st.error("😕 Incorrect password. Access denied.")
        return False
    
    # Password correct
    return True

def main():
    """
    Main application logic. 
    Will only render if check_password() returns True.
    """
    st.title("🤖 Automie Control Panel")
    st.markdown("Your AI-Powered Social Media Automation Engine")
    st.divider()

    # --- Sidebar for Navigation ---
    st.sidebar.header("Navigation")
    menu = st.sidebar.radio("Go To:", ["Draft & Schedule", "Account Management", "Task Queue"])
    
    st.sidebar.divider()
    st.sidebar.caption("Automie v1.0.0 | Open Source")

    # --- Menu 1: Draft & Schedule ---
    if menu == "Draft & Schedule":
        st.subheader("📝 Draft & Schedule AI Posts")
        st.write("Use Gemini AI to generate content and schedule it for your automated Playwright worker.")
        
        with st.form("schedule_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                target_platform = st.selectbox("Select Target Platform", ["twitter", "linkedin", "facebook"])
                target_account = st.text_input("Account ID", placeholder="e.g., my_main_twitter")
                tone = st.selectbox("Content Tone", ["Professional", "Casual", "Techy", "Humorous"])
            
            with col2:
                schedule_date = st.date_input("Schedule Date", datetime.now())
                schedule_time = st.time_input("Schedule Time", datetime.now().time())

            raw_topic = st.text_area(
                "What is the topic?", 
                placeholder="e.g., I just launched a new open-source project called Automie using Python and Playwright.",
                height=100
            )
            
            submit_button = st.form_submit_button("Generate & Add to Queue", type="primary")

            if submit_button:
                if not raw_topic or not target_account:
                    st.error("Please fill in the Account ID and Topic.")
                else:
                    with st.spinner("Processing with AI and saving to database..."):
                        # --- Mocking Backend Logic for UI Testing ---
                        # In production, this will call: ai.generate_post_content() and db.add_task()
                        scheduled_datetime = datetime.combine(schedule_date, schedule_time)
                        
                        st.success(f"Task successfully scheduled for {target_platform} at {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}!")
                        st.info(f"**Mocked AI Output preview:**\n\nExcited to share my latest open-source project! Built with Python and Playwright, it automates social media workflows seamlessly. Check out the repo! 🚀 #Python #OpenSource")

    # --- Menu 2: Account Management ---
    elif menu == "Account Management":
        st.subheader("👥 Manage Social Accounts")
        st.write("Register new accounts and generate session cookies (`.json`) for the automation engine.")
        
        st.info("Ensure your Playwright worker has UI access (headless=False) when registering a new account for the first time.")
        
        with st.form("account_form"):
            new_platform = st.selectbox("Platform", ["twitter", "linkedin"])
            new_username = st.text_input("Account Name / Identifier")
            
            if st.form_submit_button("Launch Browser to Login"):
                st.warning(f"Feature in development. This will trigger Playwright to open {new_platform} so you can log in manually.")
    
     # --- Menu 3: Task Queue ---
    elif menu == "Task Queue":
        st.subheader("📋 Task Queue & Logs")
        st.write("Monitor pending posts and view logs of completed or failed automations.")
        
        # 1. Coba ambil data asli dari Database
        real_data = []
        try:
            # Pastikan core/database.py sudah ada dan class DatabaseHandler siap
            from core.database import DatabaseHandler
            db = DatabaseHandler()
            
            # Asumsi get_pending_tasks() mengembalikan List of Dictionaries
            # Contoh: [{"ID": 1, "Platform": "twitter", "Status": "pending"}]
            real_tasks = db.get_pending_tasks() 
            
            if real_tasks:
                real_data = real_tasks
        except Exception as e:
            st.caption(f"ℹ️ Database connection not fully initialized yet. ({e})")

        # 2. Logic: Jika ada data asli tampilkan, jika kosong tampilkan Mock Data
        if real_data:
            st.success("🟢 Live Database Active")
            st.dataframe(real_data, use_container_width=True)
        else:
            st.info("💡 No real tasks found in the database. Showing sample data for visualization:")
            
            mock_data = [
                {"ID": 1, "Platform": "twitter", "Account": "my_main_twitter", "Scheduled": "2026-02-22 10:00:00", "Status": "✅ Success"},
                {"ID": 2, "Platform": "linkedin", "Account": "pro_linkedin", "Scheduled": "2026-02-22 14:30:00", "Status": "⏳ Pending"},
                {"ID": 3, "Platform": "twitter", "Account": "bot_account_1", "Scheduled": "2026-02-22 16:00:00", "Status": "⏳ Pending"},
                {"ID": 4, "Platform": "facebook", "Account": "page_admin", "Scheduled": "2026-02-21 09:00:00", "Status": "❌ Failed (Session Expired)"},
            ]
            
            st.dataframe(mock_data, use_container_width=True)
        
        if st.button("Refresh Queue"):
            st.rerun()

if __name__ == "__main__":
    # The gatekeeper: only run main() if the password is correct
    if check_password():
        main()