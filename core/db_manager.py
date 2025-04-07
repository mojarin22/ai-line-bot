import sqlite3
import os
from contextlib import contextmanager

# データベースのパス設定
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'user_data.db')

# DB接続（コンテキストマネージャ）
@contextmanager
def connect_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        print(f"[DBエラー] {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

# DBのテーブル初期化（最初に一回実行すればOK）
def init_db():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                honorific TEXT DEFAULT 'さん',
                mode TEXT DEFAULT 'normal'
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diaries (
                diary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                diary_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_message TEXT,
                ai_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                reminder_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                reminder_text TEXT,
                remind_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_sent INTEGER DEFAULT 0
            )
        ''')

# ユーザーの取得・追加・更新
def upsert_user(user_id, nickname, honorific='さん', mode='normal'):
    with connect_db() as conn:
        conn.execute('''
            INSERT INTO users(user_id, nickname, honorific, mode)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                nickname=excluded.nickname,
                honorific=excluded.honorific,
                mode=excluded.mode
        ''', (user_id, nickname, honorific, mode))

def get_user(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        return cursor.fetchone()

# ユーザーモードの変更
def set_user_mode(user_id, mode):
    with connect_db() as conn:
        conn.execute('UPDATE users SET mode=? WHERE user_id=?', (mode, user_id))

def get_user_mode(user_id):
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT mode FROM users WHERE user_id=?', (user_id,))
        result = cursor.fetchone()
        return result[0] if result else 'normal'

# 日記保存
def save_diary(user_id, diary_text):
    with connect_db() as conn:
        conn.execute('INSERT INTO diaries(user_id, diary_text) VALUES (?, ?)', (user_id, diary_text))

# 会話ログ保存
def save_chat_log(user_id, user_message, ai_response):
    with connect_db() as conn:
        conn.execute('INSERT INTO chat_logs(user_id, user_message, ai_response) VALUES (?, ?, ?)', 
                     (user_id, user_message, ai_response))

# リマインダー追加
def add_reminder(user_id, reminder_text, remind_at):
    with connect_db() as conn:
        conn.execute('INSERT INTO reminders(user_id, reminder_text, remind_at) VALUES (?, ?, ?)',
                     (user_id, reminder_text, remind_at))

# 未送信のリマインダー取得
def get_pending_reminders():
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT reminder_id, user_id, reminder_text, remind_at FROM reminders WHERE is_sent=0 AND remind_at <= CURRENT_TIMESTAMP')
        return cursor.fetchall()

# リマインダーを送信済みに変更
def mark_reminder_sent(reminder_id):
    with connect_db() as conn:
        conn.execute('UPDATE reminders SET is_sent=1 WHERE reminder_id=?', (reminder_id,))

# メインからの実行用（本番では直接実行はせず、セットアップ時のみ使用）
if __name__ == "__main__":
    init_db()
    print("データベースを初期化しました！")
