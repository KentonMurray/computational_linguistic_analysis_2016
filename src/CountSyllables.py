import sys
import string
import nltk
from nltk.corpus import cmudict

d = cmudict.dict()
num_syllables = 0
track_syllables = {}
track_syllables[1] = 0
track_syllables[2] = 0
track_syllables[3] = 0
track_syllables[4] = 0
track_syllables[5] = 0
track_syllables[6] = 0
track_syllables[7] = 0
track_syllables[-1] = 0
with open(sys.argv[1]) as f:
  for line in f:
    line = line.rstrip('\n')
    line =  line.decode('utf-8')
    line = line.replace("-"," ") # Lot's of hyphenated words are not in the dictionary ... some should be one, some two ... splitting the diff :/ not ideal
    words = line.split(' ')
    for word in words:
      #no_punct = "".join(l for l in word if l not in string.punctuation) #Need apostrophes ... dict recognizes don't but not dont
      no_punct = "".join(l for l in word if l not in ('!','.',':','?','(',')',',','#','$','"'))
      if no_punct.lower() not in d:  #Not all words will be in the dictionary ... this includes numbers
        #print "WORD NOT IN PRONUNCIATION DICTIONARY: ", no_punct #DEBUGGING
        current = track_syllables[-1]
        current = current + 1
        track_syllables[-1] = current
        continue
      num_syllables = [len(list(y for y in x if y[-1].isdigit())) for x in d[no_punct.lower()]][0] #basically, there is number for each new syllable
      #print no_punct, " ", num_syllables #DEBUGGING
      if num_syllables in track_syllables:
        current = track_syllables[num_syllables]
        current = current + 1
        track_syllables[num_syllables] = current

print track_syllables
