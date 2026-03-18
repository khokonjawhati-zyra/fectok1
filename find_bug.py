import os

path = r'c:\Users\Admin\shorts\user_panel\lib\main.dart'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_container = False
has_color = False
has_decoration = False
start_line = 0
nest_level = 0

for i, line in enumerate(lines):
    if 'Container(' in line:
        in_container = True
        has_color = False
        has_decoration = False
        start_line = i + 1
        nest_level = 0
    
    if in_container:
        if 'color:' in line:
            has_color = True
        if 'decoration:' in line:
            has_decoration = True
        
        nest_level += line.count('(') - line.count(')')
        
        if nest_level < 0:
            if has_color and has_decoration:
                print(f'Error found at line {start_line}')
            in_container = False
