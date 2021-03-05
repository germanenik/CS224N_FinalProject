from rouge import Rouge
import argparse
import os

SUMMARY_FILE_SUFFIX = "-SUMMARY.txt"

def compute_rouge(args):
    #breakpoint()
    cand, ref = args.c, args.r
    cand_is_dir = os.path.isdir(cand)
    ref_is_dir = os.path.isdir(ref)
    rouge_scores = []
    assert cand_is_dir == ref_is_dir
    if not ref_is_dir:
        rouge_score = compute_rouge_instance(cand, ref, args.debug)
        rouge_scores.append(rouge_score)
    else:
        cand_files = os.listdir(cand)
        ref_files = os.listdir(ref)
        for ref_file_name in sorted(ref_files):
            cand_file_name = ref_name_2_cand_name(ref_file_name)
            if cand_file_name not in cand_files:
                continue
            cand_file_path = get_file_path(cand, cand_file_name)
            ref_file_path = get_file_path(ref, ref_file_name)
            try:
                rouge_score = compute_rouge_instance(cand_file_path, ref_file_path, args.debug)
                rouge_scores.append(rouge_score)
            except (RecursionError, AssertionError) as e:
                print(f"Error {e} encountered when calculating rouge for {cand_file_name} and {ref_file_name}")

    print("Length of rouge reports: ", len(rouge_scores))
    print(rouge_scores)
            
def ref_name_2_cand_name(ref_file_name):
    prefix = ""
    if ref_file_name.endswith(".txt"):
        prefix = ref_file_name[:-4]
    else:
        prefix = ref_file_name
    return prefix + SUMMARY_FILE_SUFFIX 

def get_file_path(dir_path, file_name):
    return dir_path + "/" + file_name 

def compute_rouge_instance(cand_file, ref_file, debug):
    # returns a dictinary
    if debug:
        return (cand_file, ref_file)

    cand_text, ref_text = "", ""
    with open(cand_file, "r") as cand:
        cand_text = cand.read()
    with open(ref_file, "r") as ref:
        ref_text = ref.read()
    assert len(cand_text) != 0
    assert len(ref_text) != 0
    cand_text.replace('\n', ' ')
    ref_text.replace('\n', ' ')

    rouge_ = Rouge()
    scores = rouge_.get_scores(cand_text, ref_text)
    print("Rouge scores:")
    print(scores)
    return scores


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
    #can provide two directories or two files
    parser.add_argument('-c', type=str, default="candidate.txt",
                        help='candidate file')
    parser.add_argument('-r', type=str, default="reference.txt",
                        help='reference file')
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")

    args = parser.parse_args()
    print(args.c)
    print(args.r)

    compute_rouge(args)
