"""This class does nothing except keep all global configuration options. It is
   imported by (I think) every module."""

import mysql.connector

BASE_DIRECTORY = '/home/zac/projects/hintomatic/'
""":ivar BASE_DIRECTORY: Where the hintomatic project lives"""
TMP_DIRECTORY = '/tmp/'
""":ivar TMP_DIRECTORY: Where temporary files will be created and destroyed"""
EMAIL_ACCOUNT = 'hintomatic@gmail.com'
""":ivar EMAIL_ACCOUNT: The hintomatic email address to which users will
                     submit input and output files"""
SMTP_SERVER = 'smtp.gmail.com'
""":ivar SMTP_SERVER: Server for hintomatic email account (gmail)"""
EMAIL_PASSWORD = '*********'
""":ivar EMAIL_PASSWORD: Password for hintomatic email account"""
IMAP_SERVER = 'imap.gmail.com'
""":ivar IMAP_SERVER: The address for hintomatic's email account's IMAP"""
MYSQL_DATABASE = 'prover9nudge'
""":ivar MYSQL_DATABASE: Name of database for storing proofs, clauses, etc."""
MYSQL_USER = 'zac'
""":ivar MYSQL_USER: User authorized for access to MYSQL"""
MYSQL_PASSWORD = '***************'
""":ivar MYSQL_PASSWORD: That user's password"""
MYSQL_PROOFS_TABLE = 'proofs'
""":ivar MYSQL_PROOFS_TABLE: Name of table holding proofs"""

MYSQL_RAW_PROOF_COLUMN = 'rawproof'
MYSQL_PARSED_PROOF_COLUMN = 'clauselist'
MYSQL_PROOF_HASH = 'rawproofhash'

TEST_DIRECTORY = BASE_DIRECTORY + 'test_files/'
""":ivar TEST_DIRECTORY: Where sample input and output files are kept"""
TEST_INPUT_FILE = TEST_DIRECTORY + './prop.in'
""":ivar TEST_INPUT_FILE: Relative pathname to a sample input file for testing"""
ASSUMPTIONS_START = 'formulas(assumptions)'
""":ivar ASSUMPTIONS_START: String that marks the beginning of an assumptions
                            list in a Prover9 input file"""
SOS_START = 'formulas(sos)'
""":ivar SOS_START: String that marks the beginning of the SOS list in a
                 Prover9 file"""
USABLE_START = 'formulas(usable)'
""":ivar USABLE_START: String marking the beginning of the USABLE list in
                 a Prover9 file"""
GOALS_START = 'formulas(goals)'
""":ivar GOALS_START: Marks the beginning of the GOALS list in a Prover9 file"""
END_OF_LIST = 'end_of_list'
""":ivar END_OF_LIST: String used to end any list in a Prover9 file"""
COMMENT_MARKER = '%'
""":ivar COMMENT_MARKER: Anything following this character is a comment for Prover9"""
END_OF_STATEMENT = '.'
""":ivar END_OF_STATEMENT: Delimiter marking the end of any Prover9 statement"""
DISJUNCTION = '|'
""":ivar DISJUNCTION: Separator for unit clauses in a disjunction"""
SOS = 'sos'
""":ivar SOS: Name of SOS list"""
USABLE = 'usable'
""":ivar USABLE: Name of Usable list"""
ASSUMPTIONS = 'assumptions'
""":ivar ASSUMPTIONS:: Name of assumptions list"""
GOALS = 'goals'
""":ivar GOALS: Name of goals list"""
SEARCH_STRING = '==== SEARCH ===='
BUILT_IN_FUNCTIONS = ['+', '*', '-', '/', '^', '@', '~', '=']
JUNK_SYMBOL = ':'
""":ivar SEARCH_STRING: Marks the beginning of the search phase for Prover9"""
PROOF_START = '===== PROOF ====='
""":ivar PROOF_START: String that marks the beginning of a proof in a Prover9
                   output file"""
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
    db = mysql.connector.connect(user=MYSQL_USER, passwd=MYSQL_PASSWORD, db=MYSQL_DATABASE)
    cursor = db.cursor()
    return cursor

#  we're not ready for this quite yet...
#  CURSOR = getConnection()

