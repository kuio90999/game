import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import init_db
from init_data import insert_characters, insert_events, insert_character_events, insert_family_relations, insert_countries
from api import app

def setup():
    """初始化数据库和数据"""
    print("正在初始化游戏...")
    init_db()
    
    # 检查是否已有数据
    from database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    
    # 检查人物数据
    cursor.execute('SELECT COUNT(*) as count FROM characters')
    char_count = cursor.fetchone()['count']
    
    # 检查国家数据
    cursor.execute('SELECT COUNT(*) as count FROM countries')
    country_count = cursor.fetchone()['count']
    
    conn.close()
    
    if char_count == 0:
        print("正在导入三国人物数据...")
        insert_characters()
        insert_events()
        insert_character_events()
        insert_family_relations()
        print("三国人物数据导入完成！")
    else:
        print(f"数据库已存在 {char_count} 个人物")
    
    if country_count == 0:
        print("正在导入世界国家数据...")
        insert_countries()
        print("世界国家数据导入完成！")
    else:
        print(f"数据库已存在 {country_count} 个国家")
    
    print("初始化完成！\n")

if __name__ == '__main__':
    setup()
    print("="*50)
    print("猜一下 - 游戏平台")
    print("="*50)
    print("服务器启动中...")
    print("请在浏览器中访问: http://localhost:8080")
    print("="*50)
    app.run(debug=True, port=8080, host='0.0.0.0')
