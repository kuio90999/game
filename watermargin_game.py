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
    
    # 姓名（合起来显示）
    guess_name = guess['surname'] + guess['name']
    hints.append({"attr": "姓名", "value": guess_name, "status": ""})
    
    # 绰号
    hints.append({"attr": "绰号", "value": guess['nickname'], "status": ""})
    
    # 排名
    if guess['star_rank'] == answer['star_rank']:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": ""})
    elif guess['star_rank'] < answer['star_rank']:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": "比该人物更低"})
    else:
        hints.append({"attr": "排名", "value": str(guess['star_rank']), "status": "比该人物更高"})
    
    # 星位
    hints.append({"attr": "星位", "value": guess['star_type'], "status": ""})
    
    return hints
