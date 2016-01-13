import codecs
import sys
import string
import nltk.data

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

data = ""
with open(sys.argv[1]) as f:
  for line in f:
    line = line.rstrip('\n')
    data = data + " " + line

unicode_string = data.decode('utf-8')
final =  '\n'.join(tokenizer.tokenize(unicode_string))
print final.encode('utf-8')
