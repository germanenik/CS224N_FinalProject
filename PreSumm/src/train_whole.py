import train
import argparse
import os

def train_whole(args):
    codeword = args.experiment_code_word
    try:
        os.mkdir(f"../trial_{codeword}")
    except FileExistsError:
        print("trial w codeword already exists")
        return

    #raw to data0
    data0_path = get_data_dir_path(codeword, 0)
    os.mkdir(data0_path)
    logfile_path = get_log_file_path(codeword, 0)
    os.system(f"python preprocess.py -mode tokenize -raw_path {args.raw_chunk_data} -save_path {data0_path} -log_file {logfile_path} -min_tgt_ntokens 0")

    #data0 to data1
    data1_path = get_data_dir_path(codeword, 1)
    os.mkdir(data1_path)
    logfile_path = get_log_file_path(codeword, 1)
    os.system(f"python preprocess.py -mode format_to_lines -raw_path {data0_path} -save_path {data1_path} -n_cpus 1 -use_bert_basic_tokenizer false -log_file {logfile_path} -min_tgt_ntokens 0")
    #move data_split
    os.rename("../data_split.json", f"../trial_{codeword}/data_split.json")

    #data1 to data 2
    data2_path = get_data_dir_path(codeword, 2)
    os.mkdir(data2_path)
    logfile_path = get_log_file_path(codeword, 2)
    os.system(f"python preprocess.py -mode format_to_bert -raw_path {data1_path} -save_path {data2_path} -lower -n_cpus 1 -log_file {logfile_path} -min_tgt_ntokens 0")

    #train
    models_dir = get_models_path(codeword)
    os.mkdir(models_dir)
    os.system(f"python train.py -task ext -mode train -bert_data_path {data2_path} -ext_dropout 0.1 -model_path {models_dir} -lr 2e-3 -visible_gpus 0 -report_every 50 -save_checkpoint_steps 300 -batch_size 3000 -train_steps 50000 -accum_count 2 -log_file ../logs/{codeword}-train.log -use_interval true -warmup_steps 10000 -max_pos 512 -train_from ../baseline_models/model_step_18000.pt")

    #create validation folder
    os.mkdir(get_valid_path(codeword))

def get_data_dir_path(codeword, num):
    #num is 0 / 1 / 2
    return f"../trial_{codeword}/{codeword}_data{num}"

def get_models_path(codeword):
    return f"../trial_{codeword}/{codeword}_models"

def get_valid_path(codeword):
    return f"../trial_{codeword}/{codeword}_valid"

def get_log_file_path(codeword, num):
    #num is data dir num that is BEING SAVED to
    if num == 0:
        return f"../logs/{codeword}-raw-to-data{num}.log"
    return f"../logs/{codeword}-data{num-1}-to-data{num}.log"

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
    parser.add_argument("-raw_chunk_data", type=str, default='')
    parser.add_argument("-experiment_code_word", type=str)
    parser.add_argument("-max_pos", default=512, type=int)
    parser.add_argument("-debug", type=str2bool, nargs='?', const=True, default=False, help="Debug mode (no trainig done).")

    args = parser.parse_args()

    train_whole(args)