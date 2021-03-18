import os, json
import pandas as pd
import re
from urllib.request import urlopen
import html2text
import requests
import gzip

def get_quote_text(data, key):
    if key not in data:
        return ""
    text = data[key]
    text = re.sub('<[^>]+>', '', text)
    text = re.sub('\\n', ' ', text)
    return text


def get_link_dict(json_text):
    """ Get the mapping of documents names to their urls """
    link_dict = {}
    for doc in json_text['links']:
        doc_info = json_text['links'][doc]
        link_dict[doc_info['name']] = doc_info['url']
    return link_dict


# after baseline: keep both title and case (as 2 ref translations), get rid of named entities
def tosdr_to_csv():
    """ Parse the Jsons of the ToS;DR data to grab the features relevant to our project, saving it to a csv """
    # from https://stackoverflow.com/questions/30539679/python-read-several-json-files-from-a-folder
    # this finds our json files
    path_to_json = 'tosdr_data/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # here I define my pandas Dataframe with the columns I want to get from the json
    jsons_data = pd.DataFrame(columns=['quote_text', 'title', 'case', 'tldr', 'service', 'source_doc'])

    # we need both the json and an index number so use enumerate()
    for index, js in enumerate(json_files):
        service_name = js[:-5]
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            #link_dict = get_link_dict(json_text)

            for key in json_text['pointsData']:
                # take out the pertinent data
                quote_text = get_quote_text(json_text['pointsData'][key], 'quoteText')
                title = json_text['pointsData'][key]['title']
                case = json_text['pointsData'][key]['tosdr']['case']
                tldr = json_text['pointsData'][key]['tosdr']['tldr']
                tldr_quotes = " ".join(re.findall(r'"[^"]*"', tldr))
                tldr_quotes = re.sub('"', '', tldr_quotes)
                if tldr == "Generated through the annotate view":
                    tldr = ""
                elif tldr_quotes != "":
                	tldr = tldr_quotes
                quote_doc = json_text['pointsData'][key]['quoteDoc'] if 'quoteDoc' in json_text['pointsData'][key] else ""
                #link = json_text['links'][quote_doc]['url']

                # if service_name == 'wemod.json' and key == '10405':
                #     print(quote_text, title, case, tldr)

                # choose the data we want
                #quote = quote_text if quote_text != "" and len(quote_text) >= len(tldr) else tldr
                # if service_name == 'wemod.json' and key == '10405':
                #     print(quote)
                #simp = title if title != "" else case

                # push the data into a new row of the pandas DataFrame
                jsons_data = jsons_data.append(
                    {'quote_text': quote_text.lower(), 'title': title, 'case': case, 'tldr': tldr, 
                    'service': service_name, 'source_doc': quote_doc}, ignore_index=True)
    jsons_data.to_csv("parsed_tosdr_data.csv", encoding='utf-8-sig')


def download_ToS_pages():
    """ Go through each of the services and download their Terms of Service/Cookie Policy pages 
        Note -- failed pages:
            - sonic-net All Policies
            - paypal-com Privacy Policy
            - paypal Privacy Policy
            - paypal-com-duplicateofservice230 Privacy Policy
    """
    path_to_json = 'tosdr_data/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # we need both the json and an index number so use enumerate()
    for index, js in enumerate(json_files):
        service_name = json_files[index][:-5]
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)
            for doc_name in json_text['links']:
                name = json_text['links'][doc_name]['name']
                url = json_text['links'][doc_name]['url']
                # page = urlopen(url)
                # html_content = page.read()
                #print('Trying: ', service_name, name, url)
                try:
                    html_content = requests.get(url, 
                    headers={"User-Agent": 
                    "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
                    ).text  # => str, not bytes
                except requests.exceptions.ConnectionError as e:
                    print('FAILED: ', service_name, name)
                    continue

                rendered_content = html2text.html2text(html_content).lower()
                # charset = page.headers.get_content_charset()
                # rendered_content = html_content.decode(charset)
                # if page.getcode()!=200:
                #     print("Http code:",page.getcode())
                #     continue;
                # else:
                #     try:
                #         charset = page.headers.get_content_charset()
                #         rendered_content = html_content.decode(charset)
                #     except:
                #         decompressed_content = gzip.decompress(html_content)
                #         rendered_content = decompressed_content.decode('utf-8')
                file = open('full_texts/' + service_name + "_" + name + '.txt', 'w+')
                file.write(rendered_content)
                file.close()


def quotes_from_csv():
    """ Grab the quotes (whether it's quoteText or tldr) from the csv and put it in a .txt file """
    df = pd.read_csv("parsed_tosdr_data.csv", encoding='utf-8-sig')
    df.fillna("", inplace=True)
    lines = []
    for index, row in df.iterrows():
        quote_text = row['quote_text']
        tldr = row['tldr']
        line = quote_text if quote_text != "" and len(quote_text) >= len(tldr) else tldr
        line = re.sub('\\n', ' ', line)
        lines.append(line)
    with open('quotes.complex', 'w') as f:
        f.writelines("%s\n" % i for i in lines)


def simple_from_csv():
    """ Grab the quotes (whether it's quoteText or tldr) from the csv and put it in a .txt file """
    df = pd.read_csv("parsed_tosdr_data.csv", encoding='utf-8-sig')
    df.fillna("", inplace=True)
    lines = []
    for index, row in df.iterrows():
        title = row['title']
        case = row['case']
        line = title if title != "" else case
        line = re.sub('\\n', ' ', line)
        lines.append(line)
    with open('quotes.simple', 'w') as f:
        f.writelines("%s\n" % i for i in lines)


def group_doc_quotes_together():
    """ For summarization, coalesce the quotes from one ToS doc into one text file """
    resulting_path = 'summarization/quotes/'
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


if __name__ == '__main__':
    quotes_from_csv()