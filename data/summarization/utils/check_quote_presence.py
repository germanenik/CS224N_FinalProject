import argparse
import os

def calc_quote_presence(args):
    #breakpoint()
    full, ref = args.full_texts, args.reference_texts
    full_is_dir = os.path.isdir(full)
    ref_is_dir = os.path.isdir(ref)
    assert full_is_dir == ref_is_dir

    full_files = os.listdir(full)

    ref_files = os.listdir(ref)
    if args.num_files:
        ref_files = ref_files[args.start_file_pos:args.start_file_pos+args.num_files]
    else:
        ref_files = ref_files[args.start_file_pos:]
    ref_files.sort()

    global_total_quotes = 0
    global_present_quotes = 0
    tokens_present = 0

    for ref_file_name in ref_files:
        local_total_quotes = 0
        local_present_quotes = 0
        if ref_file_name not in full_files:
            continue
        full_file_name = ref_file_name
        full_file_path = get_file_path(full, full_file_name)
        ref_file_path = get_file_path(ref, ref_file_name)
        
        with open(ref_file_path, "r") as ref_f:
            with open(full_file_path, "r") as full_f:
                ref_string = ref_f.read().replace("\n", " ")
                full_string = full_f.read().replace("\n", " ")
                quotes = ref_string.split(" [CLS] [SEP] ")
                print(f"\n\n****{ref_file_name}****")
                for quote in quotes:
                    if quote == "":
                        continue
                    global_total_quotes += 1
                    local_total_quotes += 1
                    if quote in full_string:
                        tokens_present += len(quote.split(" "))
                        global_present_quotes += 1
                        local_present_quotes += 1
                    else:
                        print(f"quote absent: {quote}")
                print(f"{ref_file_name} quote count: {pretty_print(local_present_quotes, local_total_quotes)}")
    
    print(f"Total quote presence: {pretty_print(global_present_quotes, global_total_quotes)}")
    print(f"Token count in present quotes: {tokens_present}")

def get_file_path(dir_path, file_name):
    return dir_path + "/" + file_name 

def pretty_print(present, total):
    return f"{present} / {total}  = {present / total * 100}%"

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
    parser.add_argument("-start_file_pos", nargs='?', const=0, default=0, type=int)
    parser.add_argument("-num_files", nargs='?', const=None, default=None, type=int)
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")

    args = parser.parse_args()

    calc_quote_presence(args)