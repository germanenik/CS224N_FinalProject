from rouge import Rouge
import argparse

def compute_rouge(cand_file, ref_file):
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
    

if __name__ == "__main__":
    # init_logger('test_rouge.log')
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', type=str, default="candidate.txt",
                        help='candidate file')
    parser.add_argument('-r', type=str, default="reference.txt",
                        help='reference file')
    args = parser.parse_args()
    print(args.c)
    print(args.r)

    compute_rouge(args.c, args.r)
