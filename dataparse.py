import os, json
import pandas as pd
import re

def getQuoteText(data, key):
    if key not in data:
        return ""
    text = data[key]
    text = re.sub('<[^>]+>', '', text)
    text = re.sub('\\n', ' ', text)
    # text = re.sub('‚Äì', '-', text)
    # text = re.sub('‚Äô', '\'', text)
    return text


def parse_jsons():
    # from https://stackoverflow.com/questions/30539679/python-read-several-json-files-from-a-folder
    # this finds our json files
    path_to_json = 'tosdr_data/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # here I define my pandas Dataframe with the columns I want to get from the json
    jsons_data = pd.DataFrame(columns=['quote', 'simplified', 'service'])

    # we need both the json and an index number so use enumerate()
    for index, js in enumerate(json_files):
        serviceName = json_files[index]
        with open(os.path.join(path_to_json, js)) as json_file:
            json_text = json.load(json_file)

            for key in json_text['pointsData']:
                # take out the pertinent data
                quoteText = getQuoteText(json_text['pointsData'][key], 'quoteText')
                title = json_text['pointsData'][key]['title']
                case = json_text['pointsData'][key]['tosdr']['case']
                tldr = json_text['pointsData'][key]['tosdr']['tldr']
                quotesInTLDR = " ".join(re.findall(r'"[^"]*"', tldr))
                if tldr == "Generated through the annotate view":
                    tldr = ""
                elif quotesInTLDR != "":
                	tldr = quotesInTLDR

                # if serviceName == 'wemod.json' and key == '10405':
                #     print(quoteText, title, case, tldr)

                # choose the data we want
                quote = quoteText if quoteText != "" and len(quoteText) >= len(tldr) else tldr
                # if serviceName == 'wemod.json' and key == '10405':
                #     print(quote)
                simp = title if title != "" else case

                # push the data into a new row of the pandas DataFrame
                jsons_data = jsons_data.append({'quote': quote, 'simplified': simp, 'service': serviceName}, ignore_index=True)
    jsons_data.to_csv("parsed_tosdr_data.csv", encoding='utf-8-sig')


if __name__ == '__main__':
    parse_jsons()