import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, make_guess, get_room_info

def test_improved_hints():
    """测试改进后的提示功能"""
    print("测试改进后的提示功能")
    print("="*50)
    
    # 创建房间
    room_code, room_id = create_room("测试玩家")
    print(f"房间码: {room_code}")
    
    # 测试猜测
    test_cases = ["曹操", "郭嘉", "孙权"]
    
    for guess in test_cases:
        print(f"\n猜测: {guess}")
        result, error = make_guess(room_code, "测试玩家", guess)
        
        if error:
            print(f"错误: {error}")
            continue
        
        if result['correct']:
            print(f"[OK] 猜对了！答案是：{result['answer']['name']}")
            break
        else:
            print(f"[NO] 猜错了，提示：")
            for hint in result['hints']:
                print(f"  - {hint}")
    
    print("\n" + "="*50)
    print("测试完成！")

if __name__ == '__main__':
    test_improved_hints()
