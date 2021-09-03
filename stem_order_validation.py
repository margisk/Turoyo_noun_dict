import re

def read_stem_order(stem_order_file):
    templates_dict = {}
    with open(stem_order_file, 'r', encoding = 'utf-8') as f:
        for template_line in f:
            if template_line:
                template_root = template_line.split()[0]
                template = template_line.split()[1]
                templates_dict[template_root] = template
    return templates_dict

with open('lexemes-V.txt','r',encoding = 'utf-8-sig') as input_file:
    text = input_file.read()
    lexemes = re.findall('-lexeme\n(?: [^\r\n]+\n)+', text, flags=re.DOTALL)

def check_paradigm(root, paradigm):
    """check if the lexemes in the file have the correct paradigm"""
    root_type = ''
    irregular = re.compile('to_(go|play|give|say)')
    if re.match(irregular, paradigm):
        paradigm_base = ''
        paradigm_deviation = ''
    else:
        paradigm_label = re.search('_([VIQX]+)_*(.*)', paradigm)
        paradigm_base = paradigm_label.group(1)
        paradigm_deviation = paradigm_label.group(2)

    #many redundant checks
    if root.endswith('y'):
        if root[1] == 'w':
            root_type = '2w_3y'
        else:
            root_type = '3y'
    elif root.endswith('n'):
        if root[1] == 'w':
            root_type = '2w_3n'
        elif root[1] == 'y':
            root_type = '2y_3n'
        else:
            root_type = '3n'
    elif root.endswith('w'):
        if root[1] == 'y':
            root_type == '2y_3w'
        else:
            root_type = '3w'
    elif root.endswith('r'):
        if root[1] == 'y':
            root_type = '2y_3r'
        elif root[1] == 'w':
            root_type = '2w_3r'
        else:
            root_type = '3r'
    elif root.endswith('l'):
        if root[1] == 'y':
            root_type = '2y_3l'
        elif root[1] == 'w':
            root_type = '2w_3r'
        else:
            root_type = '3l'
    elif root[1] == 'y':
        if root.endswith('w'):
            root_type = '2y_3w'
        elif root.endswith('n'):
            root_type = '2y_3n'
        elif root.endswith('r'):
            root_type = '2y_3r'
        elif root.endswith('l'):
            root_type = '2y_3l'
        else:
            root_type = '2y'
    elif root[1] == 'w':
        if root.endswith('n'):
            root_type = '2w_3n'
        elif root.endswith('r'):
            root_type = '2w_3r'
        elif root.endswith('y'):
            root_type = '2w_3y'
        elif root.endswith('l'):
            root_type = '2w_3l'
        else:
            root_type = '2w'
    elif root[0] == 'y':
        if root.endswith('y'):
            root_type = '1y_3y'
        elif root.endswith('w'):
            root_type = '1y_3w'
        elif root.endswith('n'):
            root_type = '1y_3n'
        elif root.endswith('r'):
            root_type = '1y_3r'
        elif root.endswith('3l') == '1y_3l':
            root_type = '1y_3l'
        else:
            root_type = '1y'

        if root_type != paradigm_deviation:
            print('Expected {0} but got {1} for root {2}.'.format(root_type, paradigm_deviation, root))


stem_order_templates = read_stem_order('correct_stem_order.txt')

with open('lexemes_order_test.txt', 'w', encoding = 'utf-8') as out_file:
    with open('missing_templates', 'w', encoding='utf-8') as err_file:
        for l in lexemes:
            lex = re.search('lex: ([^\r\n]+)', l).group(1)
            paradigm = re.search('paradigm: ((?:V|to)_[^\r\n]*)', l).group(1)
            gramm = re.search('gramm: ([^\r\n]+)', l).group(1)
            stem = ''
            if 'stem:' in l:
                stem = re.search('stem: ([^\r\n/|]+)', l).group(1)
            root = ''
            if 'root:' in l:
                root = re.search('root: *([^\r\n]+)', l).group(1)
            stamm = ''
            stamm_match = re.compile(r'stamm:\s[^\r\n]+')
            if 'stamm:' in l and re.match(stamm_match, l):
                stamm = re.search('stamm: ([^\r\n]+)', l).group(1)
            trans_de = ''
            if 'trans_de:' in l:
                trans_de = re.search('trans_de: *([^\r\n]*)', l).group(1)
            trans_en = ''
            if 'trans_en:' in l:
                trans_en = re.search('trans_en: *([^\r\n]*)', l).group(1)

            check_paradigm(root, paradigm)

            try:
                new_stem_pattern = stem_order_templates[paradigm]
                if len(root) == 3:
                    new_stem = re.sub('C[1-3]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2]}[x.group(0)], new_stem_pattern)
                if len(root) == 4:
                    new_stem = re.sub('C[1-4]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2], 'C4': root[3]}[x.group(0)], new_stem_pattern)
                if len(root) == 5:
                    new_stem = re.sub('C[1-5]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2], 'C4': root[3], 'C5': root[4]}[x.group(0)], new_stem_pattern)
                out_file.write('-lexeme\n' \
                   ' lex: ' + lex + '\n' \
                   ' stem: ' + new_stem + '\n' \
                   ' gramm: ' + gramm + '\n' \
                   ' root: ' + root + '\n' \
                   ' stamm: ' + stamm + '\n' \
                   ' paradigm: ' + paradigm + '\n' \
                   ' trans_de: ' + trans_de + '\n' \
                   ' trans_en: ' + trans_en + '\n' + '\n')
            except KeyError:
                print("No pattern to use was found!")
                err_file.write(paradigm + '\n')




