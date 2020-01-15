import re
import os

rxDiaPartsStem = re.compile('( stem:)( *[^\r\n]+)')
rxDiaPartsFlex = re.compile('(-flex:)( *[^\r\n]+)')
rxStemVariants = re.compile('[^ |/]+')
rxFlexVariants = re.compile('[^ /]+')


def collect_lemmata():
    lemmata = ''
    lexrules = ''
    for fname in os.listdir('..'):
        if fname.endswith('.txt') and fname.startswith('lexemes'):
            f = open(os.path.join('..', fname), 'r', encoding='utf-8-sig')
            lemmata += f.read() + '\n'
            f.close()
        elif fname.endswith('.txt') and fname.startswith('lexrules'):
            f = open(os.path.join('..', fname), 'r', encoding='utf-8-sig')
            lexrules += f.read() + '\n'
            f.close()
    lemmataSet = set(re.findall('-lexeme\n(?: [^\r\n]*\n)+', lemmata, flags=re.DOTALL))
    # lemmata = '\n'.join(sorted(list(lemmataSet),
    #                            key=lambda l: (re.search('gramm: *([^\r\n]*)', l).group(1), l)))
    lemmata = '\n'.join(sorted(list(lemmataSet)))
    return lemmata, lexrules


def collect_paradigms():
    paradigms = ''
    for fname in os.listdir('../paradigms/'):
        if fname.endswith('.txt') and fname.startswith('paradigms'):
            f = open(os.path.join('../paradigms/', fname), 'r',
                     encoding='utf-8-sig')
            paradigms += f.read() + '\n'
            f.close()
    return paradigms


def main():
    """
    Put all the lemmata to lexemes.txt. Put all the lexical
    rules to lexical_rules.txt. Create separate versions of
    relevant files for diacriticless texts.
    """
    lemmata, lexrules = collect_lemmata()
    paradigms = collect_paradigms()
    fOutLemmata = open('lexemes.txt', 'w', encoding='utf-8')
    fOutLemmata.write(lemmata)
    fOutLemmata.close()
    fOutLemmata = open('../analyzer/lexemes.txt', 'w', encoding='utf-8')
    fOutLemmata.write(lemmata)
    fOutLemmata.close()
    if len(lexrules) > 0:
        fOutLexrules = open('lex_rules.txt', 'w', encoding='utf-8')
        fOutLexrules.write(lexrules)
        fOutLexrules.close()
        fOutLexrules = open('../analyzer/lex_rules.txt', 'w', encoding='utf-8')
        fOutLexrules.write(lexrules)
        fOutLexrules.close()
    fOutParadigms = open('paradigms.txt', 'w', encoding='utf-8')
    fOutParadigms.write(paradigms)
    fOutParadigms.close()
    fOutParadigms = open('../analyzer/paradigms.txt', 'w', encoding='utf-8')
    fOutParadigms.write(paradigms)
    fOutParadigms.close()


if __name__ == '__main__':
    main()
