import PyPDF2
import os
import re
import codecs


reg_keywords = re.compile('[kK]ey ?[wW]ords:([a-zA-Z ,;\n\r]+)', flags=re.M)
reg_author = re.compile('(.+?)_')
reg_key_sub = re.compile('[;\n\r]+')


'''
class Article:
    def __init__(self, path):
        self.path_pdf = path
        self.path_txt = path.replace('journals/pdf', 'journals/txt')
        self.text = get_text(path)
        self.journal, self.year, self.issue, self.name = path.\
            replace('journals/pdf', '').split('/')
        self.keywords = get_keywords(self.text)
'''


def get_text(path):
    text = ''
    pdfFileObj = open(path, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    for page in range(0, pdfReader.numPages):
        pageObj = pdfReader.getPage(page)
        text += pageObj.extractText()
    return text


def get_keywords(path):
    with codecs.open(path, 'r', encoding='utf-8') as f:
        text = f.read()
        keywords = ''
        m = reg_keywords.search(text)
        if m:
            keywords = m.group(1).strip()
    keywords = reg_key_sub.sub(',', keywords)
    return keywords


def articles_to_txt(path):
    for root, dirs, files in os.walk(path):
        for name in dirs:
            new_path = os.path.join(root.replace('journals/pdf',
                                                 'journals/txt'), name)
            if not os.path.exists(new_path):
                os.makedirs(new_path)
        for name in files:
            if name.endswith('.pdf'):
                art_path = os.path.join(root, name)
                path_txt = art_path.replace('journals/pdf', 'journals/txt')
                path_txt = path_txt[:-4] + '.txt'
                text = get_text(art_path)
                with codecs.open(path_txt, 'w', encoding='utf-8') as f:
                    f.write(text)


def make_table(path, data_file):
    with codecs.open(data_file, 'w', encoding='utf-8') as f:
        keywords = ''
        f.write('journal;year;issue;first_author;keywords;path\n')
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith('.txt'):
                    full_path = os.path.join(root, name)
                    components = full_path.split('/')
                    journal = components[2]
                    year = components[3]
                    issue = components[4]
                    first_author = ''
                    m = reg_author.search(components[5])
                    if m:
                        first_author = m.group(1)
                    art_keywords = get_keywords(full_path)
                    keywords += art_keywords + '\n'
                    article_line = '{};{};{};{};{};{}\n'.format(journal,
                                                                year,
                                                                issue,
                                                                first_author,
                                                                art_keywords,
                                                                full_path)
                    f.write(article_line)
    with codecs.open('keywords.txt', 'w', encoding='utf-8') as f:
        f.write(keywords)


def find_words(words_path, corpus_path, result_path):
    words = get_words(words_path)
    result = ''
    for root, dirs, files in os.walk(corpus_path):
        for name in files:
            if name.endswith('.txt'):
                file_path = os.path.join(root, name)
                with codecs.open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read().lower()
                    for word in words:
                        if word[0] != '#':
                            m = re.findall(word, text, flags=re.M)
                            c = len(m)
                            if c > 0:
                                result += 'in file {}: {}, {}\n'.format(file_path, word, c)
    with codecs.open(result_path, 'w', encoding='utf-8') as f:
        f.write(result)


def get_words(path):
    words = []
    with codecs.open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            words.append(line)
    return words


if __name__ == '__main__':
    #articles_to_txt('journals/pdf')
    #make_table('journals/txt', 'article_data.csv')
    find_words('query_words.txt', 'journals/txt', 'query_result.txt')