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
    
    relations = []
    
    # 查询两个人物共同参与的事件
    cursor.execute('''
        SELECT DISTINCT e.event_name, e.event_type
        FROM character_events ce1
        JOIN character_events ce2 ON ce1.event_id = ce2.event_id
        JOIN events e ON ce1.event_id = e.id
        WHERE ce1.character_id = ? AND ce2.character_id = ?
    ''', (char_id_1, char_id_2))
    
    events = cursor.fetchall()
    for event in events:
        relations.append({
            'type': event['event_type'],
            'event': event['event_name']
        })
    
    # 查询亲属关系
    cursor.execute('''
        SELECT relation_name FROM family_relations
        WHERE (char_id_1 = ? AND char_id_2 = ?) OR (char_id_1 = ? AND char_id_2 = ?)
    ''', (char_id_1, char_id_2, char_id_2, char_id_1))
    
    family = cursor.fetchone()
    if family:
        relations.append({
            'type': '亲属',
            'event': family['relation_name']
        })
    
    conn.close()
    
    return relations if relations else None

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
    if guess_char['birth_year'] is None and answer_char['birth_year'] is None:
        hints.append({"attr": "生年", "value": "不详", "status": "一致"})
    elif guess_char['birth_year'] is None:
        hints.append({"attr": "生年", "value": "不详", "status": "不一致"})
    elif answer_char['birth_year'] is None:
        hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "不一致"})
    else:
        if guess_char['birth_year'] == answer_char['birth_year']:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "一致"})
        elif guess_char['birth_year'] < answer_char['birth_year']:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "更早"})
        else:
            hints.append({"attr": "生年", "value": str(guess_char['birth_year']), "status": "更晚"})
    
    # 卒年
    if guess_char['death_year'] is None and answer_char['death_year'] is None:
        hints.append({"attr": "卒年", "value": "不详", "status": "一致"})
    elif guess_char['death_year'] is None:
        hints.append({"attr": "卒年", "value": "不详", "status": "不一致"})
    elif answer_char['death_year'] is None:
        hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "不一致"})
    else:
        if guess_char['death_year'] == answer_char['death_year']:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "一致"})
        elif guess_char['death_year'] < answer_char['death_year']:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "更早"})
        else:
            hints.append({"attr": "卒年", "value": str(guess_char['death_year']), "status": "更晚"})
    
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
    
    # 打印日志
    guess_name = guess_char['surname'] + guess_char['name']
    answer_name = answer_char['surname'] + answer_char['name']
    print(f"[猜测日志] {player} - 猜测: {guess_name} - 答案: {answer_name}")
    
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
    birth_exact = None  # 确切的生年
    death_exact = None  # 确切的卒年
    
    # 已确认的属性
    confirmed_force = None
    confirmed_identity = None
    confirmed_dynasty = None
    confirmed_province = None
    
    # 收集所有猜测过的势力、身份、特质（用于显示匹配/不匹配）
    guessed_forces = set()
    guessed_identities = set()
    guessed_traits = set()
    
    # 收集字、姓等信息
    confirmed_surname = None
    confirmed_name = None
    confirmed_courtesy_name = None
    common_chars_in_courtesy_name = set()
    
    # 从猜测记录中提取信息
    for guess in guesses:
        # 比较生卒年，推断范围
        if guess['birth_year'] and answer_char['birth_year']:
            if guess['birth_year'] == answer_char['birth_year']:
                birth_exact = guess['birth_year']
            elif guess['birth_year'] < answer_char['birth_year']:
                # 答案生年更晚，所以guess生年是下界
                if birth_min is None or guess['birth_year'] > birth_min:
                    birth_min = guess['birth_year']
            elif guess['birth_year'] > answer_char['birth_year']:
                # 答案生年更早，所以guess生年是上界
                if birth_max is None or guess['birth_year'] < birth_max:
                    birth_max = guess['birth_year']
        
        if guess['death_year'] and answer_char['death_year']:
            if guess['death_year'] == answer_char['death_year']:
                death_exact = guess['death_year']
            elif guess['death_year'] < answer_char['death_year']:
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
        
        # 收集猜测过的势力、身份、特质
        guessed_forces.add(guess['force'])
        guessed_identities.add(guess['identity'])
        if guess['traits']:
            guessed_traits.update(guess['traits'].split('·'))
        
        # 检查出生地
        guess_province = guess['birthplace'][:2] if guess['birthplace'] else None
        answer_province = answer_char['birthplace'][:2] if answer_char['birthplace'] else None
        if guess_province == answer_province:
            confirmed_province = guess_province
    
    # 计算生卒年范围
    if birth_exact:
        summary.append({"type": "text", "content": f"生年：{birth_exact}"})
    elif birth_min is not None or birth_max is not None:
        if birth_min is not None and birth_max is not None:
            summary.append({"type": "text", "content": f"生年：{birth_min} - {birth_max}"})
        elif birth_min is not None:
            summary.append({"type": "text", "content": f"生年：{birth_min} -"})
        elif birth_max is not None:
            summary.append({"type": "text", "content": f"生年：- {birth_max}"})
    
    if death_exact:
        summary.append({"type": "text", "content": f"卒年：{death_exact}"})
    elif death_min is not None or death_max is not None:
        if death_min is not None and death_max is not None:
            summary.append({"type": "text", "content": f"卒年：{death_min} - {death_max}"})
        elif death_min is not None:
            summary.append({"type": "text", "content": f"卒年：{death_min} -"})
        elif death_max is not None:
            summary.append({"type": "text", "content": f"卒年：- {death_max}"})
    
    # 已确认的姓、名、字
    if confirmed_surname:
        summary.append({"type": "text", "content": f"姓：{confirmed_surname}"})
    
    if confirmed_name:
        summary.append({"type": "text", "content": f"名：{confirmed_name}"})
    
    if confirmed_courtesy_name:
        summary.append({"type": "text", "content": f"字：{confirmed_courtesy_name}"})
    
    if common_chars_in_courtesy_name:
        summary.append({"type": "text", "content": f"字中有相同字符：{'、'.join(common_chars_in_courtesy_name)}"})
    
    # 势力（显示所有猜测过的势力，匹配的绿色，不匹配的灰色）
    if guessed_forces:
        force_items = []
        for force in guessed_forces:
            is_match = (force == answer_char['force'])
            force_items.append({"value": force, "match": is_match})
        summary.append({"type": "tags", "attr": "势力", "items": force_items})
    
    # 身份（显示所有猜测过的身份，匹配的绿色，不匹配的灰色）
    if guessed_identities:
        identity_items = []
        for identity in guessed_identities:
            is_match = (identity == answer_char['identity'])
            identity_items.append({"value": identity, "match": is_match})
        summary.append({"type": "tags", "attr": "身份", "items": identity_items})
    
    # 特质（显示所有猜测过的特质，匹配的绿色，不匹配的灰色）
    if guessed_traits:
        trait_items = []
        for trait in guessed_traits:
            is_match = (trait in answer_char['traits'].split('·') if answer_char['traits'] else False)
            trait_items.append({"value": trait, "match": is_match})
        summary.append({"type": "tags", "attr": "特质", "items": trait_items})
    
    # 已确认的其他属性
    if confirmed_dynasty:
        summary.append({"type": "text", "content": f"朝代：{confirmed_dynasty}"})
    
    if confirmed_province:
        summary.append({"type": "text", "content": f"出生地：{confirmed_province}省"})
    
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
