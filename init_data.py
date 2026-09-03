from database import get_connection, init_db
from data import CHARACTERS, EVENTS, CHARACTER_EVENTS, FAMILY_RELATIONS
from country_data import COUNTRIES
from watermargin_data import WATERMARGIN

def insert_characters():
    conn = get_connection()
    cursor = conn.cursor()
    
    for char in CHARACTERS:
        cursor.execute('''
            INSERT INTO characters (surname, name, courtesy_name, birth_year, death_year, birthplace, dynasty, force, identity, traits)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            char['surname'],
            char['name'],
            char['courtesy_name'],
            char['birth_year'],
            char['death_year'],
            char['birthplace'],
            char.get('dynasty', '东汉'),
            char['force'],
            char['identity'],
            char['traits']
        ))
    
    conn.commit()
    print(f"已插入 {len(CHARACTERS)} 个人物")
    conn.close()

def insert_events():
    conn = get_connection()
    cursor = conn.cursor()
    
    for event in EVENTS:
        cursor.execute('''
            INSERT INTO events (event_name, event_type)
            VALUES (?, ?)
        ''', (event['name'], event['type']))
    
    conn.commit()
    print(f"已插入 {len(EVENTS)} 个事件")
    conn.close()

def insert_character_events():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取事件ID映射
    cursor.execute('SELECT id, event_name FROM events')
    event_map = {row['event_name']: row['id'] for row in cursor.fetchall()}
    
    for char_id, event_name in CHARACTER_EVENTS:
        event_id = event_map.get(event_name)
        if event_id:
            cursor.execute('''
                INSERT INTO character_events (character_id, event_id)
                VALUES (?, ?)
            ''', (char_id, event_id))
    
    conn.commit()
    print(f"已插入 {len(CHARACTER_EVENTS)} 条人物-事件关联")
    conn.close()

def insert_family_relations():
    conn = get_connection()
    cursor = conn.cursor()
    
    for char_id_1, char_id_2, relation_name in FAMILY_RELATIONS:
        cursor.execute('''
            INSERT INTO family_relations (char_id_1, char_id_2, relation_name)
            VALUES (?, ?, ?)
        ''', (char_id_1, char_id_2, relation_name))
    
    conn.commit()
    print(f"已插入 {len(FAMILY_RELATIONS)} 条亲属关系")
    conn.close()

def insert_countries():
    conn = get_connection()
    cursor = conn.cursor()
    
    for country in COUNTRIES:
        cursor.execute('''
            INSERT INTO countries (name, capital, country_chars, capital_chars, longitude, latitude, population, area, gdp_rank)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            country['name'],
            country['capital'],
            country['country_chars'],
            country['capital_chars'],
            country['longitude'],
            country['latitude'],
            country['population'],
            country['area'],
            country['gdp_rank']
        ))
    
    conn.commit()
    print(f"已插入 {len(COUNTRIES)} 个国家")
    conn.close()

def insert_watermargin():
    conn = get_connection()
    cursor = conn.cursor()
    
    for char in WATERMARGIN:
        cursor.execute('''
            INSERT INTO watermargin (surname, name, courtesy_name, nickname, star_rank, star_type, birth_year, death_year, birthplace, identity, pre_mountains, weapon, specialty, traits, ending)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            char['surname'],
            char['name'],
            char['courtesy_name'],
            char['nickname'],
            char['star_rank'],
            char['star_type'],
            char['birth_year'],
            char['death_year'],
            char['birthplace'],
            char['identity'],
            char['pre_mountains'],
            char['weapon'],
            char['specialty'],
            char['traits'],
            char['ending']
        ))
    
    conn.commit()
    print(f"已插入 {len(WATERMARGIN)} 个水浒人物")
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_characters()
    insert_events()
    insert_character_events()
    insert_family_relations()
    insert_countries()
    insert_watermargin()
    print("数据初始化完成！")
