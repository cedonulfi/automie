-- Automie Database Schema

-- Table: accounts
-- Stores social media account credentials and session file paths.
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    platform TEXT NOT NULL,          -- e.g., 'twitter', 'linkedin'
    username TEXT NOT NULL,          -- Display name or login ID
    session_file TEXT NOT NULL,      -- Path to .json session file (e.g., sessions/user1_twitter.json)
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: tasks
-- Queue for scheduled posts. The worker script picks tasks from here.
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    content TEXT NOT NULL,           -- The text content to post
    media_path TEXT,                 -- Optional: Path to image/video
    scheduled_time TIMESTAMP,        -- When this task should run
    status TEXT DEFAULT 'pending',   -- Enum: pending, processing, success, failed
    log_message TEXT,                -- Error messages or success logs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(account_id) REFERENCES accounts(id)
);