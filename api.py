from flask import Flask, request, jsonify, render_template, send_from_directory
from game import create_room, join_room, make_guess, get_room_info, get_all_characters, get_character_by_id
import os

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """静态文件"""
    return send_from_directory('static', filename)

@app.route('/api/create', methods=['POST'])
def api_create_room():
    """创建房间"""
    data = request.json
    player = data.get('player')
    
    if not player:
        return jsonify({"error": "请输入玩家名称"}), 400
    
    room_code, room_id = create_room(player)
    
    return jsonify({
        "room_code": room_code,
        "room_id": room_id,
        "message": f"房间创建成功！房间码：{room_code}"
    })

@app.route('/api/join', methods=['POST'])
def api_join_room():
    """加入房间"""
    data = request.json
    room_code = data.get('room_code')
    player = data.get('player')
    
    if not room_code or not player:
        return jsonify({"error": "请输入房间码和玩家名称"}), 400
    
    room, error = join_room(room_code, player)
    
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({
        "message": f"成功加入房间！游戏开始！",
        "player1": room['player1'],
        "player2": player
    })

@app.route('/api/guess', methods=['POST'])
def api_guess():
    """猜测人物"""
    data = request.json
    room_code = data.get('room_code')
    player = data.get('player')
    character_name = data.get('character_name')
    
    if not room_code or not player or not character_name:
        return jsonify({"error": "请输入房间码、玩家名称和猜测人物"}), 400
    
    result, error = make_guess(room_code, player, character_name)
    
    if error:
        return jsonify({"error": error}), 400
    
    if result['correct']:
        return jsonify({
            "correct": True,
            "message": f"恭喜！答案就是【{result['answer']['surname']}{result['answer']['name']}】！",
            "answer": result['answer']
        })
    else:
        # 格式化提示信息
        hints_text = []
        for hint in result['hints']:
            if hint['value']:
                hints_text.append(f"{hint['attr']}：{hint['value']}  {hint['status']}")
            else:
                hints_text.append(f"{hint['attr']}：{hint['status']}")
        
        return jsonify({
            "correct": False,
            "hints": result['hints'],
            "guess": result['guess'],
            "summary": result.get('summary', []),
            "message": "猜错了！\n" + "\n".join(hints_text)
        })

@app.route('/api/room/<room_code>', methods=['GET'])
def api_room_info(room_code):
    """获取房间信息"""
    room = get_room_info(room_code)
    
    if not room:
        return jsonify({"error": "房间不存在"}), 404
    
    return jsonify(room)

@app.route('/api/characters', methods=['GET'])
def api_characters():
    """获取所有人物列表"""
    chars = get_all_characters()
    return jsonify(chars)

@app.route('/api/character/<int:char_id>', methods=['GET'])
def api_character(char_id):
    """获取单个人物信息"""
    char = get_character_by_id(char_id)
    
    if not char:
        return jsonify({"error": "人物不存在"}), 404
    
    return jsonify(dict(char))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
