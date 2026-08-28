import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import init_db
from init_data import insert_characters, insert_relations
from cli import GameCLI

def setup():
    """初始化数据库和数据"""
    print("正在初始化游戏...")
    init_db()
    
    # 检查是否已有数据
    from database import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as count FROM characters')
    count = cursor.fetchone()['count']
    conn.close()
    
    if count == 0:
        print("正在导入三国人物数据...")
        insert_characters()
        insert_relations()
        print("数据导入完成！")
    else:
        print(f"数据库已存在 {count} 个人物")
    
    print("初始化完成！\n")

if __name__ == '__main__':
    setup()
    game = GameCLI()
    game.run()
