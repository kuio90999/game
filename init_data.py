from database import get_connection, init_db
from data import CHARACTERS, RELATIONS

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

def insert_relations():
    conn = get_connection()
    cursor = conn.cursor()
    
    for rel in RELATIONS:
        cursor.execute('''
            INSERT INTO relations (char_id_1, char_id_2, relation_type, event_name)
            VALUES (?, ?, ?, ?)
        ''', rel)
    
    conn.commit()
    print(f"已插入 {len(RELATIONS)} 条关系")
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_characters()
    insert_relations()
    print("数据初始化完成！")
