import argparse
import re
import os
import codecs

def build_pipeline_reference(args):
    qcomplex_arr = get_quotes_array(args.all_complex_quotes)
    qsimple_arr = get_quotes_array(args.all_simple_quotes)
    qcomplex_arr = [q.decode("utf-8").strip() for q in qcomplex_arr]
    qsimple_arr = [q.decode("utf-8").strip() for q in qsimple_arr]

    print(len(qcomplex_arr), len(qsimple_arr))
    # print(qcomplex_arr)

    # qgold_arr = get_quotes_array(args.gold_pulled_quotes)
    # qgold_arr = [q.decode("utf-8") for q in qgold_arr]
    qgold_arr = [line.strip() for line in codecs.open(args.gold_pulled_quotes, encoding="utf-8")]
    pipeline_gold_arr = []

    found = 0
    not_found = 0
    for quote in qgold_arr:
        if quote == '':
            pipeline_gold_arr.append("")
        else:
            entries = []
            subquotes = quote.split("<q>")
            for subq in subquotes:
                alnums = re.findall(r"[a-z0-9 ]+", subq)
                alnums = [alnum.strip() for alnum in alnums]
                if len(alnums) == 0:
                    continue
                candidate_indices = [x for x in range(len(qcomplex_arr))]
                for alnum in alnums:
                    candidate_indices = [idx for idx in candidate_indices if alnum in qcomplex_arr[idx]]
                    if len(candidate_indices) == 1:
                        idx = candidate_indices[0]
                        entries.append(qsimple_arr[idx])
                        found += 1
                        break
                
                if len(candidate_indices) > 1:
                    candidates = [qsimple_arr[idx] for idx in candidate_indices]
                    entries.append(min(candidates, key=len))
                    found += 1
                elif len(candidate_indices) == 0:
                    print("***")
                    # print("candidate indices:", candidate_indices)
                    print(f"couldn't locate subquote, locate manually '{subq}'")
                    # print("complex / simple candidates:", [(qcomplex_arr[i], qsimple_arr[i]) for i in candidate_indices])
                    # print("***\n\n")
                    #entries.append("<RAW>" + subq + "<RAW>")
                    entries.append(subq)
                    not_found += 1
                
            entry = " ".join(entries)
            pipeline_gold_arr.append(entry)
    print(f"subqs not found: {not_found}")
    print(f"subqs found: {found}")
    print(f"pipeline gold arr length: {len(pipeline_gold_arr)}")
    print(f"quote gold arr length: {len(pipeline_gold_arr)}")

    with open(f"{os.path.dirname(args.gold_pulled_quotes)}/quotes.ref", "w", encoding='utf8') as f:
        for q in pipeline_gold_arr:
            q.strip()
            f.write(f"{q}\n")
    #in the end write each quote per new line

def get_quotes_array(file):
    with open(file, "rb") as f:
        return f.readlines()
    # text = codecs.open(file, encoding="utf-8")
    # return [line.strip() for line in text]

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
    parser.add_argument('-gold_pulled_quotes', type=str)
    parser.add_argument('-all_complex_quotes', type=str)
    parser.add_argument("-all_simple_quotes", type=str)

    args = parser.parse_args()

    build_pipeline_reference(args)