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

stem_order_templates = read_stem_order('correct_stem_order.txt')

with open('lexemes_order_test.txt', 'w', encoding = 'utf-8') as out_file:
    with open('missing_templates', 'w', encoding='utf-8') as err_file:
        for l in lexemes:
            print(l)
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
            if 'stamm:' in l:
                stamm = re.search('stamm: ([^\r\n]+)', l).group(1)
            trans_de = ''
            if 'trans_de:' in l:
                trans_de = re.search('trans_de: *([^\r\n]*)', l).group(1)
            trans_en = ''
            if 'trans_en:' in l:
                trans_en = re.search('trans_en: *([^\r\n]*)', l).group(1)

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




