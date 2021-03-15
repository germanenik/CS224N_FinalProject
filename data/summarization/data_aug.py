import os
import random
import argparse

def main(args):
    empty_highlight_files = []
    directory = args.raw_chunk_data_dir
    ending = "chunk0.story" if args.only_read_chunk0 else ".story"
    for filename in os.listdir(directory):
        if filename.endswith(ending):
            data = open(directory + '/' + filename).read()
            if data.split('@highlight')[1].strip() == '':
                empty_highlight_files.append(directory + '/' + filename)
        else:
            continue

    NUM_FILES_TO_GENERATE = args.num_files
    OUTPUT_PATH = args.output_path

    for i in range(NUM_FILES_TO_GENERATE):
        r1 = random.choice(empty_highlight_files)
        r2 = random.choice(empty_highlight_files)
        r1_data = open(r1).read().split('@highlight')[0].strip()
        r2_data = open(r2).read().split('@highlight')[0].strip()
        combined = r1_data[:len(r1_data) // 2] + r2_data[:len(r2_data) // 2]
        combined = combined.replace('\n', ' ')
        f = open(OUTPUT_PATH + '/' + f'random_{i}.story', 'w+')
        f.write(combined)
        f.write('\n')
        f.write('@highlight\n\n')

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
    parser.add_argument("-raw_chunk_data_dir", type=str)
    parser.add_argument("-num_files", type=int)
    parser.add_argument("-output_path", type=str)
    parser.add_argument("-only_read_chunk0", type=str2bool, nargs='?', const=True, default=False)

    args = parser.parse_args()
    main(args)
