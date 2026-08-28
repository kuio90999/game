import random
import string
from database import get_connection

def generate_room_code(length=6):
    """生成房间码"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def create_room(player1):
    """创建房间"""
    conn = get_connection()
    cursor = conn.cursor()
    
    room_code = generate_room_code()
    
    # 随机选择一个人物作为答案
    cursor.execute('SELECT id FROM characters ORDER BY RANDOM() LIMIT 1')
    answer_id = cursor.fetchone()['id']
    
    cursor.execute('''
        INSERT INTO rooms (room_code, player1, answer_id, status)
        VALUES (?, ?, ?, 'playing')
    ''', (room_code, player1, answer_id))
    
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return room_code, room_id

def join_room(room_code, player2):
    """加入房间"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        return None, "房间不存在"
    
    if room['player2']:
        conn.close()
        return None, "房间已满"
    
    cursor.execute('''
        UPDATE rooms SET player2 = ?
        WHERE room_code = ?
    ''', (player2, room_code))
    
    conn.commit()
    conn.close()
    
    return room, None

def get_character_by_name(name):
    """根据名字查找人物"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 先尝试精确匹配姓+名
    cursor.execute('SELECT * FROM characters WHERE surname || name = ?', (name,))
    char = cursor.fetchone()
    
    if not char:
        # 再尝试单独匹配名
        cursor.execute('SELECT * FROM characters WHERE name = ?', (name,))
        char = cursor.fetchone()
    
    conn.close()
    return char

def get_character_by_id(char_id):
    """根据ID查找人物"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM characters WHERE id = ?', (char_id,))
    char = cursor.fetchone()
    
    conn.close()
    return char

def get_relation(char_id_1, char_id_2):
    """获取两个人物的关系"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT relation_type, event_name FROM relations 
        WHERE (char_id_1 = ? AND char_id_2 = ?) OR (char_id_1 = ? AND char_id_2 = ?)
    ''', (char_id_1, char_id_2, char_id_2, char_id_1))
    
    results = cursor.fetchall()
    conn.close()
    
    if not results:
        return None
    
    # 返回所有关系
    relations = []
    for result in results:
        relations.append({
            'type': result['relation_type'],
            'event': result['event_name']
        })
    
    return relations

def compare_characters(guess_char, answer_char):
    """比较两个人物，返回提示"""
    hints = []
    
    # 姓
    if guess_char['surname'] == answer_char['surname']:
        hints.append({"attr": "姓", "value": guess_char['surname'], "status": "一致"})
    else:
        hints.append({"attr": "姓", "value": guess_char['surname'], "status": "不一致"})
    
    # 名
    if guess_char['name'] == answer_char['name']:
        hints.append({"attr": "名", "value": guess_char['name'], "status": "一致"})
    else:
        hints.append({"attr": "名", "value": guess_char['name'], "status": "不一致"})
    
    # 字
    if guess_char['courtesy_name'] == answer_char['courtesy_name']:
        hints.append({"attr": "字", "value": guess_char['courtesy_name'], "status": "一致"})
    else:
        # 检查是否有部分相同的字
        if guess_char['courtesy_name'] != '无' and answer_char['courtesy_name'] != '无':
            common_chars = set(guess_char['courtesy_name']) & set(answer_char['courtesy_name'])
            if common_chars:
                hints.append({"attr": "字", "value": guess_char['courtesy_name'], "status": f"有相同的字：{'、'.join(common_chars)}"})
            else:
                hints.append({"attr": "字", "value": guess_char['courtesy_name'], "status": "不一致"})
        else:
            hints.append({"attr": "字", "value": guess_char['courtesy_name'], "status": "不一致"})
    
    # 生年
    if guess_char['birth_year'] and answer_char['birth_year']:
        if guess_char['birth_year'] == answer_char['birth_year']:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "一致"})
        elif guess_char['birth_year'] < answer_char['birth_year']:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "更早"})
        else:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "更晚"})
    else:
        hints.append({"attr": "生年", "value": str(guess_char['birth_year']) if guess_char['birth_year'] else "无", "status": "不一致"})
    
    # 卒年
    if guess_char['death_year'] and answer_char['death_year']:
        if guess_char['death_year'] == answer_char['death_year']:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "一致"})
        elif guess_char['death_year'] < answer_char['death_year']:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "更早"})
        else:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "更晚"})
    else:
        hints.append({"attr": "卒年", "value": str(guess_char['death_year']) if guess_char['death_year'] else "无", "status": "不一致"})
    
    # 朝代
    if guess_char['dynasty'] == answer_char['dynasty']:
        hints.append({"attr": "朝代", "value": guess_char['dynasty'], "status": "一致"})
    else:
        hints.append({"attr": "朝代", "value": guess_char['dynasty'], "status": "不一致"})
    
    # 出生地（省）
    guess_province = guess_char['birthplace'][:2] if guess_char['birthplace'] != '无' else '无'
    answer_province = answer_char['birthplace'][:2] if answer_char['birthplace'] != '无' else '无'
    
    if guess_province == answer_province:
        hints.append({"attr": "出生地", "value": guess_char['birthplace'], "status": f"同省：{guess_province}"})
    else:
        hints.append({"attr": "出生地", "value": guess_char['birthplace'], "status": "不同省"})
    
    # 势力
    if guess_char['force'] == answer_char['force']:
        hints.append({"attr": "势力", "value": guess_char['force'], "status": "一致"})
    else:
        hints.append({"attr": "势力", "value": guess_char['force'], "status": "不一致"})
    
    # 身份
    if guess_char['identity'] == answer_char['identity']:
        hints.append({"attr": "身份", "value": guess_char['identity'], "status": "一致"})
    else:
        hints.append({"attr": "身份", "value": guess_char['identity'], "status": "不一致"})
    
    # 特质
    if guess_char['traits'] == answer_char['traits']:
        hints.append({"attr": "特质", "value": guess_char['traits'], "status": "一致"})
    else:
        if guess_char['traits'] != '无' and answer_char['traits'] != '无':
            guess_traits = set(guess_char['traits'].split('·'))
            answer_traits = set(answer_char['traits'].split('·'))
            common_traits = guess_traits & answer_traits
            
            if common_traits:
                hints.append({"attr": "特质", "value": guess_char['traits'], "status": f"相同：{'、'.join(common_traits)}"})
            else:
                hints.append({"attr": "特质", "value": guess_char['traits'], "status": "无相同"})
        else:
            hints.append({"attr": "特质", "value": guess_char['traits'], "status": "不一致"})
    
    # 关系
    relations = get_relation(guess_char['id'], answer_char['id'])
    if relations:
        for relation in relations:
            if relation['type'] == '战争':
                hints.append({"attr": "关系", "value": "", "status": "经历过同一场战争"})
            elif relation['type'] == '事件':
                hints.append({"attr": "关系", "value": "", "status": "有直接关联"})
            elif relation['type'] == '亲属':
                hints.append({"attr": "关系", "value": "", "status": "亲属关系"})
    
    return hints

def make_guess(room_code, player, character_name):
    """玩家猜测"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取房间信息
    cursor.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        return None, "房间不存在"
    
    if room['status'] != 'playing':
        conn.close()
        return None, "游戏未开始或已结束"
    
    # 检查是否轮到该玩家（如果有两个玩家）
    if room['player2']:
        if room['current_turn'] == 1 and player != room['player1']:
            conn.close()
            return None, "还没轮到你"
        if room['current_turn'] == 2 and player != room['player2']:
            conn.close()
            return None, "还没轮到你"
    
    # 查找猜测的人物
    guess_char = get_character_by_name(character_name)
    if not guess_char:
        conn.close()
        return None, "人物不存在"
    
    # 获取答案人物
    answer_char = get_character_by_id(room['answer_id'])
    
    # 记录猜测
    cursor.execute('SELECT COUNT(*) as count FROM guesses WHERE room_id = ?', (room['id'],))
    guess_count = cursor.fetchone()['count']
    
    cursor.execute('''
        INSERT INTO guesses (room_id, player, character_id, guess_order)
        VALUES (?, ?, ?, ?)
    ''', (room['id'], player, guess_char['id'], guess_count + 1))
    
    # 检查是否猜对
    if guess_char['id'] == answer_char['id']:
        cursor.execute('''
            UPDATE rooms SET status = 'finished', winner = ?
            WHERE id = ?
        ''', (player, room['id']))
        conn.commit()
        conn.close()
        return {"correct": True, "answer": dict(answer_char)}, None
    
    # 切换回合（如果有两个玩家）
    if room['player2']:
        next_turn = 2 if room['current_turn'] == 1 else 1
        cursor.execute('''
            UPDATE rooms SET current_turn = ?
            WHERE id = ?
        ''', (next_turn, room['id']))
    
    conn.commit()
    conn.close()
    
    # 比较人物
    hints = compare_characters(guess_char, answer_char)
    
    # 获取所有猜测记录，用于总结
    all_guesses = get_room_guesses(room['id'])
    
    # 总结当前信息
    summary = summarize_hints(all_guesses, answer_char, hints)
    
    return {"correct": False, "hints": hints, "guess": dict(guess_char), "summary": summary}, None

def get_room_guesses(room_id):
    """获取房间的所有猜测记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT g.*, c.surname, c.name, c.courtesy_name, c.birth_year, c.death_year, c.force, c.identity, c.traits, c.dynasty, c.birthplace
        FROM guesses g 
        JOIN characters c ON g.character_id = c.id
        WHERE g.room_id = ?
        ORDER BY g.guess_order
    ''', (room_id,))
    
    guesses = cursor.fetchall()
    conn.close()
    
    return [dict(g) for g in guesses]

def summarize_hints(guesses, answer_char, current_hints=None):
    """总结当前已知信息"""
    summary = []
    
    # 生卒年范围（使用None表示未知边界）
    birth_min = None  # 生年最小值
    birth_max = None  # 生年最大值
    death_min = None  # 卒年最小值
    death_max = None  # 卒年最大值
    
    # 已确认的属性
    confirmed_force = None
    confirmed_identity = None
    confirmed_dynasty = None
    confirmed_province = None
    confirmed_traits = set()
    
    # 收集字、姓等信息
    confirmed_surname = None
    confirmed_name = None
    confirmed_courtesy_name = None
    common_chars_in_courtesy_name = set()
    
    # 从猜测记录中提取信息
    for guess in guesses:
        # 获取该猜测的提示信息
        guess_char = {
            'surname': guess['surname'],
            'name': guess['name'],
            'courtesy_name': guess['courtesy_name'],
            'birth_year': guess['birth_year'],
            'death_year': guess['death_year'],
            'birthplace': guess['birthplace'],
            'dynasty': guess['dynasty'],
            'force': guess['force'],
            'identity': guess['identity'],
            'traits': guess['traits']
        }
        
        # 比较生卒年，推断范围
        if guess['birth_year'] and answer_char['birth_year']:
            if guess['birth_year'] < answer_char['birth_year']:
                # 答案生年更晚，所以guess生年是下界
                if birth_min is None or guess['birth_year'] > birth_min:
                    birth_min = guess['birth_year']
            elif guess['birth_year'] > answer_char['birth_year']:
                # 答案生年更早，所以guess生年是上界
                if birth_max is None or guess['birth_year'] < birth_max:
                    birth_max = guess['birth_year']
        
        if guess['death_year'] and answer_char['death_year']:
            if guess['death_year'] < answer_char['death_year']:
                # 答案卒年更晚，所以guess卒年是下界
                if death_min is None or guess['death_year'] > death_min:
                    death_min = guess['death_year']
            elif guess['death_year'] > answer_char['death_year']:
                # 答案卒年更早，所以guess卒年是上界
                if death_max is None or guess['death_year'] < death_max:
                    death_max = guess['death_year']
        
        # 检查姓
        if guess['surname'] == answer_char['surname']:
            confirmed_surname = guess['surname']
        
        # 检查名
        if guess['name'] == answer_char['name']:
            confirmed_name = guess['name']
        
        # 检查字
        if guess['courtesy_name'] and answer_char['courtesy_name']:
            if guess['courtesy_name'] == answer_char['courtesy_name']:
                confirmed_courtesy_name = guess['courtesy_name']
            else:
                # 检查是否有部分相同的字
                common_chars = set(guess['courtesy_name']) & set(answer_char['courtesy_name'])
                if common_chars:
                    common_chars_in_courtesy_name.update(common_chars)
        
        # 检查是否与答案一致
        if guess['force'] == answer_char['force']:
            confirmed_force = guess['force']
        if guess['identity'] == answer_char['identity']:
            confirmed_identity = guess['identity']
        if guess['dynasty'] == answer_char['dynasty']:
            confirmed_dynasty = guess['dynasty']
        
        # 检查出生地
        guess_province = guess['birthplace'][:2] if guess['birthplace'] else None
        answer_province = answer_char['birthplace'][:2] if answer_char['birthplace'] else None
        if guess_province == answer_province:
            confirmed_province = guess_province
        
        # 检查特质
        if guess['traits'] and answer_char['traits']:
            guess_traits = set(guess['traits'].split('·'))
            answer_traits = set(answer_char['traits'].split('·'))
            common_traits = guess_traits & answer_traits
            confirmed_traits.update(common_traits)
    
    # 计算生卒年范围
    if birth_min is not None or birth_max is not None:
        if birth_min is not None and birth_max is not None:
            summary.append(f"生年：{birth_min} - {birth_max}")
        elif birth_min is not None:
            summary.append(f"生年：{birth_min} -")
        elif birth_max is not None:
            summary.append(f"生年：- {birth_max}")
    
    if death_min is not None or death_max is not None:
        if death_min is not None and death_max is not None:
            summary.append(f"卒年：{death_min} - {death_max}")
        elif death_min is not None:
            summary.append(f"卒年：{death_min} -")
        elif death_max is not None:
            summary.append(f"卒年：- {death_max}")
    
    # 已确认的姓、名、字
    if confirmed_surname:
        summary.append(f"姓：{confirmed_surname}")
    
    if confirmed_name:
        summary.append(f"名：{confirmed_name}")
    
    if confirmed_courtesy_name:
        summary.append(f"字：{confirmed_courtesy_name}")
    
    if common_chars_in_courtesy_name:
        summary.append(f"字中有相同字符：{'、'.join(common_chars_in_courtesy_name)}")
    
    # 已确认的属性
    if confirmed_force:
        summary.append(f"势力：{confirmed_force}")
    
    if confirmed_identity:
        summary.append(f"身份：{confirmed_identity}")
    
    if confirmed_dynasty:
        summary.append(f"朝代：{confirmed_dynasty}")
    
    if confirmed_province:
        summary.append(f"出生地：{confirmed_province}省")
    
    if confirmed_traits:
        summary.append(f"特质：{'、'.join(confirmed_traits)}")
    
    return summary

def get_room_info(room_code):
    """获取房间信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM rooms WHERE room_code = ?', (room_code,))
    room = cursor.fetchone()
    
    if not room:
        conn.close()
        return None
    
    # 获取猜测记录
    cursor.execute('''
        SELECT g.*, c.surname, c.name 
        FROM guesses g 
        JOIN characters c ON g.character_id = c.id
        WHERE g.room_id = ?
        ORDER BY g.guess_order
    ''', (room['id'],))
    
    guesses = cursor.fetchall()
    
    room_dict = dict(room)
    room_dict['guesses'] = [dict(g) for g in guesses]
    
    conn.close()
    return room_dict

def get_all_characters():
    """获取所有人物列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id, surname, name, force, identity FROM characters ORDER BY id')
    chars = cursor.fetchall()
    
    conn.close()
    return [dict(c) for c in chars]
