import os
import sys
import string

tokens = ('NAME', 'NOT_EQUAL')
literals = ['=', '-', '(', ')', '+', '|', ',', r'.', r'|']
t_NAME = r'[a-zA-Z]+'

#t_ignore = r'[ \t\r\n]'

t_NOT_EQUAL = r'\!='

import ply.lex as lex
lex.lex()

vocabulary = {}
arity = {}

def p_clause(p):
    """clause : unit_clause '.'
              | non_unit_clause '.'""" 
    p[0] = p[1]

def p_non_unit_clause(p):
    """non_unit_clause : unit_clause '|' unit_clause
                       | non_unit_clause '|' unit_clause"""
    p[0] = ('OR', (p[1], p[3]))    

def p_unit_clause(p):
    """unit_clause : '-' predicate_expression
                   | predicate_expression
                   | equality_expression
                   | negated_equality_expression"""
    if p[1] == '-':
        p[0] = ('NEGATION', p[2],)
    else:
        p[0] = p[1]

def p_negated_predicate(p):
    """negated_predicate : '-' predicate_expression"""
    p[0] = ('NEGATION', p[2],)

def p_predicate_expression(p):
    "predicate_expression : NAME finished_argument_list"
    if not isinstance(p[1], tuple): vocabulary[p[1]] = 'predicate'
    arity[p[1]] = len(p[2])
    p[0] = (p[1], p[2],)

def p_equality_expression(p):
    "equality_expression : function_expression '=' function_expression"
    if not isinstance(p[1], tuple): vocabulary[p[1]] = 'function'
    if not isinstance(p[3], tuple): vocabulary[p[3]] = 'function'
    p[0] = ('EQUALS', (p[1], p[3],))

def p_negated_equality_expression(p):
    "negated_equality_expression : function_expression NOT_EQUAL function_expression"
    if not isinstance(p[1], tuple): vocabulary[p[1]] = 'function'
    if not isinstance(p[3], tuple): vocabulary[p[3]] = 'function'
    p[0] = ('NEGATION', ('EQUALS', (p[1], p[3],)))

def p_function_expression(p):
    "function_expression : NAME finished_argument_list"
    vocabulary[p[1]] = 'function'
    if not isinstance(p[1], tuple): arity[p[1]] = len(p[2])
    p[0] = (p[1], p[2],)

def p_argument_list_atomic_1(p):
    """argument_list : '(' NAME"""
    if not isinstance(p[2], tuple): vocabulary[p[2]] = 'variable'
    #print 'argument_list_atomic_1'
    p[0] = (p[2],)

def p_argument_list_atomic_2(p):
    """argument_list : '(' function_expression"""
    p[0] = (p[2],)

def p_argument_list_molecular_1(p):
    """argument_list : argument_list ',' NAME"""
    if not isinstance(p[3], tuple): vocabulary[p[3]] = 'variable'
    p[0] = p[1] + (p[3],)

def p_argument_list_molecular_2(p):
    """argument_list : argument_list ',' function_expression"""
    p[0] = p[1] + (p[3],)

def p_finished_argument_list(p):
    "finished_argument_list : argument_list ')'"
    #print 'finished_argument_list', p[1]
    p[0] = p[1]

def is_flat(l):
    sentinal = True
    for i in l:
        if isinstance(i, list): sentinal = False
    return sentinal

flatten_global = []

def inner_flatten(y):
    global flatten_global
    if isinstance(y, str):
        flatten_global.append(y)
    else:
        for i in y:
            inner_flatten(i)

import ply.yacc as yacc
yacc.yacc()

# equality not set up for atoms yet.

def canonicalize_tree(tree, vocabulary_dict):
    print 'in canonicalize_tree'

    def make_replacement_dict(d):
        function_counter = 0
        predicate_counter = 0
        variable_counter = 0
        out = {}
        for k, v in d.iteritems():
            if v == 'function':
                replacement = '<<function:'+str(function_counter)+'>>'
                function_counter += 1
            elif v == 'predicate':
                replacement = '<<predicate:'+str(predicate_counter)+'>>'
                predicate_counter += 1
            elif v == 'variable':
                replacement = '<<variable:'+str(variable_counter)+'>>'
                variable_counter += 1
            else:
                replacement = v
            out[k] = replacement
        return out
    
    replacement_dict = make_replacement_dict(vocabulary_dict)
    if not isinstance(tree, tuple) and tree in ['OR', 'NEGATION', 'CLAUSE']:
        return tree
    if not isinstance(tree, tuple):
        return replacement_dict[tree]
    return tuple((canonicalize_tree(i, replacement_dict) for i in tree))

def ladr_parser(s):
    global vocabulary
    global arity
    global flatten_global
    vocabulary = {}
    arity = {}
    d = {}
    result = yacc.parse(s)
    d['vocabulary'] = vocabulary
    d['arity'] = arity
    flatten_global = []
    inner_flatten(result)
    d['flattened'] = flatten_global
    d['tree'] = result
    d['flattened_canonicalized'] = canonicalize_tree(d['tree'], d['vocabulary'])
    return d
