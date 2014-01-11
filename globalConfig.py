import os
import sys
import string
import MySQLdb

BASE_DIRECTORY = '/home/zac/projects/hintomatic/'
TMP_DIRECTORY = '/tmp/'

EMAIL_ACCOUNT = 'hintomatic@gmail.com'
SMTP_SERVER = 'smtp.gmail.com'
EMAIL_PASSWORD ='*********'
IMAP_SERVER = 'imap.gmail.com'
MYSQL_DATABASE = 'autoprove'
MYSQL_USER = '**********'
MYSQL_PASSWORD = '*********'

TEST_DIRECTORY = BASE_DIRECTORY + 'test_files/'
TEST_INPUT_FILE = TEST_DIRECTORY + './prop.in'

SOS_START = 'formulas(sos)'
USABLE_START = 'formulas(usable)'
GOALS_START = 'formulas(goals)'
END_OF_LIST = 'end_of_list'
COMMENT_MARKER = '%'
END_OF_STATEMENT = '.'
DISJUNCTION = '|'
SOS = 'sos'
USABLE = 'usable'
GOALS = 'goals'
SEARCH_STRING = '==== SEARCH ===='
BUILT_IN_FUNCTIONS = ['+', '*', '-', '/', '^', '@', '~', '=']
JUNK_SYMBOL = ':'
PROOF_START = '===== PROOF ====='
PROOF_END = '==== end of proof ===='
PARENTHESES = ['(', ')']

LYNX_COMMAND = '/usr/bin/lynx'
LYNX_DUMP_OPTION = '-dump'
LYNX_STDIN_OPTION = '-stdin'
LYNX_INPUT_FILE = TMP_DIRECTORY + 'lynx_input.html'

def getConnection():
  global MYSQL_USER
  global MYSQL_PASSWORD
  global MYSQL_DATABASE
  db = MySQLdb.connect(user = MYSQL_USER, passwd = MYSQL_PASSWORD, db = MYSQL_DATABASE)
  cursor = db.cursor()
  return cursor

# we're not ready for this quite yet...
# CURSOR = getConnection()

