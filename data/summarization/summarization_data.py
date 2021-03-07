import os, json
import pandas as pd
import re
from urllib.request import urlopen
import html2text
import requests
import gzip


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
                    line = line.replace('.\n', '. [CLS] [SEP]\n')
                    f.write(line)


def count_shared_filenames():
    full_texts_path = 'full_texts/'
    quotes_path = 'quotes/'
    full_text_filenames = set([filename for filename in os.listdir(full_texts_path) if filename.endswith('.txt')])
    quote_filenames = [filename for filename in os.listdir(quotes_path) if filename.endswith('.txt')]
    intersection = full_text_filenames.intersection(quote_filenames)
    print(intersection)


def swap_separators(path_to_texts):
    """ Swap the separators [CLS] [SEP] in all texts along this path """
    for filename in os.scandir(path_to_texts):
        if filename.path.endswith('.txt'):
            with open(filename, 'r') as f:
                lines = f.readlines()
            with open(filename, 'w') as f:
                for line in lines:
                    line = line.replace('[CLS] [SEP]', '[SEP] [CLS]')
                    line = line.replace('[SEP] [CLS]', '[CLS] [SEP]')
                    f.write(line)


def download_ToS_pages():
    """ Go through each of the links in the text doc and download their Terms of Service/Cookie Policy pages
        Note -- failed pages:
            - openmailbox Privacy Policy
            - guerrillamail Terms of Service
            - guerrillamail About
    """
    resulting_path = 'new_full_texts/'
    df = pd.read_csv("links_to_add.csv", encoding='utf-8-sig')
    df.fillna("", inplace=True)
    for index, row in df.iterrows():
        service = row['service']
        docname = re.sub('/', '', row['source_doc'])
        used = row['used']
        if (used == 'y'):
            continue
        url = row['url']
        if (pd.isna(url)):
            break
        try:
            html_content = requests.get(url, 
            headers={"User-Agent": 
            "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
            ).text  # => str, not bytes
        except requests.exceptions.ConnectionError as e:
            print('FAILED: ', service, docname)
            continue

        rendered_content = html2text.html2text(html_content).lower()
        file = open(resulting_path + service + "_" + docname + '.txt', 'w+')
        file.write(rendered_content)
        file.close()

if __name__ == '__main__':
    # swap_separators('full_texts/')
    # swap_separators('quotes/')
    #download_ToS_pages()
    add_separators_to_texts('new_full_texts/')