import re


def shorten_stem(m):
    stemsOut = ''
    usedStems = set()
    stems = m.group(1).split('|')
    for stem in stems:
        stemOut = ''
        for stemVar in stem.split('//'):
            oldStemVar = stemVar
            if stemVar.endswith(('a.', 'ə.', 'i.', 'ь.')) and stemVar[:-2] + '.' not in usedStems:
                stemVar += '//' + stemVar[:-2] + '.'
            usedStems.add(oldStemVar)
            usedStems.add(oldStemVar[:-2] + '.')
            if len(stemOut) > 0:
                stemOut += '//'
            stemOut += stemVar
        if len(stemsOut) > 0:
            stemsOut += '|'
        stemsOut += stemOut
    return 'stem: ' + stemsOut


def add_reduplicated_stem(m):
    stems = m.group(1)
    stemsNew = ''
    for stem in stems.split('|'):
        stemNew = re.sub('(.+)([^.<>\r\n])\\.$', '\\1\\2\\2.', stem)
        stemsNew += '|' + stemNew
    return 'stem: ' + stems + stemsNew

def make_lexeme(lex, stem, gramm ,root, paradigm, trans_de, trans_en, stamm):
    return '-lexeme\n' \
           ' lex: ' + lex + '\n' \
           ' stem: ' + stem + '\n' \
           ' gramm: ' + gramm + '\n' \
           ' root: ' + root + '\n' \
           ' stamm: ' + stamm + '\n' \
           ' paradigm: V_' + paradigm + '\n' \
           ' trans_de: ' + trans_de + '\n' \
           ' trans_en: ' + trans_en + '\n'


def read_patterns(root, paradigm):
    with open('derived_patterns.txt', 'r', encoding='utf-8') as patterns_file:
        patterns = {}
        for line in patterns_file:
            patterns[line.split()[0]] = line.split()[1:]
        return patterns


def generate_derivations(lex, stem, gramm, root, paradigm, trans_de, trans_en, existing_lemmata):
    clean_stem = stem.replace('.', '')
    paradigm_label = re.search('^([IQ]+)_*(.*)', paradigm)
    paradigm_base = paradigm_label.group(1)
    paradigm_deviation = paradigm_label.group(2)
    if paradigm_base == 'I':
        paradigm_new = 'III'
        stamm = 'III'
        if paradigm_deviation:
            paradigm_new += '_' + paradigm_deviation
        
        patterns = read_patterns(root, paradigm_new)
        lex_pattern = patterns[paradigm_new][0]
        stem_pattern = patterns[paradigm_new][1]

        new_lex = re.sub('C[1-3]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2]}[x.group(0)], lex_pattern)
        new_stem = re.sub('C[1-3]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2]}[x.group(0)], stem_pattern)

        if new_lex not in existing_lemmata:
            trans_en_new = trans_en + ' (III)'
            trans_de_new = trans_de + ' (III)'

            yield make_lexeme(new_lex, new_stem, gramm, root, paradigm_new, trans_de_new, trans_en_new, stamm)

        paradigm_new = 'Ip'
        stamm = 'Ip'
        if paradigm_deviation:
            paradigm_new += '_' + paradigm_deviation
        
        patterns = read_patterns(root, paradigm_new)
        lex_pattern = patterns[paradigm_new][0]
        stem_pattern = patterns[paradigm_new][1]

        new_lex = re.sub('C[1-3]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2]}[x.group(0)], lex_pattern)
        new_stem = re.sub('C[1-3]', lambda x: {'C1': root[0], 'C2': root[1], 'C3': root[2]}[x.group(0)], stem_pattern)

        if new_lex not in existing_lemmata:
            trans_en_new = trans_en + ' (Ip)'
            trans_de_new = trans_de + ' (Ip)'
            yield make_lexeme(new_lex, new_stem, gramm, root, paradigm_new, trans_de_new, trans_en_new, stamm)


with open('lexemes-V.txt', 'r', encoding='utf-8-sig') as input_file:
    text = input_file.read()
    lexemes = re.findall('-lexeme\n(?: [^\r\n]+\n)+', text, flags=re.DOTALL)
    lemmata = set()
    for l in lexemes:
        m = re.search('lex: *([^\r\n]+)', l)
        if m is None:
            continue
        for lex in m.group(1).split('/'):
            lemmata.add(lex)

with open('lexemes-V-auto_derivations.txt', 'w', encoding='utf-8') as output_file:
    for l in lexemes:
        if re.search('gramm: (?:V).*?paradigm: V_', l, flags=re.DOTALL) is not None:
            if 'stem:' not in l:
                continue
            lex = re.search('lex: ([^\r\n]+)', l).group(1)
            stem = re.search('stem: ([^\r\n/|]+)', l).group(1)
            gramm = re.search('gramm: ([^\r\n]+)', l).group(1)
            paradigm = re.search('paradigm: V_([^\r\n]*)', l).group(1)
            root = ''
            if 'root' in l:
                root = re.search('root: *([^\r\n]+)', l).group(1)
            trans_en = ''
            if 'trans_en:' in l:
                trans_en = re.search('trans_en: *([^\r\n]*)', l).group(1)
            trans_de = ''
            if 'trans_de:' in l:
                trans_de = re.search('trans_de: *([^\r\n]*)', l).group(1)
        
            if paradigm == 'I' or paradigm.startswith('I_'):
                for new_lemma in generate_derivations(lex, stem, gramm, root, paradigm, trans_de, trans_en, lemmata):
                    output_file.write(new_lemma + '\n')
