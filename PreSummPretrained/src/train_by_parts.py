import train
import argparse
import os
from others.tokenization import BasicTokenizer
#from nltk.tokenize.treebank import TreebankWordToe
from nltk.tokenize.treebank import TreebankWordDetokenizer

def train_by_parts(args):
    if os.path.isdir(args.text_src):
        counter = 0
        dirpath = args.text_src
        entries = sorted(os.listdir(dirpath))
        entries = get_overlap()
        if not args.num_files:
            entries[args.start_file_pos]
        else:
            entries = entries[args.start_file_pos:args.start_file_pos+args.num_files]
        for entry in entries:
            if not entry.endswith(".txt"):
                continue
            file_path = f"{dirpath}/{entry}"

            print("\n")
            print("*"*120)
            print(f"{counter} / {args.num_files}. ***** Summarizing file path {file_path} ******")
            print("*"*120)
            print("\n")

            if not args.debug:
                train_by_parts_singlefile(file_path, args.max_pos, args.debug)
            counter += 1
    else:
        train_by_parts_singlefile(args.text_src, args.max_pos, args.debug)

def train_by_parts_singlefile(text_src_path, max_pos, debug):

    #split file into chunks of size 512
    file_paths = []
    tokenizer = BasicTokenizer()
    detokenizer = TreebankWordDetokenizer()

    print(f'\n\n STARTING TO SPLITTING INTO CHUNKS \n')

    with open(text_src_path) as f:
        text = f.read()
        tokenized = [tup[1] for tup in tokenizer.tokenize(text)] #just list of strings

        prev_endidx = 0
        max_size = max_pos
        file_name_counter = 0
        while prev_endidx < len(tokenized):
            curr_tokens = tokenized[prev_endidx:prev_endidx+max_size]
            if "[SEP]" in curr_tokens: #change later
                print("found [SEP]")
                chunk_len = rindex(curr_tokens,"[SEP]")
            elif "\n" in curr_tokens:
                print("found newline")
                chunk_len = rindex(curr_tokens,"\n")
            elif "." in curr_tokens:
                print("found period")
                chunk_len = rindex(curr_tokens,".")
            else:
                chunk_len = max_size
            print("new end indx")
            curr_tokens = curr_tokens[:chunk_len+1]
           # curr_text =  " ".join(curr_tokens) #figure out to how condense normally
            curr_text =  detokenizer.detokenize(curr_tokens)
            chunk_file_path = get_chunkfile_path(f.name, file_name_counter) 
            chunk_file = open(chunk_file_path, 'w')
            chunk_file.write(curr_text)

            file_paths.append(chunk_file_path)
            prev_endidx += (chunk_len+1)
            file_name_counter += 1
    print(f'\n\n DONE SPLITTING INTO {len(file_paths)} CHUNKS \n')

    #eval on each file
    counter = 0
    for file_path in file_paths:
        print(f'\n\n SUMMARIZING CHUNK {counter} / {len(file_paths)} \n')
        counter += 1
        file_path_notxt = file_path[:-4]
        os.system(f"python train.py -task ext -mode test_text -text_src {file_path} -test_from ../models/bertext_cnndm_transformer.pt -log_file ../logs/cnndm.log -result_path {file_path_notxt}")
    
    #write to one file
    print(f'\n\n WRITING TO ONE SUMMARY FILE \n')
    results_file_path = get_resultsfile_path(text_src_path) 
    with open(results_file_path, 'a') as final_file:
        final_file.truncate(0)
        for file_path in file_paths:
            chunk_result_path = get_chunk_summary_path(file_path)
            with open(chunk_result_path, 'r') as chunk_result:
                final_file.write(chunk_result.read())

def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

def get_chunkfile_path(path: str, file_name_counter: int):
    chunk_name = os.path.basename(path)
    chunk_name = chunk_name[:-4]
    # Create target Directory if don't exist
    if not os.path.exists(f'../chunks/{chunk_name}/'):
        os.mkdir(f'../chunks/{chunk_name}/')
    return f'../chunks/{chunk_name}/{chunk_name}-chunk{file_name_counter}.txt'

def get_resultsfile_path(src_path: str):
    directory = os.path.dirname(src_path)
    target_dir = f'{directory}/summaries/'
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    
    base_name = os.path.basename(src_path)
    base_name = base_name[:-4]
    base_name.replace(" ", "_")
    return f'{target_dir}{base_name}-SUMMARY.txt'


def get_chunk_summary_path(path: str):
    #path is the path of original chunk
    return path[:-4] + '.candidate'

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def get_overlap():
    arr = ['google_Privacy_Policy.txt', 'lastpass_Terms_of_Service.txt', 'github_Privacy_Policy.txt', 'warnerbros_Privacy_Policy.txt', 'yahoo_Terms_of_Service.txt', 'tumblr_Privacy_Policy.txt', 'steam_Steam_Subscriber_Agreement.txt', 'dashlane_Terms_of_Service.txt', 'habbo_Terms_of_Service.txt', 'bing_Privacy_Policy.txt', 'disqus_Privacy_Policy.txt', 'healthline_Terms_of_Use.txt', 'seenthis_Intellectual_Property.txt', 'cloudant_Terms_of_Service.txt', 'yelp_Terms_of_Service.txt', 'runescape_Terms_and_Conditions.txt', 'adobe_Privacy_Policy.txt', 'pocket_Privacy_Policy.txt', 'habbo_Privacy_Policy.txt', 'flattr_Privacy_Policy.txt', 'mint.com_Terms_of_Use.txt', 'academia-edu_Privacy_Policy.txt', 'twitter_Privacy_Policy.txt', 'vimeo_Terms_of_Service.txt', 'bitcasa_Acceptable_Use_Policy.txt', 'evernote_Privacy_Policy.txt', 'biblegateway_Privacy_Policy.txt', 'freeforums_Privacy_Policy.txt', 'apple_iTunes_Terms_of_Service.txt', 'zillow_Privacy_Policy.txt', 'evernote_Terms_of_Service.txt', 'quake_Terms_of_Use.txt', 'apple_Website_Terms_of_Service.txt', 'gitlab_Privacy_Policy.txt', 'facebook_Terms_of_Service.txt', 'deviantart_Terms_of_Service.txt', 'deviantart_Privacy_Policy.txt', 'olx_Terms_of_Use.txt', 'wikipedia_Terms_of_Use.txt', 'linkedin_Privacy_Policy.txt', 'jagex_Terms_and_Conditions.txt', 'toodledo_Terms_of_Service.txt', 'khanacademy_Privacy_Policy.txt', 'youtube_Terms_of_Service.txt', 'zoosk_Privacy_Policy.txt', 'couchsurfing_Terms_of_Use.txt', 'skype_Terms_of_Use.txt', 'envato_Privacy_Policy.txt', 'flickr_Additional_Terms_of_Service.txt', 'quora_Terms_of_Service.txt', 'minecraft_Terms_and_Conditions.txt', 'youtube_Privacy_Policy.txt', 'trello_Privacy_Policy.txt', 'spotify_Terms_and_Conditions_of_Use.txt', 'pinterest_Terms_of_Service.txt', 'toodledo_Privacy_Policy.txt', 'linkedin_Terms_of_Service.txt', 'yelp_Privacy_Policy.txt', 'newegg-com_Privacy_Policy.txt', 'yahoo_Privacy_Policy.txt', 'apple_iCloud_Terms_of_Service.txt', 'mapquest_Privacy_Policy.txt', 'pocket_Terms_of_Service.txt', 'packagetrackr_Terms_of_Service.txt', 'quora_Privacy_Policy.txt', 'apple_Privacy_Policy.txt', 'tinyurl_Terms_of_Service.txt', 'myspace_Terms_of_Service.txt', 'facebook_Data_Policy.txt', 'hulu_Privacy_Policy.txt', 'duckduckgo_Privacy_Policy.txt', 'soundcloud_Terms_of_Service.txt', 'healthline_Privacy_Policy.txt', 'netflix_Terms_of_Use.txt', 'quake_Privacy_Policy.txt', 'grammarly_Privacy_Policy.txt', 'twitter_Terms_of_Service.txt', 'blizzard_Privacy_Policy.txt', 'quake_Legal_Notices.txt', 'w3schools_Terms_of_Use_-_About_Copyright.txt', 'nytimes_Privacy_Policy.txt', 'tumblr_Terms_of_Service.txt', 'wikihow_Privacy_Policy.txt', 'spotify_Privacy_Policy.txt', 'craigslist_Privacy_Policy.txt', 'wikipedia_Privacy_Policy.txt', 'goodreads_Privacy_Policy.txt', 'spideroak_Privacy_Policy.txt', 'etsy_Privacy_Policy.txt', 'github_Terms_of_Service.txt', 'dropbox_Privacy_Policy.txt', 'groupon_Privacy_Policy.txt', 'livejournal_Terms_of_Service.txt', 'amazon_Amazon_Maps_Terms_of_Use.txt', 'wordpress-com_Terms_of_Service.txt', 'coursera_Terms_of_Use.txt', 'w3schools_Cookies_and_Privacy_Policy_-_About_Privacy.txt', 'at-t_Privacy_Policy.txt', 'instagram_Data_Policy.txt', 'metacafe_Privacy_Policy.txt', 'urban-dictionary_Privacy_Policy.txt', 'vimeo_Privacy_Policy.txt', 'fandom_Privacy_Policy.txt', 'reddit_Privacy_Policy.txt', 'cnn_Terms_of_Use.txt', 'reputation.com_Terms_of_Use.txt', 'godaddy_Privacy_Policy.txt', 'coursera_Cookies_Policy.txt', 'ifttt_Terms_of_Use.txt', 'allrecipes_Privacy_Policy.txt', 'foxnews_Privacy_Policy.txt', 'dailymotion_Privacy_Policy.txt', 'couchsurfing_Privacy_Policy.txt', 'disqus_Terms_of_Service.txt', 'fandango_Privacy_Policy.txt', 'newgrounds_Privacy_Policy.txt', 'blogspot_Privacy_Policy.txt', 'grammarly_Terms_of_Service_and_License_Agreement.txt', 'mint.com_Privacy_Policy.txt', 'runescape_Privacy_Policy.txt', 'flattr_Terms_of_Use.txt', 'theguardian_Privacy_Policy.txt', 'jagex_Privacy_Policy.txt', 'bbc_Privacy_and_Cookies_Policy.txt', 'tripadvisor_Privacy_Policy.txt', 'webmd_Privacy_Policy.txt', 'steam_Privacy_Policy_Agreement.txt', 'spideroak_Terms_of_Use.txt', 'blablacar_Privacy_Policy.txt', 'amazon_EU-US_and_Swiss-US_Privacy_Shield.txt', 'amazon_Conditions_of_Use.txt', 'allrecipes_Terms_and_Conditions.txt', 'dailymotion_Terms_of_Use.txt', 'weebly_Terms_of_Service.txt', 'soundcloud_Privacy_Policy.txt', 'researchgate_Privacy_Policy.txt', 'foxnews_Terms_of_Use.txt', 'atlassian(incl-trello,bitbucket)_Privacy_Policy.txt', 'stackexchange_Terms_of_Service.txt', 'researchgate_Terms_of_Service.txt', 'reputation.com_Privacy_Policy.txt', 'nabble_Terms_of_Service.txt', 'quake_EULA.txt', 'bbc_Terms_of_Use.txt', 'imdb_Terms_of_Service.txt', 'ikeausa_Privacy_Policy.txt', 'facebook_Cookie_Policy.txt', 'ifttt_Privacy_Policy.txt']
    return sorted(arr)[::-1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-text_src", default='')  #if a directory, summarize all files
    parser.add_argument("-start_file_pos", nargs='?', const=0, default=0, type=int)
    parser.add_argument("-num_files", nargs='?', const=None, default=None, type=int)

    parser.add_argument("-text_tgt", default='')
    parser.add_argument("-max_pos", default=512, type=int)
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")

    args = parser.parse_args()

    train_by_parts(args)