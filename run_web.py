import sys
import os
sys.path.append(os.path.dirname(__file__))

from database import init_db
from init_data import insert_characters, insert_relations
from api import app

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
    print("="*50)
    print("三国人物猜猜猜 - 网页版")
    print("="*50)
    print("服务器启动中...")
    print("请在浏览器中访问: http://localhost:5000")
    print("="*50)
    app.run(debug=True, port=5000, host='0.0.0.0')
