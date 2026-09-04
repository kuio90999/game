import sys
sys.path.append('.')

from watermargin_data import WATERMARGIN

# 重新分配排名
for i, c in enumerate(WATERMARGIN):
    c['star_rank'] = i + 1

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
        
        line = f'    {{"surname": "{surname}", "name": "{name}", "courtesy_name": "{courtesy_name}", "nickname": "{nickname}", "star_rank": {star_rank}, "star_type": "{star_type}", "birth_year": {birth_year}, "death_year": {death_year}, "birthplace": "{birthplace}", "identity": "{identity}", "pre_mountains": "{pre_mountains}", "weapon": "{weapon}", "specialty": "{specialty}", "traits": "{traits}", "ending": "{ending}"}},'
        f.write(line + '\n')
    f.write(']\n')

print('Saved watermargin_data.py')
print('Total:', len(WATERMARGIN))
