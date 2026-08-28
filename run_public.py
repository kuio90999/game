import sys
import os
import subprocess
import threading
import time
sys.path.append(os.path.dirname(__file__))

from database import init_db
from init_data import insert_characters, insert_relations
from api import app

def setup():
    """初始化数据库和数据"""
    print("正在初始化游戏...")
    init_db()
    
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

def run_flask():
    """运行Flask服务器"""
    app.run(debug=False, port=5000, host='0.0.0.0')

def run_ngrok():
    """运行ngrok内网穿透"""
    try:
        # 检查ngrok是否安装
        result = subprocess.run(['ngrok', 'version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("未检测到ngrok，请先安装ngrok")
            print("访问 https://ngrok.com/download 下载")
            return
        
        print("正在启动ngrok内网穿透...")
        ngrok_process = subprocess.Popen(
            ['ngrok', 'http', '5000'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # 等待ngrok启动
        time.sleep(3)
        
        print("\n" + "="*60)
        print("内网穿透已启动！")
        print("="*60)
        print("请访问 http://127.0.0.1:4040 查看公网地址")
        print("或者查看ngrok控制台输出的Forwarding地址")
        print("="*60)
        
        # 保持ngrok运行
        ngrok_process.wait()
        
    except FileNotFoundError:
        print("未检测到ngrok，请先安装ngrok")
        print("访问 https://ngrok.com/download 下载")
    except Exception as e:
        print(f"启动ngrok失败: {e}")

def main():
    setup()
    
    print("="*60)
    print("三国人物猜猜猜 - 网页版（支持外网访问）")
    print("="*60)
    print("本地访问: http://localhost:5000")
    print("局域网访问: http://你的IP地址:5000")
    print("="*60)
    
    # 启动Flask服务器（在后台线程）
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 等待Flask启动
    time.sleep(2)
    
    print("\n请选择内网穿透方案：")
    print("1. ngrok（推荐，最简单）")
    print("2. 不使用内网穿透（仅局域网访问）")
    print("3. 使用localtunnel")
    
    choice = input("\n请输入选项编号: ").strip()
    
    if choice == '1':
        run_ngrok()
    elif choice == '2':
        print("\n游戏已启动，仅支持局域网访问")
        print("按 Ctrl+C 退出")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n游戏已退出")
    elif choice == '3':
        try:
            print("正在启动localtunnel...")
            lt_process = subprocess.Popen(
                ['lt', '--port', '5000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            time.sleep(3)
            print("\nlocaltunnel已启动，请查看上方输出的URL")
            lt_process.wait()
        except FileNotFoundError:
            print("未检测到localtunnel，请先安装：npm install -g localtunnel")
    else:
        print("无效的选项")

if __name__ == '__main__':
    main()
