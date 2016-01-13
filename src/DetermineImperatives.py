########################
# This will tell you if a sentence is indicative, imperative, conditional, or subjunctive (indicative is default)
########################
import sys
import nltk
from nltk import tokenize
from pattern.en import parse, Sentence, parse
from pattern.en import modality
from pattern.en import mood

type_of_sent = {}
type_of_sent["indicative"] = 0
type_of_sent["imperative"] = 0
type_of_sent["conditional"] = 0
type_of_sent["subjunctive"] = 0

with open(sys.argv[1]) as f:
  for line in f:
    line = line.rstrip('\n')
    line =  line.decode('utf-8')
    sentences = tokenize.sent_tokenize(line)
    for sentence in sentences:
      #print sentence #DEBUGGING
      s = parse(sentence, lemmata=True)
      s = Sentence(s)
      #print mood(s) #DEGUGGING
      mood_type = str(mood(s))
      current = type_of_sent[mood_type]
      current = current + 1
      type_of_sent[mood_type] = current

print type_of_sent

#s = "Some amino acids tend to be acidic while others may be basic." # weaseling
#s = parse(s, lemmata=True)
#s = Sentence(s)
# 
##print modality(s) #How sure a sentence is ... not using here
#print mood(s) 
