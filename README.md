# Project description

Code:
* pdf_to_txt.py - takes a folder of journals structured as root/pdf/journal_title/issue/article.pdf and converts pdf-files to .txt in root/txt/journal_title/issue/article.txt. Does not convert secured text, cyrillic text. Formatting problems with columns, spaces, OCR mistakes.
* find_tests.py - takes a list of items from query_words.txt and finds them in a folder of .txt files. The result is in query_result.txt in format article_path: query_word, frequency.

Folders, text files, and tables:
* test_list.txt - a clean list of quantitative methods to be found in articles
* query_words.txt - a modified test_list.txt with added spelled-out abbreviations, query words with and without spaces/dashes; to be used in find_tests.py 
* query_result.txt - a result of search in find_tests.py
* article_data.xlsx - journal;year;issue;first_author;keywords;path - for Lingua
* keywords.txt - extracted keywords from Lingua
* journals/txt/Lingua - an example of .pdf to .txt conversion for Lingua
