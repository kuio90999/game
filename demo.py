import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, join_room, make_guess, get_room_info, get_all_characters

def demo():
    """演示游戏功能"""
    print("="*50)
    print("       三国人物猜猜猜 - 功能演示")
    print("="*50)
    
    # 获取人物列表
    chars = get_all_characters()
    print(f"\n1. 人物数据库：共 {len(chars)} 个三国人物")
    print("   包括：曹操、刘备、孙权、诸葛亮、关羽等")
    
    # 创建房间
    print("\n2. 创建房间测试")
    room_code, room_id = create_room("玩家A")
    print(f"   房间码：{room_code}")
    print(f"   房间ID：{room_id}")
    
    # 加入房间
    print("\n3. 加入房间测试")
    room, error = join_room(room_code, "玩家B")
    if error:
        print(f"   加入失败：{error}")
    else:
        print(f"   玩家B成功加入房间")
        print(f"   游戏开始！")
    
    # 模拟猜测
    print("\n4. 猜测测试")
    test_guesses = ["曹操", "刘备", "孙权"]
    
    for guess_name in test_guesses:
        print(f"\n   猜测：{guess_name}")
        result, error = make_guess(room_code, "玩家A", guess_name)
        
        if error:
            print(f"   错误：{error}")
            continue
        
        if result['correct']:
            print(f"   [OK] 猜对了！答案就是 {result['answer']['name']}")
            break
        else:
            print(f"   [NO] 猜错了！提示：")
            for hint in result['hints']:
                print(f"     - {hint}")
    
    # 房间信息
    print("\n5. 房间信息")
    room_info = get_room_info(room_code)
    print(f"   房间码：{room_info['room_code']}")
    print(f"   状态：{room_info['status']}")
    print(f"   玩家1：{room_info['player1']}")
    print(f"   玩家2：{room_info['player2']}")
    print(f"   猜测次数：{len(room_info['guesses'])}")
    
    print("\n" + "="*50)
    print("演示完成！")
    print("="*50)
    print("\n要开始游戏，请运行：python run.py")

if __name__ == '__main__':
    demo()
