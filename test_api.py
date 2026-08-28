import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_create_room():
    """测试创建房间"""
    response = requests.post(f"{BASE_URL}/create", json={"player": "玩家1"})
    print("创建房间响应：", response.json())
    return response.json().get('room_code')

def test_join_room(room_code):
    """测试加入房间"""
    response = requests.post(f"{BASE_URL}/join", json={"room_code": room_code, "player": "玩家2"})
    print("加入房间响应：", response.json())

def test_guess(room_code, player, character_name):
    """测试猜测"""
    response = requests.post(f"{BASE_URL}/guess", json={
        "room_code": room_code,
        "player": player,
        "character_name": character_name
    })
    print("猜测响应：", response.json())

def test_room_info(room_code):
    """测试获取房间信息"""
    response = requests.get(f"{BASE_URL}/room/{room_code}")
    print("房间信息：", response.json())

def test_characters():
    """测试获取人物列表"""
    response = requests.get(f"{BASE_URL}/characters")
    data = response.json()
    print(f"人物列表（共{len(data)}人）：")
    for c in data[:5]:  # 只显示前5个
        print(f"  {c['name']} - {c['force']} - {c['identity']}")

if __name__ == '__main__':
    print("测试API接口...\n")
    
    # 测试获取人物列表
    test_characters()
    print()
    
    # 测试创建房间
    room_code = test_create_room()
    print()
    
    # 测试加入房间
    test_join_room(room_code)
    print()
    
    # 测试猜测
    test_guess(room_code, "玩家1", "曹操")
    print()
    
    # 测试获取房间信息
    test_room_info(room_code)
