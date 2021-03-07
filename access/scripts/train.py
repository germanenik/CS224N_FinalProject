# Copyright (c) Facebook, Inc. and its affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from access.fairseq.main import fairseq_train_and_evaluate
from access.resources.prepare import prepare_wikilarge, prepare_turkcorpus
import random

if __name__ == '__main__':
    print('Training a model from scratch')
    prepare_wikilarge()
    prepare_turkcorpus()
    kwargs = {
        'arch': 'transformer',
        'warmup_updates': 4000,
        'parametrization_budget': 256,
        'beam': random.randint(2, 10),
        'dataset': 'simplification',
        'dropout': random.random(),
        'fp16': False,
        'label_smoothing': random.random(),
        'lr': random.random() * 10^(random.randint(-5, 0)),
        'lr_scheduler': 'fixed',
        'max_epoch': 100,
        'max_tokens': 5000,
        'metrics_coefs': [0, 1, 0],
        'optimizer': 'adam',
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
    fairseq_train_and_evaluate(**kwargs)
