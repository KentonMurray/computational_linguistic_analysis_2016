#########################################################################
# My implementation of Alg. 1 from:
# "Characterizing Stylistic Elements in Syntactic Structure"
# by Feng et al. 2012. EMNLP
#
# This assumes that the input is parse already by the Berkeley Parser
# 
# Kenton Murray 2016
##########################################################################

import codecs
import sys
import string
import nltk
from nltk.tree import ParentedTree

sentence_type = {}
sentence_type["Other"] = 0
sentence_type["Compound"] = 0
sentence_type["Complex"] = 0
sentence_type["ComplexCompound"] = 0
sentence_type["Simple"] = 0


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
  VP = False

  if t.label() == "": #Berkeley parser has one more set of parens than nltk
    for child in t: # Should only be one ....
      to_return = root_level(child)
      return to_return
  elif t.label() == "S":
    for child  in t:
      if child.label() == "S": # Is there a compound in this sentence
        S = True
    if S == True:
      sbar = contains_TAG(t, "SBAR") # Check the whole tree for SBAR (not just under S)
      return ("S", sbar)
    else:  # S wasn't there, now check top level for VP
      for child in t:
        if child.label() == "VP":
          VP = True
      if VP == True:
        sbar = contains_TAG(t, "SBAR") # Check the whole tree for SBAR (not just under VP)
        return ("VP", sbar)


#        for grandchild in child:
#          sbar = contains_TAG(grandchild, "SBAR")
#          if sbar == True:
#            return ("S", True)
#          #else:
#          #  return ("S", False)
#        return ("S", False)
#      elif child.label() == "VP":
#        for grandchild in child:
#          sbar = contains_TAG(grandchild, "SBAR")
#          if sbar == True:
#            return ("VP", True)
#          #else:
#          #  return ("VP", False)
#        return ("VP", False)
#
#
#      to_return = top_structure_level(child)
#      return to_return
#  else:
#    return



def top_structure_level(t):

  try:
    t.label()
  except AttributeError:
    return

  print "t.label(): ", t.label()

  #if t.label() == "": #Berkeley parser has one more set of parens than nltk
  #  for child in t:
  #    to_return = top_structure_level(child)
  #    return to_return
  if t.label() == "S":
    #print t.contains("SBAR")
    for child in t:
      #print child.label(),
      sbar = contains_TAG(child, "SBAR")
      if sbar == True:
        return ("S", True)
      #else:
      #  return ("S", False)
    return ("S", False)
    #print "kenton"
  elif t.label() == "VP":
    for child in t:
      sbar = contains_TAG(child, "SBAR")
      if sbar == True:
        return ("VP", True)
      #else:
      #  return ("VP", False)
    return ("VP", False)



with open(sys.argv[1]) as f:
  for line in f:

    #print "====================================="  #DEBUGGING

    line = line.rstrip('\n')
    line =  line.decode('utf-8')
    parsed = ParentedTree.fromstring(line)
    #print parsed  #DEBUGGING

    sbar = ("", False)
    sbar = root_level(parsed)
    #print sbar  #DEBUGGING

    if sbar == None:
      current = sentence_type["Other"]
      current = current + 1
      sentence_type["Other"] = current
      #print "Other"  #DEBUGGING
    elif sbar == ('S', True):
      current = sentence_type["ComplexCompound"]
      current = current + 1
      sentence_type["ComplexCompound"] = current
      #print "ComplexCompound"  #DEBUGGING
    elif sbar == ('VP', True):
      current = sentence_type["Complex"]
      current = current + 1
      sentence_type["Complex"] = current
      #print "Complex"  #DEBUGGING
    elif sbar == ('S', False):
      current = sentence_type["Compound"]
      current = current + 1
      sentence_type["Compound"] = current
      #print "Compound"  #DEBUGGING
    elif sbar == ('VP', False):
      current = sentence_type["Simple"]
      current = current + 1
      sentence_type["Simple"] = current
      #print "Simple"  #DEBUGGING
    else:
      print "ERROR"



print sentence_type
