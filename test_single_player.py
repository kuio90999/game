import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, join_room, make_guess, get_room_info, get_all_characters

def test_single_player():
    """测试单人游戏功能"""
    print("三国人物猜猜猜 - 单人游戏测试")
    print("="*40)
    
    # 创建房间
    print("\n1. 创建房间（单人模式）")
    room_code, room_id = create_room("单人玩家")
    print(f"   房间码：{room_code}")
    print(f"   游戏已开始！")
    
    # 获取房间信息
    room_info = get_room_info(room_code)
    print(f"   状态：{room_info['status']}")
    print(f"   玩家2：{room_info['player2'] or '无（单人模式）'}")
    
    # 测试猜测
    print("\n2. 测试猜测功能")
    test_guesses = ["曹操", "刘备", "孙权", "诸葛亮"]
    
    for guess in test_guesses:
        print(f"\n   猜测：{guess}")
        result, error = make_guess(room_code, "单人玩家", guess)
        
        if error:
            print(f"   错误：{error}")
            continue
        
        if result['correct']:
            print(f"   [OK] 猜对了！答案是：{result['answer']['name']}")
            break
        else:
            print(f"   [NO] 猜错了，提示：")
            for hint in result['hints']:
                print(f"     - {hint}")
    
    # 最终房间信息
    print("\n3. 最终房间信息")
    room_info = get_room_info(room_code)
    print(f"   状态：{room_info['status']}")
    print(f"   猜测次数：{len(room_info['guesses'])}")
    if room_info['winner']:
        print(f"   胜者：{room_info['winner']}")
    
    print("\n" + "="*40)
    print("单人游戏测试完成！")
    print("="*40)

def test_two_player():
    """测试双人游戏功能"""
    print("\n\n三国人物猜猜猜 - 双人游戏测试")
    print("="*40)
    
    # 玩家1创建房间
    print("\n1. 玩家1创建房间")
    room_code, room_id = create_room("玩家A")
    print(f"   房间码：{room_code}")
    
    # 玩家2加入房间
    print("\n2. 玩家2加入房间")
    room, error = join_room(room_code, "玩家B")
    if error:
        print(f"   加入失败：{error}")
        return
    print(f"   加入成功！")
    
    # 获取房间信息
    room_info = get_room_info(room_code)
    print(f"   玩家1：{room_info['player1']}")
    print(f"   玩家2：{room_info['player2']}")
    print(f"   当前回合：{'玩家1' if room_info['current_turn'] == 1 else '玩家2'}")
    
    # 测试轮流猜测
    print("\n3. 测试轮流猜测")
    test_cases = [
        ("玩家A", "曹操"),
        ("玩家B", "刘备"),
        ("玩家A", "孙权"),
        ("玩家B", "诸葛亮"),
    ]
    
    for player, guess in test_cases:
        print(f"\n   {player} 猜测：{guess}")
        result, error = make_guess(room_code, player, guess)
        
        if error:
            print(f"   错误：{error}")
            continue
        
        if result['correct']:
            print(f"   [OK] 猜对了！答案是：{result['answer']['name']}")
            break
        else:
            print(f"   [NO] 猜错了，提示：")
            for hint in result['hints']:
                print(f"     - {hint}")
            
            # 更新房间信息查看回合
            room_info = get_room_info(room_code)
            print(f"   下一回合：{'玩家1' if room_info['current_turn'] == 1 else '玩家2'}")
    
    print("\n" + "="*40)
    print("双人游戏测试完成！")
    print("="*40)

if __name__ == '__main__':
    test_single_player()
    test_two_player()
