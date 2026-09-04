import sys
sys.path.append('.')

from watermargin_data import WATERMARGIN

# 修改武器和擅长
weapon_specialty_map = {
    # 原武器 -> (新武器, 新擅长)
    '刀': ('无', '无'),
    '枪': ('无', '无'),
    '剑': ('无', '无'),
    '双刀': ('双刀', '刀法'),
    '双枪': ('双枪', '枪法'),
    '青龙偃月刀': ('青龙偃月刀', '刀法'),
    '狼牙棒': ('狼牙棒', '棒法'),
    '双鞭': ('双鞭', '鞭法'),
    '弓箭': ('弓箭', '射击'),
    '飞刀': ('飞刀', '飞刀'),
    '禅杖': ('禅杖', '杖法'),
    '双斧': ('双斧', '斧法'),
    '大斧': ('大斧', '斧法'),
    '钩镰枪': ('钩镰枪', '枪法'),
    '飞石': ('飞石', '射击'),
    '方天画戟': ('方天画戟', '戟法'),
    '铁链': ('铁链', '链法'),
    '阔剑': ('阔剑', '剑法'),
    '火炮': ('火炮', '火炮'),
    '弩': ('弩', '射击'),
    '标枪': ('标枪', '标枪'),
    '三尖两刃刀': ('三尖两刃刀', '刀法'),
    '扇子': ('扇子', '管家'),
}

# 特殊情况的擅长技能
specialty_override = {
    '林冲': '枪棒',  # 林冲擅长枪棒
    '董平': '双枪',  # 董平擅长双枪
    '杨志': '刀法',  # 杨志擅长刀法，但有其他特长
    '徐宁': '钩镰枪',  # 徐宁擅长钩镰枪
    '史进': '枪棒',  # 史进擅长枪棒
    '穆弘': '无',  # 穆弘没有特别的特长
    '雷横': '步战',  # 雷横擅长步战
    '朱仝': '刀法',  # 朱仝擅长刀法
    '黄信': '刀法',  # 黄信擅长刀法
    '孙立': '枪棒',  # 孙立擅长枪棒
    '宣赞': '刀法',  # 宣赞擅长刀法
    '郝思文': '枪法',  # 郝思文擅长枪法
    '韩滔': '枪法',  # 韩滔擅长枪法
    '彭玘': '刀法',  # 彭玘擅长刀法
    '单廷珪': '枪法',  # 单廷珪擅长枪法
    '魏定国': '刀法',  # 魏定国擅长刀法
    '欧鹏': '枪法',  # 欧鹏擅长枪法
    '杨林': '枪法',  # 杨林擅长枪法
    '王英': '枪法',  # 王英擅长枪法
    '扈三娘': '双刀',  # 扈三娘擅长双刀
    '鲍旭': '阔剑',  # 鲍旭擅长阔剑
    '孔明': '枪法',  # 孔明擅长枪法
    '孔亮': '枪法',  # 孔亮擅长枪法
    '陈达': '枪法',  # 陈达擅长枪法
    '杨春': '枪法',  # 杨春擅长枪法
    '郑天寿': '枪法',  # 郑天寿擅长枪法
    '龚旺': '枪法',  # 龚旺擅长枪法
    '丁得孙': '枪法',  # 丁得孙擅长枪法
    '穆春': '枪法',  # 穆春擅长枪法
    '宋万': '枪法',  # 宋万擅长枪法
    '杜迁': '枪法',  # 杜迁擅长枪法
    '薛永': '枪法',  # 薛永擅长枪法
    '施恩': '枪法',  # 施恩擅长枪法
    '李忠': '枪法',  # 李忠擅长枪法
    '周通': '枪法',  # 周通擅长枪法
    '汤隆': '枪法',  # 汤隆擅长枪法
    '邹渊': '枪法',  # 邹渊擅长枪法
    '邹润': '枪法',  # 邹润擅长枪法
    '焦挺': '枪法',  # 焦挺擅长枪法
    '石勇': '刀法',  # 石勇擅长刀法
    '孙新': '枪法',  # 孙新擅长枪法
    '郁保四': '枪法',  # 郁保四擅长枪法
    '马麟': '双刀',  # 马麟擅长双刀
    '童威': '水性',  # 童威擅长水性
    '童猛': '水性',  # 童猛擅长水性
    '曹正': '厨艺',  # 曹正擅长厨艺
    '朱贵': '情报',  # 朱贵擅长情报
    '顾大嫂': '经商',  # 顾大嫂擅长经商
    '张青': '种菜',  # 张青擅长种菜
    '孙二娘': '开店',  # 孙二娘擅长开店
}

# 参与战役映射（按优先级）
battle_priority = [
    '智取生辰纲',
    '风雪山神庙',
    '攻打东昌府',
    '火并王伦',
    '江州劫法场',
    '三打祝家庄',
    '曾头市之战',
    '征方腊',
]

# 人物参与战役映射
battle_map = {
    '宋江': '智取生辰纲',
    '吴用': '智取生辰纲',
    '公孙胜': '智取生辰纲',
    '刘唐': '智取生辰纲',
    '阮小二': '智取生辰纲',
    '阮小五': '智取生辰纲',
    '阮小七': '智取生辰纲',
    '白胜': '智取生辰纲',
    '林冲': '风雪山神庙',
    '鲁智深': '攻打东昌府',
    '宋万': '火并王伦',
    '杜迁': '火并王伦',
    '朱贵': '火并王伦',
    '柴进': '江州劫法场',
    '李逵': '江州劫法场',
    '花荣': '三打祝家庄',
    '秦明': '三打祝家庄',
    '黄信': '三打祝家庄',
    '孙立': '三打祝家庄',
    '孙新': '三打祝家庄',
    '顾大嫂': '三打祝家庄',
    '解珍': '曾头市之战',
    '解宝': '曾头市之战',
    '卢俊义': '征方腊',
    '关胜': '征方腊',
    '呼延灼': '征方腊',
    '董平': '征方腊',
    '张清': '征方腊',
    '杨志': '征方腊',
    '徐宁': '征方腊',
    '索超': '征方腊',
    '戴宗': '征方腊',
    '史进': '征方腊',
    '穆弘': '征方腊',
    '雷横': '征方腊',
    '李俊': '征方腊',
    '张横': '征方腊',
    '张顺': '征方腊',
    '杨雄': '征方腊',
    '石秀': '征方腊',
    '燕青': '征方腊',
    '朱武': '征方腊',
    '宣赞': '征方腊',
    '郝思文': '征方腊',
    '韩滔': '征方腊',
    '彭玘': '征方腊',
    '单廷珪': '征方腊',
    '魏定国': '征方腊',
    '萧让': '征方腊',
    '裴宣': '征方腊',
    '欧鹏': '征方腊',
    '邓飞': '征方腊',
    '燕顺': '征方腊',
    '杨林': '征方腊',
    '凌振': '征方腊',
    '蒋敬': '征方腊',
    '吕方': '征方腊',
    '郭盛': '征方廉',
    '安道全': '征方腊',
    '皇甫端': '征方腊',
    '王英': '征方腊',
    '扈三娘': '征方腊',
    '鲍旭': '征方腊',
    '樊瑞': '征方腊',
    '孔明': '征方腊',
    '孔亮': '征方腊',
    '项充': '征方腊',
    '李衮': '征方腊',
    '金大坚': '征方腊',
    '马麟': '征方腊',
    '童威': '征方腊',
    '童猛': '征方腊',
    '孟康': '征方腊',
    '侯健': '征方腊',
    '陈达': '征方腊',
    '杨春': '征方腊',
    '郑天寿': '征方腊',
    '陶宗旺': '征方腊',
    '龚旺': '征方腊',
    '丁得孙': '征方腊',
    '穆春': '征方腊',
    '曹正': '征方腊',
    '薛永': '征方腊',
    '施恩': '征方腊',
    '李忠': '征方腊',
    '周通': '征方腊',
    '汤隆': '征方腊',
    '杜兴': '征方腊',
    '邹渊': '征方腊',
    '邹润': '征方腊',
    '朱富': '征方腊',
    '蔡福': '征方腊',
    '蔡庆': '征方腊',
    '李立': '征方腊',
    '李云': '征方腊',
    '焦挺': '征方腊',
    '石勇': '征方腊',
    '张青': '征方腊',
    '孙二娘': '征方腊',
    '王定六': '征方腊',
    '郁保四': '征方腊',
    '时迁': '征方腊',
    '段景住': '征方腊',
    '宋清': '征方腊',
    '乐和': '征方腊',
}

# 更新数据
for c in WATERMARGIN:
    name = c['surname'] + c['name']
    
    # 修改武器
    old_weapon = c['weapon']
    if old_weapon in weapon_specialty_map:
        new_weapon, new_specialty = weapon_specialty_map[old_weapon]
        c['weapon'] = new_weapon
        # 只有当没有特殊覆盖时才修改擅长
        if name not in specialty_override:
            c['specialty'] = new_specialty
    
    # 应用特殊覆盖
    if name in specialty_override:
        c['specialty'] = specialty_override[name]
    
    # 添加参与战役
    if name in battle_map:
        c['battle'] = battle_map[name]
    else:
        c['battle'] = '无'

# 保存到文件
with open('watermargin_data.py', 'w', encoding='utf-8') as f:
    f.write('WATERMARGIN = [\n')
    for c in WATERMARGIN:
        surname = c['surname']
        name = c['name']
        courtesy_name = c['courtesy_name']
        nickname = c['nickname']
        star_rank = c['star_rank']
        star_type = c['star_type']
        birth_year = c['birth_year']
        death_year = c['death_year']
        birthplace = c['birthplace']
        identity = c['identity']
        pre_mountains = c['pre_mountains']
        weapon = c['weapon']
        specialty = c['specialty']
        traits = c['traits']
        ending = c['ending']
        battle = c['battle']
        
        line = f'    {{"surname": "{surname}", "name": "{name}", "courtesy_name": "{courtesy_name}", "nickname": "{nickname}", "star_rank": {star_rank}, "star_type": "{star_type}", "birth_year": {birth_year}, "death_year": {death_year}, "birthplace": "{birthplace}", "identity": "{identity}", "pre_mountains": "{pre_mountains}", "weapon": "{weapon}", "specialty": "{specialty}", "traits": "{traits}", "ending": "{ending}", "battle": "{battle}"}},'
        f.write(line + '\n')
    f.write(']\n')

print('Saved watermargin_data.py')
print('Total:', len(WATERMARGIN))

# 统计修改
weapon_changes = sum(1 for c in WATERMARGIN if c['weapon'] == '无')
specialty_changes = sum(1 for c in WATERMARGIN if c['specialty'] == '无')
battle_count = sum(1 for c in WATERMARGIN if c['battle'] != '无')

print(f'Weapon changes: {weapon_changes} characters now have "无" as weapon')
print(f'Specialty changes: {specialty_changes} characters now have "无" as specialty')
print(f'Battle assignments: {battle_count} characters have battle assignments')
