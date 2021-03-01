import train
import argparse
import os
from others.tokenization import BasicTokenizer
#from nltk.tokenize.treebank import TreebankWordToe
from nltk.tokenize.treebank import TreebankWordDetokenizer

def train_by_parts(args):

    #split file into chunks of size 512
    file_paths = []
    tokenizer = BasicTokenizer()
    detokenizer = TreebankWordDetokenizer()

    print(f'\n\n STARTING TO SPLITTING INTO CHUNKS \n')

    with open(args.text_src) as f:
        text = f.read()
        tokenized = [tup[1] for tup in tokenizer.tokenize(text)] #just list of strings

        prev_endidx = 0
        max_size = args.max_pos
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
        print(f'\n\n SUMMARIZING CHUNK {counter} \n')
        counter += 1
        file_path_notxt = file_path[:-4]
        os.system(f"python train.py -task ext -mode test_text -text_src {file_path} -test_from ../models/bertext_cnndm_transformer.pt -log_file ../logs/cnndm.log -result_path {file_path_notxt}")
    
    #write to one file
    print(f'\n\n WRITING TO ONE SUMMARY FILE \n')
    results_file_path = get_resultsfile_path(args.text_src) 
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

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-text_src", default='')
    parser.add_argument("-text_tgt", default='')
    parser.add_argument("-max_pos", default=512, type=int)
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")
    args = parser.parse_args()

    train_by_parts(args)