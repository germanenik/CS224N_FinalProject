import os, json
import pandas as pd
import re
from urllib.request import urlopen
import html2text
import requests
import gzip

def group_doc_quotes_together():
    """ For summarization, coalesce the quotes from one ToS doc into one text file """
    resulting_path = 'quotes/'
    df = pd.read_csv("parsed_tosdr_data.csv", encoding='utf-8-sig')
    df.fillna("", inplace=True)
    for index, row in df.iterrows():
        service = row['service']
        docname = re.sub('/', '', row['source_doc'])
        quote_text = row['quote_text']
        tldr = row['tldr']
        line = quote_text if quote_text != "" and len(quote_text) >= len(tldr) else tldr
        line = re.sub('\\n', ' ', line)
        if len(line) > 1:
            if line.endswith('.'):
                line += ' '
            elif not line.endswith('. '):
                line += '. '
        filename = resulting_path + service + '_' + docname + '.txt'
        with open(filename, 'a+') as f:
            f.writelines("%s" % line)


def add_separators_to_texts(path_to_texts):
    """ Add [CLS] [SEP] to the end of every sentence and/or paragraph """
    for filename in os.scandir(path_to_texts):
        if filename.path.endswith('.txt'):
            #print(filename)
            with open(filename, 'r') as f:
                lines = f.readlines()
            with open(filename, 'w') as f:
                for line in lines:
                    line = line.replace('. ', '. [CLS] [SEP] ')
                    # if line != "":
                    #     print(line[-1])
                    # if line.endswith(".\n"):
                    #     line += '[CLS] [SEP]'
                    line = line.replace('.\n', '. [CLS] [SEP]\n')
                    f.write(line)


def count_shared_filenames():
    full_texts_path = 'full_texts/'
    quotes_path = 'quotes/'
    full_text_filenames = set([filename for filename in os.listdir(full_texts_path) if filename.endswith('.txt')])
    quote_filenames = [filename for filename in os.listdir(quotes_path) if filename.endswith('.txt')]
    #full_names_set = set(list1)
    intersection = full_text_filenames.intersection(quote_filenames)
    print(intersection)



if __name__ == '__main__':
    count_shared_filenames()