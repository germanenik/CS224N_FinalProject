import argparse
import os
import json

def main(args):
    data = parse_json_txtfile(args.json_data)
    if args.print_averages:
        print_averages_rouge(data)

def parse_json_txtfile(path):
    with open(path, 'r') as f:
        json_str = f.read()
        return json.loads(json_str)

def print_averages_rouge(data):
    rouges = ["rouge-1", "rouge-2", "rouge-l"]
    metrics = [{'f': 0, 'p': 0, 'r': 0}, {'f': 0, 'p': 0, 'r': 0}, {'f': 0, 'p': 0, 'r': 0}]
    count = 0 #need counnt cuz some are None
    for datum in data:
        for rouge_type, indiv_metrics in datum[0].items():
            for metric, value in indiv_metrics.items():
                i = rouges.index(rouge_type)
                metrics[i][metric] += value
        count += 1
    print({rouges[i]: {metric: value / count for metric, value in metrics[i].items()} for i in range(len(rouges))})


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
    parser.add_argument('-json_data', type=str, help='path to txt file w json data')
    parser.add_argument("-print_averages", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")

    args = parser.parse_args()
    main(args)