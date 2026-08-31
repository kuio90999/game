from flask import Flask, request, jsonify, render_template, send_from_directory
from game import get_all_characters, get_character_by_id, get_character_by_name, compare_characters, summarize_hints, get_relation
from country_game import get_all_countries, get_country_by_name, get_country_by_id, compare_countries, summarize_country_hints
import random

app = Flask(__name__, 
            static_folder='static',
            template_folder='templates')

# 三国人物游戏状态
sanguo_state = {
    'answer_id': None,
    'guesses': []
}

# 世界国家游戏状态
country_state = {
    'answer_id': None,
    'guesses': []
}

@app.route('/')
def home():
    """主页"""
    return render_template('home.html')

@app.route('/sanguo')
def sanguo():
    """三国人物游戏"""
    return render_template('sanguo.html')

@app.route('/country')
def country():
    """世界国家游戏"""
    return render_template('country.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """静态文件"""
    return send_from_directory('static', filename)

# ==================== 三国人物游戏 API ====================

@app.route('/api/sanguo/characters', methods=['GET'])
def api_sanguo_characters():
    """获取三国人物列表"""
    chars = get_all_characters()
    return jsonify(chars)

@app.route('/api/sanguo/new-game', methods=['POST'])
def api_sanguo_new_game():
    """开始新游戏"""
    chars = get_all_characters()
    answer = random.choice(chars)
    sanguo_state['answer_id'] = answer['id']
    sanguo_state['guesses'] = []
    
    return jsonify({
        'answer_id': answer['id'],
        'message': '新游戏开始！'
    })

@app.route('/api/sanguo/guess', methods=['POST'])
def api_sanguo_guess():
    """猜测人物"""
    data = request.json
    character_name = data.get('character_name')
    
    if not character_name:
        return jsonify({"error": "请输入人物名字"}), 400
    
    if not sanguo_state['answer_id']:
        return jsonify({"error": "游戏未开始"}), 400
    
    guess_char = get_character_by_name(character_name)
    if not guess_char:
        return jsonify({"error": "人物不存在"}), 400
    
    answer_char = get_character_by_id(sanguo_state['answer_id'])
    
    guess_name = guess_char['surname'] + guess_char['name']
    answer_name = answer_char['surname'] + answer_char['name']
    print(f"[三国猜测日志] 猜测: {guess_name} - 答案: {answer_name}")
    
    if guess_char['id'] == answer_char['id']:
        return jsonify({
            "correct": True,
            "answer": dict(answer_char)
        })
    
    hints = compare_characters(guess_char, answer_char)
    sanguo_state['guesses'].append(dict(guess_char))
    summary = summarize_hints(sanguo_state['guesses'], answer_char, hints)
    
    return jsonify({
        "correct": False,
        "hints": hints,
        "guess": dict(guess_char),
        "summary": summary
    })

# ==================== 世界国家游戏 API ====================

@app.route('/api/country/countries', methods=['GET'])
def api_country_countries():
    """获取国家列表"""
    countries = get_all_countries()
    return jsonify(countries)

@app.route('/api/country/new-game', methods=['POST'])
def api_country_new_game():
    """开始新游戏"""
    countries = get_all_countries()
    answer = random.choice(countries)
    country_state['answer_id'] = answer['id']
    country_state['guesses'] = []
    
    return jsonify({
        'answer': {
            'id': answer['id'],
            'country_chars': answer['country_chars'],
            'capital_chars': answer['capital_chars']
        },
        'message': '新游戏开始！'
    })

@app.route('/api/country/guess', methods=['POST'])
def api_country_guess():
    """猜测国家"""
    data = request.json
    country_name = data.get('country_name')
    
    if not country_name:
        return jsonify({"error": "请输入国家名称"}), 400
    
    if not country_state['answer_id']:
        return jsonify({"error": "游戏未开始"}), 400
    
    guess_country = get_country_by_name(country_name)
    if not guess_country:
        return jsonify({"error": "国家不存在"}), 400
    
    answer_country = get_country_by_id(country_state['answer_id'])
    
    print(f"[国家猜测日志] 猜测: {country_name} - 答案: {answer_country['name']}")
    
    if guess_country['id'] == answer_country['id']:
        return jsonify({
            "correct": True,
            "answer": dict(answer_country)
        })
    
    hints = compare_countries(guess_country, answer_country)
    country_state['guesses'].append(dict(guess_country))
    summary = summarize_country_hints(country_state['guesses'], answer_country)
    
    return jsonify({
        "correct": False,
        "hints": hints,
        "guess": dict(guess_country),
        "summary": summary
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
