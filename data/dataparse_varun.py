import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('parsed_tosdr_data.csv')
df = df.fillna('')
print(len(df))
train, test = train_test_split(df, test_size=0.1)
test, val = train_test_split(test, test_size=0.5)
print(len(train), len(test), len(val))

complex_train_file = open('simplification/simplification.train.complex', 'a')
complex_test_file = open('simplification/simplification.test.complex', 'a')
complex_valid_file = open('simplification/simplification.valid.complex', 'a')
simple_train_file = open('simplification/simplification.train.simple', 'a')
simple_test_file = open('simplification/simplification.test.simple', 'a')
simple_valid_file = open('simplification/simplification.valid.simple', 'a')

for i, row in train.iterrows():
    complx = row['quote_text']
    simple = row['title']
    if complx == '' or simple == '':
        continue
    complex_train_file.write(' '.join(complx.split()) + '\n')
    simple_train_file.write(' '.join(simple.split()) + '\n')
for i, row in test.iterrows():
    complx = row['quote_text']
    simple = row['title']
    if complx == '' or simple == '':
        continue
    complex_test_file.write(' '.join(complx.split()) + '\n')
    simple_test_file.write(' '.join(simple.split()) + '\n')
for i, row in val.iterrows():
    complx = row['quote_text']
    simple = row['title']
    if complx == '' or simple == '':
        continue
    complex_valid_file.write(' '.join(complx.split()) + '\n')
    simple_valid_file.write(' '.join(simple.split()) + '\n')