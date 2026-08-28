import json

# 读取人物数据
with open('characters_export.json', 'r', encoding='utf-8') as f:
    chars = json.load(f)

# 读取RELATIONS数据
with open('relations_backup.py', 'r', encoding='utf-8') as f:
    relations_content = f.read()

# 生成CHARACTERS部分
characters_code = 'CHARACTERS = [\n'
for c in chars:
    courtesy_name = '"' + c['courtesy_name'] + '"' if c['courtesy_name'] else 'None'
    force = '"' + c['force'] + '"' if c['force'] else 'None'
    traits = '"' + c['traits'] + '"' if c['traits'] else 'None'
    
    characters_code += f'    {{"surname": "{c["surname"]}", "name": "{c["name"]}", "courtesy_name": {courtesy_name}, "birth_year": {c["birth_year"]}, "death_year": {c["death_year"]}, "birthplace": "{c["birthplace"]}", "dynasty": "{c["dynasty"]}", "force": {force}, "identity": "{c["identity"]}", "traits": {traits}}},\n'
characters_code += ']\n\n'

# 保存到文件
with open('data_new.py', 'w', encoding='utf-8') as f:
    f.write(characters_code)
    f.write(relations_content)

print('New data.py file created: data_new.py')
