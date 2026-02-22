import sqlite3
import os
from datetime import datetime

class DatabaseHandler:
    """
    Handles all database interactions for Automie.
    Scalable design: Can be swapped for SQLAlchemy for enterprise usage.
    """
    def __init__(self, db_path="automie.db"):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        """Initializes the database schema if it doesn't exist."""
        if not os.path.exists(self.db_path):
            # Load schema from file
            with open("database/schema.sql", "r") as f:
                schema = f.read()
            conn = sqlite3.connect(self.db_path)
            conn.executescript(schema)
            conn.close()
            print("[INFO] Database initialized successfully.")

    def get_pending_tasks(self):
        """
        Fetches tasks that are 'pending' and scheduled for now or the past.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
            SELECT t.id, t.content, a.platform, a.session_file 
            FROM tasks t
            JOIN accounts a ON t.account_id = a.id
            WHERE t.status = 'pending' AND t.scheduled_time <= ?
        """
        cursor.execute(query, (now,))
        tasks = cursor.fetchall()
        conn.close()
        return tasks

    def update_task_status(self, task_id, status, message=""):
        """
        Updates the status of a task after execution.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ?, log_message = ? WHERE id = ?", 
            (status, message, task_id)
        )
        conn.commit()
        conn.close()