import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'game.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 人物表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surname TEXT NOT NULL,
        name TEXT NOT NULL,
        courtesy_name TEXT,
        birth_year INTEGER,
        death_year INTEGER,
        birthplace TEXT,
        dynasty TEXT DEFAULT '东汉',
        force TEXT,
        identity TEXT,
        traits TEXT
    )
    ''')
    
    # 事件表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL UNIQUE,
        event_type TEXT NOT NULL CHECK(event_type IN ('战争', '事件'))
    )
    ''')
    
    # 人物-事件关联表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS character_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        character_id INTEGER NOT NULL,
        event_id INTEGER NOT NULL,
        FOREIGN KEY (character_id) REFERENCES characters(id),
        FOREIGN KEY (event_id) REFERENCES events(id),
        UNIQUE(character_id, event_id)
    )
    ''')
    
    # 亲属关系表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS family_relations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        char_id_1 INTEGER NOT NULL,
        char_id_2 INTEGER NOT NULL,
        relation_name TEXT NOT NULL,
        FOREIGN KEY (char_id_1) REFERENCES characters(id),
        FOREIGN KEY (char_id_2) REFERENCES characters(id),
        UNIQUE(char_id_1, char_id_2)
    )
    ''')
    
    # 房间表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rooms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_code TEXT UNIQUE NOT NULL,
        player1 TEXT,
        player2 TEXT,
        answer_id INTEGER,
        current_turn INTEGER DEFAULT 1,
        status TEXT DEFAULT 'waiting' CHECK(status IN ('waiting', 'playing', 'finished')),
        winner TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (answer_id) REFERENCES characters(id)
    )
    ''')
    
    # 猜测记录表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS guesses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_id INTEGER NOT NULL,
        player TEXT NOT NULL,
        character_id INTEGER NOT NULL,
        guess_order INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (room_id) REFERENCES rooms(id),
        FOREIGN KEY (character_id) REFERENCES characters(id)
    )
    ''')
    
    # 国家表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS countries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        capital TEXT NOT NULL,
        country_chars INTEGER NOT NULL,
        capital_chars INTEGER NOT NULL,
        longitude REAL NOT NULL,
        latitude REAL NOT NULL,
        population REAL NOT NULL,
        area REAL NOT NULL,
        gdp_rank INTEGER NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("数据库初始化完成")
