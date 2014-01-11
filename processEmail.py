import os
import sys
import string
import math
import hashlib
from dateutil import parser
import emailInterface
import sqlInterface
import globalConfig as gc

def extractEmailAddress(s):
    tokens = s.split()
    emailAddress = tokens[-1]
    emailAddress = emailAddress.replace('<', '')
    emailAddress = emailAddress.replace('>', '')
    return emailAddress

def extractDate(s):
    theDate = parser.parse(s)
    year = str(theDate.year)
    month = str(theDate.month)
    day = str(theDate.day)
    out = '-'.join([year, month, day])
    return out

def insertEmail():
    unseenEmail = emailInterface.getUnseenEmails()
    for mail in unseenEmail:
        sender = extractEmailAddress(mail['From'])
        theDate = extractDate(mail['Date'])
        subject = mail['Subject']
        longestText = emailInterface.getLongestTextPart(mail)
        emailHash = hashlib.md5(longestText).hexdigest()
        d = {}
        d['sender'] = sender
        d['date'] = theDate
        d['subject'] = subject
        d['message'] = longestText
        d['hash'] = emailHash
        print 'inserting:', emailHash
        sqlInterface.insertDict('email', d, ['subject', 'message'])