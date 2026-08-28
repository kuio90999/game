import sys
import os
sys.path.append(os.path.dirname(__file__))

from game import create_room, join_room, make_guess, get_room_info, get_all_characters

class GameCLI:
    def __init__(self):
        self.current_room = None
        self.player_name = None
        self.is_player1 = False
    
    def print_banner(self):
        print("\n" + "="*50)
        print("       三国人物猜猜猜")
        print("="*50)
        print("猜出系统预设的三国人物！")
        print("支持单人练习或两人对战！")
        print("="*50 + "\n")
    
    def print_menu(self):
        print("\n请选择操作：")
        print("1. 创建房间")
        print("2. 加入房间")
        print("3. 查看房间信息")
        print("4. 开始游戏")
        print("5. 查看人物列表")
        print("0. 退出游戏")
        print("-"*30)
    
    def create_room(self):
        name = input("请输入你的名字：").strip()
        if not name:
            print("名字不能为空！")
            return
        
        room_code, room_id = create_room(name)
        self.current_room = room_code
        self.player_name = name
        self.is_player1 = True
        
        print(f"\n房间创建成功！")
        print(f"房间码：{room_code}")
        print(f"游戏已开始！你现在可以猜测人物了。")
        print(f"你也可以分享房间码给朋友，让他加入对战。\n")
    
    def join_room(self):
        name = input("请输入你的名字：").strip()
        if not name:
            print("名字不能为空！")
            return
        
        room_code = input("请输入房间码：").strip().upper()
        if not room_code:
            print("房间码不能为空！")
            return
        
        room, error = join_room(room_code, name)
        if error:
            print(f"加入失败：{error}")
            return
        
        self.current_room = room_code
        self.player_name = name
        self.is_player1 = False
        
        print(f"\n成功加入房间！")
        print(f"玩家1：{room['player1']}")
        print(f"玩家2：{name}")
        print(f"游戏开始！请轮流猜测人物。\n")
    
    def view_room(self):
        if not self.current_room:
            print("你还没有加入任何房间！")
            return
        
        room = get_room_info(self.current_room)
        if not room:
            print("房间不存在！")
            return
        
        print(f"\n房间信息：")
        print(f"房间码：{room['room_code']}")
        print(f"状态：{room['status']}")
        print(f"玩家1：{room['player1']}")
        if room['player2']:
            print(f"玩家2：{room['player2']}")
            print(f"当前回合：{'玩家1' if room['current_turn'] == 1 else '玩家2'}")
        else:
            print(f"玩家2：等待加入（当前单人模式）")
        
        if room['status'] == 'finished':
            print(f"胜者：{room['winner']}")
        
        if room['guesses']:
            print(f"\n猜测记录：")
            for g in room['guesses']:
                full_name = g['surname'] + g['name']
                print(f"  {g['player']} 猜测了：{full_name}")
        print()
    
    def start_game(self):
        """开始游戏循环"""
        if not self.current_room:
            print("你还没有加入任何房间！")
            return
        
        room = get_room_info(self.current_room)
        if not room:
            print("房间不存在！")
            return
        
        if room['status'] == 'finished':
            print(f"游戏已结束！胜者是：{room['winner']}")
            return
        
        print(f"\n游戏开始！输入人物名字进行猜测，输入 'quit' 退出游戏")
        print("-"*50)
        
        while True:
            # 检查游戏是否结束
            room = get_room_info(self.current_room)
            if room['status'] == 'finished':
                print(f"\n游戏已结束！胜者是：{room['winner']}")
                break
            
            # 检查是否轮到自己（有两个玩家时）
            if room['player2']:
                if room['current_turn'] == 1 and self.player_name != room['player1']:
                    print("等待玩家1猜测...")
                    continue
                if room['current_turn'] == 2 and self.player_name != room['player2']:
                    print("等待玩家2猜测...")
                    continue
            
            char_name = input("\n请输入猜测的人物名字：").strip()
            
            if char_name.lower() == 'quit':
                print("退出游戏")
                break
            
            if not char_name:
                print("人物名字不能为空！")
                continue
            
            result, error = make_guess(self.current_room, self.player_name, char_name)
            
            if error:
                print(f"猜测失败：{error}")
                continue
            
            if result['correct']:
                full_name = result['answer']['surname'] + result['answer']['name']
                print(f"\n{'='*50}")
                print(f"恭喜你猜对了！答案就是【{full_name}】！")
                print(f"{'='*50}")
                break
            else:
                print(f"\n猜测：{char_name}")
                print("-"*30)
                for hint in result['hints']:
                    if hint['value']:
                        print(f"{hint['attr']}：{hint['value']}  {hint['status']}")
                    else:
                        print(f"{hint['attr']}：{hint['status']}")
                
                # 显示总结信息
                if result.get('summary'):
                    print("\n当前限定范围：")
                    print("-"*30)
                    for item in result['summary']:
                        print(f"  {item}")
    
    def list_characters(self):
        chars = get_all_characters()
        print(f"\n三国人物列表（共{len(chars)}人）：")
        print("-"*50)
        
        # 按势力分组
        forces = {}
        for c in chars:
            force = c['force'] or '其他'
            if force not in forces:
                forces[force] = []
            forces[force].append(c)
        
        for force, members in forces.items():
            print(f"\n【{force}】")
            for c in members:
                full_name = c['surname'] + c['name']
                print(f"  {full_name} - {c['identity']}")
        
        print()
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input("请输入选项编号：").strip()
            
            if choice == '1':
                self.create_room()
            elif choice == '2':
                self.join_room()
            elif choice == '3':
                self.view_room()
            elif choice == '4':
                self.start_game()
            elif choice == '5':
                self.list_characters()
            elif choice == '0':
                print("\n再见！")
                break
            else:
                print("无效的选项，请重新输入。")

if __name__ == '__main__':
    game = GameCLI()
    game.run()
