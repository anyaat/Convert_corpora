import os
import codecs
from bs4 import BeautifulSoup
from tag2positional import ruscorpora2positional

n = 0
pathIn = './school/texts'


def get_meta_school(file_name):
    stops = ['tagging', 'issue', 'rubric', 'page', 'not_place', 'quality', 'place', 'division', 'responsible']
    meta_all = ['header', 'author', 'sex', 'created', 'docid', 'words', 'sphere', 'genre_fi', 'type', 'style', \
               'audience_age', 'audience_level', 'audience_size', 'source', 'publication', 'publ_year', 'medium', \
               'subcorpus', 'chronotop', 'birthday', 'topic', 'publisher']
    metas = dict.fromkeys(meta_all, 'нет данных')
    with codecs.open(file_name, encoding='cp1251') as f:
        soup = BeautifulSoup(f.read(), 'lxml').head
    for item in soup.find_all('meta'):
        name = item.get('name').replace('title', 'header').replace('dаte', 'created')
        if name not in stops:
            content = item.get('content')
            if content:
                if metas[name] != 'нет данных':
                    metas[name] += '; ' + content
                else:
                    metas[name] = content
    return metas


with open('./school.txt', 'w', encoding='utf-8') as file:
    for root, dirs, files in os.walk(pathIn):
        for fileIn in files:
            n += 1
            if n % 25 == 0:
                print(n)
            file_xhtml = os.path.join(root, fileIn)
            metas = get_meta_school(file_xhtml)
            metas['docid'] = str(n)
            first_row = '<doc'
            for meta in metas:
                first_row += ' ' + meta + '="' + metas[meta] + '"'
            first_row += '>\n'
            file.write(first_row)

            with codecs.open(file_xhtml, encoding='cp1251') as f:
                for line in f:
                    if '<se>' in line:
                        file.write('<s>\n')
                        if not '<w>' in line:
                            string = BeautifulSoup(line, 'lxml').get_text().strip(' \n')
                            for i in range(len(string)):
                                    punc = string[i]
                                    if i >= 1 and punc == '-' and string[i-1] == '-':
                                        continue
                                    if punc in ',.;:»!?)]}':
                                        file.write('<g/>\n' + punc + '\t' + punc + '\tPUNC\n')
                                    elif punc in '«({[':
                                        file.write(punc + '\t' + punc + '\tPUNC\n' + '<g/>\n')
                                    elif not punc == ' ' and not punc == '' and not punc == '\r':
                                        file.write(punc + '\t' + punc + '\tPUNC\n')                                      
                    if '<w>' in line:
                        soup = BeautifulSoup(line, 'lxml')
                        try:
                            lemma = soup.ana.get('lex')
                        except:
                            print(file_xhtml, n, line)
                        tag = ruscorpora2positional(soup.ana.get('gr'))
                        token = soup.w.get_text()
                        string = soup.get_text()
                        if string != token:
                            string = string.replace(token, 'M')
                            i = string.index('M')
                            left = string[:i].strip()
                            right = string[i+1:].strip(' \n')
                            if left:
                                for i in range(len(left)):
                                    punc = left[i]
                                    if i >= 1 and punc == '-' and left[i-1] == '-':
                                        continue
                                    if punc in ',.;:»!?)]}':
                                        file.write('<g/>\n' + punc + '\t' + punc + '\tPUNC\n')
                                    elif punc in '«({[':
                                        file.write(punc + '\t' + punc + '\tPUNC\n' + '<g/>\n')
                                    elif not punc == ' ' and not punc == '' and not punc == '\r':
                                        file.write(punc + '\t' + punc + '\tPUNC\n')   
                            try:
                                file.write(token.replace('`', '') + '\t' + lemma + '\t' + tag + '\n')
                            except:
                                print(file_xhtml, n, line)
                            if right:
                                for i in range(len(right)):
                                    punc = right[i]
                                    if i >= 1 and punc == '-' and right[i-1] == '-':
                                        continue
                                    if punc in ',.;:»!?)]}':
                                        file.write('<g/>\n' + punc + '\t' + punc + '\tPUNC\n')
                                    elif punc in '«({[':
                                        file.write(punc + '\t' + punc + '\tPUNC\n' + '<g/>\n')
                                    elif not punc == ' ' and not punc == '' and not punc == '\r':
                                        file.write(punc + '\t' + punc + '\tPUNC\n') 
                        else:
                            file.write(token.replace('`', '') + '\t' + lemma + '\t' + tag + '\n')
                    if '</se>' in line:
                        file.write('</s>\n')
                        
            file.write('</doc>\n')
print(n)