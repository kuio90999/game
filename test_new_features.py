import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, make_guess

def test_new_features():
    """测试新功能"""
    print("测试新功能")
    print("="*50)
    
    # 创建房间
    room_code, room_id = create_room("测试玩家")
    print(f"房间码: {room_code}")
    
    # 测试猜测
    test_cases = ["曹操", "郭嘉", "孙权"]
    
    for guess in test_cases:
        print(f"\n猜测：{guess}")
        print("-"*30)
        result, error = make_guess(room_code, "测试玩家", guess)
        
        if error:
            print(f"错误：{error}")
            continue
        
        if result['correct']:
            print(f"[OK] 猜对了！答案是：{result['answer']['name']}")
            break
        else:
            for hint in result['hints']:
                if hint['value']:
                    print(f"{hint['attr']}：{hint['value']}  {hint['status']}")
                else:
                    print(f"{hint['attr']}：{hint['status']}")
    
    print("\n" + "="*50)
    print("测试完成！")

if __name__ == '__main__':
    test_new_features()
