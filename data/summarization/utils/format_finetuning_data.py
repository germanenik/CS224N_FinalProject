import argparse
import os
import sys
sys.path.append("../../../PreSumm/src/others/")
from tokenization import BasicTokenizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
import re

tokenizer = BasicTokenizer()
detokenizer = TreebankWordDetokenizer()

def format_finetuning(args):
    full, ref = args.full_texts, args.reference_texts
    full_is_dir = os.path.isdir(full)
    ref_is_dir = os.path.isdir(ref)
    global_count = 0
    assert full_is_dir == ref_is_dir

    full_files = sorted(os.listdir(full))
    ref_files = os.listdir(ref)

    for full_file in full_files:
        if full_file not in ref_files:
            continue
        full_file_path = get_file_path(full,full_file)

        with open(full_file_path) as f:
            text = f.read()
            if args.remove_characters:
                text = remove_characters(text, r"[^A-Za-z0-9 \n.,;?]")
            tokenized = [tup[1] for tup in tokenizer.tokenize(text)] #just list of strings

            prev_endidx = 0
            max_size = args.max_pos
            file_name_counter = 0
            while prev_endidx < len(tokenized):
                curr_tokens = tokenized[prev_endidx:prev_endidx+max_size]
                if "[SEP]" in curr_tokens:
                    chunk_len = rindex(curr_tokens,"[SEP]")
                elif "\n" in curr_tokens:
                    chunk_len = rindex(curr_tokens,"\n")
                elif "." in curr_tokens:
                    chunk_len = rindex(curr_tokens,".")
                elif ";" in curr_tokens:
                    chunk_len = rindex(curr_tokens,";")
                else:
                    chunk_len = max_size
                curr_tokens = curr_tokens[:chunk_len+1]

                curr_text = detokenizer.detokenize(curr_tokens)
                curr_text = curr_text.replace("[CLS] [SEP]", "") #remove them for training, only need for eval

                ref_file_path = get_file_path(ref, full_file) #full_file is ref_file
                chunk_file_path = get_chunkfile_path(f.name, file_name_counter, args.output_dir)
                curr_text = add_highlights(curr_text, ref_file_path, chunk_file_path)
                
                chunk_file = open(chunk_file_path, 'w')
                chunk_file.write(curr_text)

                prev_endidx += (chunk_len+1)
                file_name_counter += 1
        print(f"DONE NUMBER {global_count}")
        global_count += 1
    
    print(f'\n\n DONE REFORMATTING \n')

def remove_characters(text, regex):
    delim, ans = "[CLS] [SEP]", ""
    subtexts = text.split(delim)
    for subtext in subtexts:
        ans += (re.sub(regex, "", subtext)) 
    #print(ans)
    return ans

def rindex(lst, value):
    lst.reverse()
    i = lst.index(value)
    lst.reverse()
    return len(lst) - i - 1

def get_chunkfile_path(file_path: str, file_name_counter: int, output_dir: str):
    chunk_name = os.path.basename(file_path)
    if chunk_name.endswith(".txt"):
        chunk_name = chunk_name[:-4]
    return f'{output_dir}/{chunk_name}-chunk{file_name_counter}.story'

def get_file_path(dir_path, file_name):
    return dir_path + "/" + file_name 

def add_highlights(curr_text, ref_file_path, file):
    added_quote = False
    with open(ref_file_path, "r") as ref:
        quotes_text = ref.read()
        tokenized = [tup[1] for tup in tokenizer.tokenize(quotes_text)] #for formatting
        quotes_text = detokenizer.detokenize(tokenized) #for formatting
        quotes_arr = re.split('\[CLS\] \[SEP\]', quotes_text) #also removes all "[CLS] [SEP]"
        for quote in quotes_arr:
            quote = quote.strip()
            quote = remove_characters(quote, r"[^A-Za-z0-9 \n.,;?]")
            if quote == "":
                continue
            if quote in curr_text:
                added_quote = True
                print(f"added quote tp {file}")
                curr_text += f"\n@highlight\n{quote}\n"
        if not added_quote:
            curr_text += f"\n@highlight\n\n"

    return curr_text


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == "__main__":
    # init_logger('test_rouge.log')
    parser = argparse.ArgumentParser()
    #provide two directories
    parser.add_argument('-full_texts', type=str, default="candidate.txt",
                        help='full dir')
    parser.add_argument('-reference_texts', type=str, default="reference.txt",
                        help='reference dir')
    parser.add_argument("-output_dir", type=str)
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")
    parser.add_argument("-remove_characters", type=str2bool, nargs='?', const=True, default=False)
    parser.add_argument("-max_pos", default=512, type=int)
    args = parser.parse_args()

    format_finetuning(args)