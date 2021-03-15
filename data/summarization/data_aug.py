import os
import random

empty_highlight_files = []
directory = 'raw_chunk_data_clean'
for filename in os.listdir(directory):
    if filename.endswith(".story"):
        data = open(directory + '/' + filename).read()
        if data.split('@highlight')[1].strip() == '':
            empty_highlight_files.append(directory + '/' + filename)
    else:
        continue

NUM_FILES_TO_GENERATE = 20
OUTPUT_PATH = 'data_augmentation_data'

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
