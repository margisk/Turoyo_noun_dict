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


def make_lexeme(lex, stem, gramm, root, paradigm, transDe, transEn):
    return '-lexeme\n' \
           ' lex: ' + lex + '\n' \
           ' stem: ' + stem + '\n' \
           ' gramm: ' + gramm + '\n' \
           ' root: ' + root + '\n' \
           ' paradigm: V_' + paradigm + '\n' \
           ' trans_de: ' + transDe + '\n' \
           ' trans_en: ' + transEn + '\n'


def generate_derivations(lex, stem, gramm, root, paradigm,
                         transDe, transEn, existingLemmata):
    stem = stem.replace('.', '')
    mPara = re.search('^([IQ]+)_*(.*)', paradigm)
    paraBase = mPara.group(1)
    paraDeviation = mPara.group(2)
    if paraBase == 'I':
        paradigmNew = 'III'
        if len(paraDeviation) > 0:
            paradigmNew += '_' + paraDeviation
        if len(stem) == 3:
            # Lemma consists of two parts: prs and pst
            # Present form
            if paraDeviation == '3y':
                lexPrs = 'ma' + stem[0] + 'e'
            elif paraDeviation == '3w':
                lexPrs = 'ma' + stem[:2] + 'u'
            elif paraDeviation in ('2y', '2y_3l', '2y_3r', '2y_3n'):
                lexPrs = 'ma' + stem[0] + 'ə' + stem[2]
            elif paraDeviation == '2y_3w':
                lexPrs = 'ma' + stem[0] + 'u'
            else:
                lexPrs = 'ma' + stem[:2] + 'ə' + stem[2]

            if paraDeviation == '2y':
                lexPst = 'ma' + stem[0] + 'ə' + stem[2] + 'le'
            elif paraDeviation in ('3y', '3l'):
                lexPst = 'ma' + stem[:2] + 'ele'
            elif paraDeviation in ('3r', '3n'):
                lexPst = 'ma' + stem[:2] + 'alle'
            elif paraDeviation == '3l':
                lexPst = 'ma' + stem[:2] + 'ele'
            elif paraDeviation == '2y_3l':
                lexPst = 'ma' + stem[0] + 'ile'
            elif paraDeviation in ('2y_3r', '2y_3n'):
                lexPst = 'ma' + stem[0] + 'əlle'
            elif paraDeviation == '2y_3w':
                lexPst = 'ma' + stem[0] + 'ule'
            else:
                lexPst = 'ma' + stem[:2] + 'a' + stem[2] + 'le'

            lexNew = lexPrs + '/' + lexPst
            if lexNew not in existingLemmata:
                stemNew = '.' + '.'.join(stem) + '.|.' + stem[0] + '.' + stem[1] + '.' + stem[2] * 2 + '.'
                transEnNew = transEn + ' (III)'
                transDeNew = transDe + ' (III)'
                yield make_lexeme(lexNew, stemNew, gramm, root, paradigmNew,
                                  transDeNew, transEnNew)

        paradigmNew = 'Ip'
        if len(paraDeviation) > 0:
            paradigmNew += '_' + paraDeviation
        if len(stem) == 3:
            if paraDeviation == '2y':
                lexPrs = 'mə' + stem[0] + 'ə' + stem[2]
            elif paraDeviation == '3w':
                lexPrs = 'mə' + stem[:2] + 'u'
            elif paraDeviation == '3y':
                lexPrs = 'mə' + stem[:2] + 'e'
            else:
                lexPrs = 'mə' + stem[:2] + 'ə' + stem[2]

            if paraDeviation == '2y':
                lexPst = stem[0] + 'i' + stem[2]
            elif paraDeviation == '3y':
                lexPst = stem[:2] + 'e'
            else:
                lexPst = stem[:2] + 'i' + stem[2]
            lexNew = lexPrs + '/' + lexPst
            if lexNew not in existingLemmata:
                stemNew = '.' + '.'.join(stem) + '.|.' + stem[0] + '.' + stem[1] + '.' + stem[2] * 2 + '.'
                transEnNew = transEn + ' (Ip)'
                transDeNew = transDe + ' (Ip)'
                yield make_lexeme(lexNew, stemNew, gramm, root, paradigmNew,
                                  transDeNew, transEnNew)


fIn = open('lexemes-V.txt', 'r', encoding='utf-8-sig')
text = fIn.read()
fIn.close()
lexemes = re.findall('-lexeme\n(?: [^\r\n]+\n)+', text, flags=re.DOTALL)
lemmata = set()
for l in lexemes:
    m = re.search('lex: *([^\r\n]+)', l)
    if m is None:
        continue
    for lex in m.group(1).split('/'):
        lemmata.add(lex)


fOut = open('lexemes-V-auto_derivations.txt', 'w', encoding='utf-8')
for l in lexemes:
    if re.search('gramm: (?:V).*?paradigm: V_', l, flags=re.DOTALL) is not None:
        if 'stem:' not in l:
            continue
        paradigm = re.search('paradigm: V_([^\r\n]*)', l).group(1)
        stem = re.search('stem: ([^\r\n/|]+)', l).group(1)
        lex = re.search('lex: ([^\r\n]+)', l).group(1)
        transEn = ''
        if 'trans_en:' in l:
            transEn = re.search('trans_en: *([^\r\n]*)', l).group(1)
        transDe = ''
        if 'trans_de:' in l:
            transDe = re.search('trans_de: *([^\r\n]*)', l).group(1)
        gramm = re.search('gramm: ([^\r\n]+)', l).group(1)
        root = ''
        if 'root' in l:
            root = re.search('root: *([^\r\n]*)', l).group(1)
        if paradigm == 'I' or paradigm.startswith('I_'):
            for newLemma in generate_derivations(lex, stem, gramm, root, paradigm,
                                                 transDe, transEn, lemmata):
                fOut.write(newLemma + '\n')
fOut.close()
