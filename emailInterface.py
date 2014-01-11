import os
import sys
import math
import string
import smtplib
import imaplib
import globalConfig as gc
from email.mime.text import MIMEText
import email

def sendEmail(recipient, payload):
  session = smtplib.SMTP(gc.SMTP_SERVER)
  session.starttls()
  session.login(gc.EMAIL_ACCOUNT, gc.EMAIL_PASSWORD)
  session.sendmail(gc.EMAIL_ACCOUNT, recipient, payload.as_string())
  return 1

def composeEmail(message = '', sender = '', recipient = '', subject = ''):
  msg = MIMEText(message)
  msg['Subject'] = subject
  msg['From'] = sender
  msg['To'] = recipient
  return msg

def getUnseenEmails():
  allEmails = []
  mail = imaplib.IMAP4_SSL(gc.IMAP_SERVER)
  mail.login(gc.EMAIL_ACCOUNT, gc.EMAIL_PASSWORD)
  mail.select('inbox')
  result, data = mail.search(None, '(UNSEEN)')
  idList = data[0].split()
  for emailID in idList:
    result, data = mail.fetch(emailID, '(RFC822)')
    #print '---------------------------------'
    structuredEmail = email.message_from_string(data[0][1])
    allEmails.append(structuredEmail)
    for part in structuredEmail.walk():
      messagePartType = part.get_content_type()
      #print messagePartType
  return allEmails

def getTextParts(e):
  """Returns a list of all the text/plain components"""
  textParts = []
  for part in e.walk():
    messagePartType = part.get_content_type()
    #print 'messageType', messagePartType
    if messagePartType == 'text/plain':
      #print part
      textParts.append(part.get_payload())
  return textParts

def getLongestTextPart(e):
    textParts = getTextParts(e)
    longest = ''
    for textPart in textParts:
        if len(textPart) >= len(longest):
            longest = textPart
    return longest
  
def getUnseenText():
  print 'in getUnseenText...'
  unseenEmail = getUnseenEmails()
  print unseenEmail
  textParts = []
  for e in unseenEmail:
    textFromOneEmail = getTextParts(e)
    textParts += textFromOneEmail
  return textParts