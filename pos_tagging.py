# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    nnSet = set()
    nnsSet = set()

    with open("sentences.txt", "r") as f:
        for line in f:
            for pair in line.split(' '):
                (x, y) = pair.split('|')
                if (y == 'NN'):
                    nnSet.add(x)
                elif (y == 'NNS'):
                    nnsSet.add(x)

    return list(nnSet.intersection(nnsSet))


unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""

    """codes from statements.py (PART A)"""
    def match (p):
        return re.match(p + '$', s, re.IGNORECASE)

    if (s in unchanging_plurals_list):
        return s
    elif (s[-3:] == 'men'):
        return s[0:-3] + 'man'
    elif match('.*(?<!.[aeiousxyz]|sh|ch)s'):
        return s[:-1]
    elif match('.*[aeiou]ys'):
        return s[:-1]
    elif match('.*.[^aeiou]ies'):
        return s[:-3] + 'y'
    elif match('[^aeiou]ies'):
        return s[:-1]
    elif match('.*(o|x|ch|ss|zz|sh)es'):
        return s[:-2]
    elif match('.*([^s]se|[^z]ze)s'):
        return s[:-1]
    elif match('.*(?<!.[iosxz]|sh|ch)es'):
        return s[:-1]
    else:
        return ''

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""

    resultSet = {tag for (word, tag) in function_words_tags if (word == wd)}

    nS = noun_stem(wd)
    vS = verb_stem(wd)

    for x in lx.getAll('A'):
        if (x == wd):
            resultSet.add('A')

    for x in lx.getAll('P'):
        if (x == wd):
            resultSet.add('P')

    for x in lx.getAll('N'):
        if (x == nS):
            resultSet.add('Np')
        elif (x == wd):
            resultSet.add('Ns')

    for x in lx.getAll('I'):
        if (x == vS):
            resultSet.add('Ip')
        elif (x == wd):
            resultSet.add('Is')

    for x in lx.getAll('T'):
        if (x == vS):
            resultSet.add('Tp')
        elif (x == wd):
            resultSet.add('Ts')

    return list(resultSet)



def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
