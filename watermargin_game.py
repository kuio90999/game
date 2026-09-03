from database import get_connection

def get_all_watermargin():
    """获取所有水浒人物列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM watermargin ORDER BY star_rank')
    chars = cursor.fetchall()
    
    conn.close()
    return [dict(c) for c in chars]

def get_watermargin_by_name(name):
    """根据名字查找水浒人物"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 先尝试精确匹配姓+名
    cursor.execute('SELECT * FROM watermargin WHERE surname || name = ?', (name,))
    char = cursor.fetchone()
    
    if not char:
        # 再尝试单独匹配名
        cursor.execute('SELECT * FROM watermargin WHERE name = ?', (name,))
        char = cursor.fetchone()
    
    if not char:
        # 尝试匹配绰号
        cursor.execute('SELECT * FROM watermargin WHERE nickname = ?', (name,))
        char = cursor.fetchone()
    
    conn.close()
    return char

def get_watermargin_by_id(char_id):
    """根据ID查找水浒人物"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM watermargin WHERE id = ?', (char_id,))
    char = cursor.fetchone()
    
    conn.close()
    return char

def compare_watermargin(guess, answer):
    """比较两个水浒人物，返回提示"""
    hints = []
    
    # 姓
    if guess['surname'] == answer['surname']:
        hints.append({"attr": "姓", "value": guess['surname'], "status": "一致"})
    else:
        hints.append({"attr": "姓", "value": guess['surname'], "status": "不一致"})
    
    # 名
    if guess['name'] == answer['name']:
        hints.append({"attr": "名", "value": guess['name'], "status": "一致"})
    else:
        hints.append({"attr": "名", "value": guess['name'], "status": "不一致"})
    
    # 绰号
    if guess['nickname'] == answer['nickname']:
        hints.append({"attr": "绰号", "value": guess['nickname'], "status": "一致"})
    else:
        # 检查是否有相同的字
        if guess['nickname'] and answer['nickname']:
            common_chars = set(guess['nickname']) & set(answer['nickname'])
            if common_chars:
                hints.append({"attr": "绰号", "value": guess['nickname'], "status": f"有相同的字：{'、'.join(common_chars)}"})
            else:
                hints.append({"attr": "绰号", "value": guess['nickname'], "status": "不一致"})
        else:
            hints.append({"attr": "绰号", "value": guess['nickname'], "status": "不一致"})
    
    # 星座排名
    if guess['star_rank'] == answer['star_rank']:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": "一致"})
    elif guess['star_rank'] < answer['star_rank']:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": "比该人物更低"})
    else:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": "比该人物更高"})
    
    # 天罡/地煞
    if guess['star_type'] == answer['star_type']:
        hints.append({"attr": "星位", "value": guess['star_type'], "status": "一致"})
    else:
        hints.append({"attr": "星位", "value": guess['star_type'], "status": "不一致"})
    
    # 身份
    if guess['identity'] == answer['identity']:
        hints.append({"attr": "身份", "value": guess['identity'], "status": "一致"})
    else:
        hints.append({"attr": "身份", "value": guess['identity'], "status": "不一致"})
    
    # 上山前身份
    if guess['pre_mountains'] == answer['pre_mountains']:
        hints.append({"attr": "上山前身份", "value": guess['pre_mountains'], "status": "一致"})
    else:
        hints.append({"attr": "上山前身份", "value": guess['pre_mountains'], "status": "不一致"})
    
    # 擅长
    if guess['specialty'] == answer['specialty']:
        hints.append({"attr": "擅长", "value": guess['specialty'], "status": "一致"})
    else:
        hints.append({"attr": "擅长", "value": guess['specialty'], "status": "不一致"})
    
    # 特质
    if guess['traits'] and answer['traits']:
        guess_traits = set(guess['traits'].split('·'))
        answer_traits = set(answer['traits'].split('·'))
        common_traits = guess_traits & answer_traits
        
        if common_traits:
            hints.append({"attr": "特质", "value": guess['traits'], "status": f"相同：{'、'.join(common_traits)}"})
        else:
            hints.append({"attr": "特质", "value": guess['traits'], "status": "无相同"})
    else:
        hints.append({"attr": "特质", "value": guess['traits'] or "无", "status": "不一致"})
    
    # 结局
    if guess['ending'] == answer['ending']:
        hints.append({"attr": "结局", "value": guess['ending'], "status": "一致"})
    else:
        hints.append({"attr": "结局", "value": guess['ending'], "status": "不一致"})
    
    return hints
