###############################################################
# My implementation of Alg. 2 from:
# "Characterizing Stylistic Elements in Syntactic Structure"
# by Feng et al. 2012. EMNLP
#
# This assumes the data is already parsed by the Berkeley parser
#
# Kenton Murray 2016
#################################################################


import codecs
import sys
import string
import nltk
from nltk.tree import ParentedTree

sentence_type = {}
sentence_type["Other"] = 0
sentence_type["Loose"] = 0
sentence_type["Periodic"] = 0


def contains_TAG(t, tag):
  try:
    t.label()
  except AttributeError:
    return
  if t.height() <= 2:
    return
  if t.label().decode('utf-8') == tag:
    #print "TAG!"  #DEBUGGING
    sbar = True
    return sbar
  else:
    for child in t:
      #print child.label().decode('utf-8'),  #DEBUGGING
      sbar = contains_TAG(child, tag)
      if sbar == True:
        return sbar
      #else:
        #Do nothing and continue
    return False


def root_level(t):

  try:
    t.label()
  except AttributeError:
    return

  #print "t.label(): ", t.label()  #DEBUGGING

  S = False
  SBAR = False

  if t.label() == "": #Berkeley parser has one more set of parens than nltk
    for child in t: # Should only be one ....
      to_return = root_level(child)
      return to_return
  elif t.label() == "S": #Root of the tree
    for child  in t:
      S = contains_TAG(child, "S")
      SBAR = contains_TAG(child, "SBAR")
      if S == True or SBAR == True:
        if child.label() != "VP":
          #print t  #DEBUGGING
          return "PERIODIC"
        else:
          return "LOOSE"


with open(sys.argv[1]) as f:
  for line in f:

    #print "====================================="  #DEBUGGING

    line = line.rstrip('\n')
    line =  line.decode('utf-8')
    parsed = ParentedTree.fromstring(line)
    #print parsed  #DEBUGGING

    s_type = root_level(parsed)
    #print s_type  #DEBUGGING

    if s_type == "LOOSE":
      current = sentence_type["Loose"]
      current = current + 1
      sentence_type["Loose"] = current
    elif s_type == "PERIODIC":
      current = sentence_type["Periodic"]
      current = current + 1
      sentence_type["Periodic"] = current
    elif s_type == None:
      current = sentence_type["Other"]
      current = current + 1
      sentence_type["Other"] = current
    #else:
    #  print "ERROR"  #DEBUGGING



print sentence_type

