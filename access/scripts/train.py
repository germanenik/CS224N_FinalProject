# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from access.fairseq.main import fairseq_train_and_evaluate
from access.resources.prepare import prepare_wikilarge, prepare_turkcorpus
import random
import sys
import uuid
import os
from glob import glob
from shutil import rmtree

if __name__ == '__main__':
    # while(True):
    #     orig_stdout = sys.stdout
    #     new_file = uuid.uuid4()
    #     print(new_file)
    #     orig_stdout = sys.stdout
    #     f = open(f'{new_file}.txt', 'w+')
    #     sys.stdout = f
    print('Training a model from scratch')
    prepare_wikilarge()
    prepare_turkcorpus()
    random_kwargs = {
        'arch': 'transformer',
        'warmup_updates': 4000,
        'parametrization_budget': 256,
        'beam': random.randint(2, 10),
        'dataset': 'simplification',
        'dropout': random.random(),
        'fp16': False,
        'label_smoothing': random.random(),
        'lr': random.random() * (10.0 ** random.randint(-5, -3)),
        'lr_scheduler': 'fixed',
        'max_epoch': 100,
        'max_tokens': 5000,
        'metrics_coefs': [0, 1, 0],
        'optimizer': 'adam',
        'validations_before_sari_early_stopping': 10,
        'preprocessors_kwargs': {
            'LengthRatioPreprocessor': {
                'target_ratio': random.random()  # Default initial value
            },
            'LevenshteinPreprocessor': {
                'target_ratio': random.random()  # Default initial value
            },
            'WordRankRatioPreprocessor': {
                'target_ratio': random.random()  # Default initial value
            },
            'DependencyTreeDepthRatioPreprocessor': {
                'target_ratio': random.random()  # Default initial value
            },
            'SentencePiecePreprocessor': {
                'vocab_size': 10000
            }
        }
    }
    best_kwargs = {
        'arch': 'transformer',
        'warmup_updates': 4000,
        'parametrization_budget': 64,
        'beam': 4,
        'dataset': 'simplification',
        'dropout': 0.01322026984,
        'fp16': False,
        'label_smoothing': 0.08144495379,
        'lr': 6.40E-06,
        'lr_scheduler': 'fixed',
        'max_epoch': 100,
        'max_tokens': 5000,
        'metrics_coefs': [0, 1, 0],
        'optimizer': 'adam',
        'validations_before_sari_early_stopping': 10,
        'preprocessors_kwargs': {
            'LengthRatioPreprocessor': {
                'target_ratio': 0.65
            },
            'LevenshteinPreprocessor': {
                'target_ratio': 0.4
            },
            'WordRankRatioPreprocessor': {
                'target_ratio': 0.9
            },
            'DependencyTreeDepthRatioPreprocessor': {
                'target_ratio': 0.45
            },
            'SentencePiecePreprocessor': {
                'vocab_size': 10000
            }
        }
    }
    try:
        fairseq_train_and_evaluate(**best_kwargs)
    except:
        print('Unexpected error', sys.exc_info()[0])
        print('this run failed.')
        # sys.stdout = orig_stdout
        # f.close()
        # path = 'resources/datasets/'
        # pattern = os.path.join(path, "_*")

        # for item in glob(pattern):
        #     if not os.path.isdir(item):
        #         continue
        #     rmtree(item)
        #     print('removing', item)
