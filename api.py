from flask import Flask, request, jsonify, render_template, send_from_directory
from game import get_all_characters, get_character_by_id, get_character_by_name, compare_characters, summarize_hints, get_relation
from country_game import get_all_countries, get_country_by_name, get_country_by_id, compare_countries, summarize_country_hints
from watermargin_game import get_all_watermargin, get_watermargin_by_name, get_watermargin_by_id, compare_watermargin
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

# 水浒人物游戏状态
watermargin_state = {
    'answer_id': None,
    'guesses': [],
    'shown_hints': []  # 已显示的提示项
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

@app.route('/watermargin')
def watermargin():
    """水浒人物游戏"""
    return render_template('watermargin.html')

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
            "answer": dict(answer_country),
            "guess_count": len(country_state['guesses']) + 1
        })
    
    hints = compare_countries(guess_country, answer_country)
    country_state['guesses'].append(dict(guess_country))
    summary = summarize_country_hints(country_state['guesses'], answer_country)
    
    guess_count = len(country_state['guesses'])
    
    return jsonify({
        "correct": False,
        "hints": hints,
        "guess": dict(guess_country),
        "summary": summary,
        "guess_count": guess_count
    })

# ==================== 水浒人物游戏 API ====================

@app.route('/api/watermargin/characters', methods=['GET'])
def api_watermargin_characters():
    """获取水浒人物列表"""
    chars = get_all_watermargin()
    return jsonify(chars)

@app.route('/api/watermargin/new-game', methods=['POST'])
def api_watermargin_new_game():
    """开始新游戏"""
    chars = get_all_watermargin()
    answer = random.choice(chars)
    watermargin_state['answer_id'] = answer['id']
    watermargin_state['guesses'] = []
    watermargin_state['shown_hints'] = []
    
    # 计算姓名和绰号的字数
    name = answer['surname'] + answer['name']
    nickname = answer['nickname'] or ''
    
    # 生成初始提示（必给姓名和绰号字数）
    initial_hints = [
        {"type": "name_chars", "label": "姓名", "value": f"{len(name)}个字"},
        {"type": "nickname_chars", "label": "绰号", "value": f"{len(nickname)}个字"}
    ]
    
    # 从其他提示项中随机选择2项
    other_hints = [
        {"type": "star_type", "label": "星位", "value": answer['star_type']},
        {"type": "birthplace", "label": "祖籍", "value": answer['birthplace'][:2] + "省"},
        {"type": "identity", "label": "身份", "value": answer['identity']},
        {"type": "pre_mountains", "label": "上山前身份", "value": answer['pre_mountains']},
        {"type": "weapon", "label": "专属武器", "value": "有" if answer['weapon'] != '无' else "无"},
        {"type": "specialty", "label": "特殊技能", "value": "有" if answer['specialty'] != '无' else "无"},
        {"type": "ending", "label": "自然死亡", "value": "是" if answer['ending'] in ['善终', '病死', '圆寂', '出家', '归隐'] else "否"},
        {"type": "battle", "label": "参与战争", "value": answer['battle'] if answer['battle'] != '无' else "未参与"},
        {"type": "nickname_type", "label": "绰号特点", "value": get_nickname_type(answer['nickname'])}
    ]
    
    # 随机选择2项
    selected = random.sample(other_hints, 2)
    initial_hints.extend(selected)
    
    # 记录已显示的提示
    watermargin_state['shown_hints'] = [hint['type'] for hint in initial_hints]
    
    return jsonify({
        'answer': {
            'id': answer['id'],
            'name_chars': len(name),
            'nickname_chars': len(nickname)
        },
        'initial_hints': initial_hints,
        'message': '新游戏开始！'
    })

def get_nickname_type(nickname):
    """判断绰号类型"""
    if not nickname:
        return "无"
    
    animals = ['龙', '虎', '蛇', '蝎', '凤', '鹤', '马', '狗', '鼠', '龟', '蛟', '蜃', '雕', '鹰', '豹', '熊', '鹿', '猿', '蛇', '蝎']
    materials = ['金', '银', '铁', '铜', '玉', '石', '钢']
    numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万']
    
    has_animal = any(a in nickname for a in animals)
    has_material = any(m in nickname for m in materials)
    has_number = any(n in nickname for n in numbers)
    
    results = []
    if has_animal:
        results.append("动物")
    if has_material:
        results.append("材料")
    if has_number:
        results.append("数字")
    
    return "、".join(results) if results else "都没有"

@app.route('/api/watermargin/guess', methods=['POST'])
def api_watermargin_guess():
    """猜测人物"""
    data = request.json
    character_name = data.get('character_name')
    
    if not character_name:
        return jsonify({"error": "请输入人物名字"}), 400
    
    if not watermargin_state['answer_id']:
        return jsonify({"error": "游戏未开始"}), 400
    
    guess_char = get_watermargin_by_name(character_name)
    if not guess_char:
        return jsonify({"error": "人物不存在"}), 400
    
    answer_char = get_watermargin_by_id(watermargin_state['answer_id'])
    
    guess_name = guess_char['surname'] + guess_char['name']
    answer_name = answer_char['surname'] + answer_char['name']
    print(f"[水浒猜测日志] 猜测: {guess_name} - 答案: {answer_name}")
    
    if guess_char['id'] == answer_char['id']:
        return jsonify({
            "correct": True,
            "answer": dict(answer_char),
            "guess_count": len(watermargin_state['guesses']) + 1
        })
    
    hints = compare_watermargin(guess_char, answer_char)
    watermargin_state['guesses'].append(dict(guess_char))
    
    return jsonify({
        "correct": False,
        "hints": hints,
        "guess": dict(guess_char),
        "guess_count": len(watermargin_state['guesses'])
    })

@app.route('/api/watermargin/get-hint', methods=['POST'])
def api_watermargin_get_hint():
    """获取额外提示"""
    if not watermargin_state['answer_id']:
        return jsonify({"error": "游戏未开始"}), 400
    
    answer_char = get_watermargin_by_id(watermargin_state['answer_id'])
    
    # 所有可选的提示项
    all_hints = [
        {"type": "star_type", "label": "星位", "value": answer_char['star_type']},
        {"type": "birthplace", "label": "祖籍", "value": answer_char['birthplace'][:2] + "省"},
        {"type": "identity", "label": "身份", "value": answer_char['identity']},
        {"type": "pre_mountains", "label": "上山前身份", "value": answer_char['pre_mountains']},
        {"type": "weapon", "label": "专属武器", "value": "有" if answer_char['weapon'] != '无' else "无"},
        {"type": "specialty", "label": "特殊技能", "value": "有" if answer_char['specialty'] != '无' else "无"},
        {"type": "ending", "label": "自然死亡", "value": "是" if answer_char['ending'] in ['善终', '病死', '圆寂', '出家', '归隐'] else "否"},
        {"type": "battle", "label": "参与战争", "value": answer_char['battle'] if answer_char['battle'] != '无' else "未参与"},
        {"type": "nickname_type", "label": "绰号特点", "value": get_nickname_type(answer_char['nickname'])}
    ]
    
    # 过滤掉已显示的提示
    available_hints = [h for h in all_hints if h['type'] not in watermargin_state['shown_hints']]
    
    if not available_hints:
        return jsonify({"error": "没有更多提示了"}), 400
    
    # 随机选择一项
    hint = random.choice(available_hints)
    watermargin_state['shown_hints'].append(hint['type'])
    
    return jsonify({
        "hint": hint,
        "remaining_hints": len(available_hints) - 1
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
