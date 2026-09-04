import sys
sys.path.append('.')

from watermargin_data import WATERMARGIN

# 重新定义战役参与人员（根据用户提供的详细名单）
battle_participants = {
    '智取生辰纲': ['晁盖', '吴用', '公孙胜', '刘唐', '阮小二', '阮小五', '阮小七', '白胜'],
    '风雪山神庙': ['林冲'],
    '攻打东昌府': ['张清', '龚旺', '丁得孙', '卢俊义', '徐宁', '燕顺', '韩滔', '彭玘', '宣赞', '呼延灼', '刘唐', '杨志', '朱仝', '雷横', '关胜', '董平', '索超', '郝思文', '燕青', '公孙胜'],
    '火并王伦': ['晁盖', '吴用', '公孙胜', '刘唐', '阮小二', '阮小五', '阮小七', '林冲', '杜迁', '宋万', '朱贵'],
    '江州劫法场': ['宋江', '戴宗', '花荣', '黄信', '吕方', '郭盛', '燕顺', '刘唐', '杜迁', '宋万', '朱贵', '王英', '郑天寿', '石勇', '阮小二', '阮小五', '阮小七', '白胜', '李俊', '张横', '张顺', '穆弘', '穆春', '李立', '薛永', '童威', '童猛', '李逵'],
    '三打祝家庄': ['宋江', '花荣', '李俊', '穆弘', '李逵', '杨雄', '石秀', '黄信', '欧鹏', '杨林', '林冲', '秦明', '戴宗', '张横', '张顺', '马麟', '邓飞', '王英', '白胜', '吴用', '阮小二', '阮小五', '阮小七', '吕方', '郭盛', '孙立', '解珍', '解宝', '邹渊', '邹润', '孙新', '顾大嫂', '乐和', '扈三娘', '时迁', '裴宣', '萧让', '侯健', '金大坚'],
    '曾头市之战': ['林冲', '呼延灼', '徐宁', '穆弘', '刘唐', '张横', '阮小二', '阮小五', '阮小七', '杨雄', '石秀', '孙立', '黄信', '杜迁', '宋万', '燕顺', '邓飞', '欧鹏', '杨林', '白胜', '秦明', '花荣', '马麟', '鲁智深', '武松', '孔明', '孔亮', '杨志', '史进', '杨春', '陈达', '朱仝', '雷横', '邹渊', '邹润', '宋江', '吴用', '公孙胜', '吕方', '郭盛', '解珍', '解宝', '戴宗', '时迁', '李逵', '樊瑞', '项充', '李衮', '卢俊义', '燕青', '关胜', '徐宁', '段景住', '郁保四'],
    '征方腊': ['宋江', '卢俊义', '吴用', '公孙胜', '关胜', '林冲', '秦明', '呼延灼', '花荣', '柴进', '李应', '朱仝', '鲁智深', '武松', '董平', '张清', '杨志', '徐宁', '索超', '戴宗', '刘唐', '李逵', '史进', '穆弘', '雷横', '李俊', '阮小二', '张横', '张顺', '阮小五', '阮小七', '杨雄', '石秀', '解珍', '解宝', '燕青', '朱武', '黄信', '孙立', '宣赞', '郝思文', '韩滔', '彭玘', '单廷珪', '魏定国', '萧让', '裴宣', '欧鹏', '邓飞', '燕顺', '杨林', '凌振', '蒋敬', '吕方', '郭盛', '安道全', '皇甫端', '王英', '扈三娘', '鲍旭', '樊瑞', '孔明', '孔亮', '项充', '李衮', '金大坚', '马麟', '童威', '童猛', '孟康', '侯健', '陈达', '杨春', '郑天寿', '陶宗旺', '龚旺', '丁得孙', '穆春', '曹正', '宋万', '杜迁', '薛永', '施恩', '李忠', '周通', '汤隆', '杜兴', '邹渊', '邹润', '朱贵', '朱富', '蔡福', '蔡庆', '李立', '李云', '焦挺', '石勇', '孙新', '顾大嫂', '张青', '孙二娘', '王定六', '郁保四', '白胜', '时迁', '段景住', '宋清', '乐和']
}

# 战役优先级
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

# 为每个角色分配战役（按优先级）
for c in WATERMARGIN:
    full_name = c['surname'] + c['name']
    assigned = False
    
    for battle in battle_priority:
        if full_name in battle_participants[battle]:
            c['battle'] = battle
            assigned = True
            break
    
    if not assigned:
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

# 统计战役分布
battle_stats = {}
for c in WATERMARGIN:
    battle = c['battle']
    if battle not in battle_stats:
        battle_stats[battle] = 0
    battle_stats[battle] += 1

print('\nBattle distribution:')
for battle in battle_priority:
    count = battle_stats.get(battle, 0)
    print(f'  {battle}: {count}')
print(f'  无: {battle_stats.get("无", 0)}')
