def unwrapper(file_name: str):
    with open(f'generators/models/svg/{file_name}.svg', 'r', encoding='utf-8') as file:
        svg = file.readlines()
    
    if '<!-- TEMPLATE -->\n' in svg: svg.remove('<!-- TEMPLATE -->\n')
    else: svg = svg[1:-1]

    return ''.join(svg)