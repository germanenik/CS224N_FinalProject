# import nltk import TweetTokenizer

f = open('pipeline8/clean4.complex')
fout = open('pipeline8/clean4.complex.sent', 'w+')

for line in f:
    sent_text = line.split('.')
    for sent in sent_text:
        if not sent.strip().isspace() and not sent.strip() == '':
            fout.write(f'{sent.strip()}\n')
