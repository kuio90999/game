import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, join_room, make_guess, get_room_info, get_all_characters

def test_game():
    """测试游戏核心功能"""
    print("三国人物猜猜猜 - 功能测试")
    print("="*40)
    
    # 测试1：获取人物列表
    print("\n1. 测试获取人物列表")
    chars = get_all_characters()
    print(f"   数据库中共有 {len(chars)} 个人物")
    print("   前5个人物：")
    for i, c in enumerate(chars[:5]):
        print(f"   {i+1}. {c['name']} ({c['force']}) - {c['identity']}")
    
    # 测试2：创建房间
    print("\n2. 测试创建房间")
    room_code, room_id = create_room("测试玩家1")
    print(f"   房间码：{room_code}")
    print(f"   房间ID：{room_id}")
    
    # 测试3：加入房间
    print("\n3. 测试加入房间")
    room, error = join_room(room_code, "测试玩家2")
    if error:
        print(f"   加入失败：{error}")
    else:
        print(f"   加入成功")
        print(f"   玩家1：{room['player1']}")
        print(f"   玩家2：测试玩家2")
    
    # 测试4：猜测功能
    print("\n4. 测试猜测功能")
    test_cases = [
        ("测试玩家1", "曹操"),
        ("测试玩家2", "刘备"),
        ("测试玩家1", "孙权"),
    ]
    
    for player, guess in test_cases:
        print(f"\n   {player} 猜测：{guess}")
        result, error = make_guess(room_code, player, guess)
        
        if error:
            print(f"   错误：{error}")
            continue
        
        if result['correct']:
            print(f"   猜对了！答案是：{result['answer']['name']}")
            break
        else:
            print(f"   猜错了，提示：")
            for hint in result['hints']:
                print(f"   - {hint}")
    
    # 测试5：房间信息
    print("\n5. 测试获取房间信息")
    room_info = get_room_info(room_code)
    print(f"   房间码：{room_info['room_code']}")
    print(f"   状态：{room_info['status']}")
    print(f"   猜测次数：{len(room_info['guesses'])}")
    
    print("\n" + "="*40)
    print("测试完成！")
    print("="*40)

if __name__ == '__main__':
    test_game()
