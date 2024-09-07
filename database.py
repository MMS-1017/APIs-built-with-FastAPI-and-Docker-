import sqlite3
import uuid

DATABASE = 'content.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')
        conn.commit()

def store_content(content_type: str, content: str) -> str:
    chat_id = str(uuid.uuid4())
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO content (id, type, content) VALUES (?, ?, ?)', 
                       (chat_id, content_type, content))
        conn.commit()
    return chat_id

def get_content(chat_id: str):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT type, content FROM content WHERE id = ?', (chat_id,))
        return cursor.fetchone()