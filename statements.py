# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)

class Lexicon:
    """stores known word stems of various part-of-speech categories"""

    def __init__(self):
        self.catDictionary = {'P':[], 'N':[], 'A':[], 'I':[], 'T':[]}

    def add(self, stem, cat):
        if (cat == 'P' or cat == 'N' or cat == 'A' or cat == 'I' or cat == 'T'):
            if (stem not in self.catDictionary[cat]):
                self.catDictionary[cat].append(stem)

        else:
            return "Error: the given tag is not valid"

    def getAll(self, cat):
        return self.catDictionary[cat]

class FactBase:
    """stores unary and binary relational facts"""

    def __init__(self):
        self.unaries = {}
        self.binaries = {}

    def addUnary(self, pred, e1):
        if (pred in self.unaries.keys()):
            self.unaries[pred].append(e1)
        else:
            self.unaries[pred] = []
            self.unaries[pred].append(e1)

    def addBinary(self, pred, e1, e2):
        if (pred in self.binaries.keys()):
            self.binaries[pred].append((e1, e2))
        else:
            self.binaries[pred] = []
            self.binaries[pred].append((e1, e2))

    def queryUnary(self, pred, e1):
        if (pred in self.unaries.keys()):
            if (e1 in self.unaries[pred]):
                return True
            else:
                return False

        else:
            return False

    def queryBinary(self, pred, e1, e2):
        if (pred in self.binaries.keys()):
            if ((e1, e2) in self.binaries[pred]):
                return True
            else:
                return False

        else:
            return False

import re
from nltk.corpus import brown

tagSetOfBrown = set(brown.tagged_words())

def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    def match(p):
        return re.match(p + '$', s, re.IGNORECASE)

    verbStem = ""

    if match('.*(?<!.[aeiousxyz]|sh|ch)s'):
        verbStem = s[:-1]
    elif match('.*([^s]se|[^z]ze)s'):
        verbStem = s[:-1]
    elif match('.*[aeiou]ys'):
        verbStem = s[:-1]
    elif match('[^aeiou]ies'):
        verbStem = s[:-1]
    elif match('.*.[^aeiou]ies'):
        verbStem = s[:-3] + 'y'
    elif match('.*(o|x|ch|ss|zz|sh)es'):
        verbStem = s[:-2]
    elif match('.*(?<!.[iosxz]|sh|ch)es'):
        verbStem = s[:-1]
    elif match('has'):
        verbStem = 'have'
    if (not (s, 'VB') in tagSetOfBrown and not (s, 'VBZ') in tagSetOfBrown):
        return ''

    return verbStem

def add_proper_name (w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")

def process_statement (lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.
