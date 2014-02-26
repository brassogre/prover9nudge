import os
import sys
import string

def stripWhitespace(s):
    out = ''
    for c in s:
        if not c in string.whitespace:
            out += c
    return out

def allDigits(s):
    sentinal = True
    for c in s:
        if not c in string.digits: sentinal = False
    return sentinal

def allWhitespace(s):
    sentinal = True
    for c in s:
        if not c in string.whitespace: sentinal = False
    return sentinal 
