#!/usr/bin/env python

import json
import orgjson
import element
import datetime

def htmltree(org_text):
    '''
    Return tuple (html,tree) from org-mode text where <tree> is the top element.Node
    '''
    json_text = orgjson.dumps(org_text, debug=True)
    dat = json.loads(json_text)
    return (dat['html'], element.nodify(dat['tree']))

def date(org_text):
    '''
    Convert org text to date object.
    '''
    org_text = org_text.strip()
    if org_text[0] in '[<':
        org_text = org_text[1:]
    if org_text[-1] in '>]':
        org_text = org_text[:-1]
    y,m,d = map(int, org_text.split()[0].split('-')) # super brittle
    return datetime.datetime(y,m,d)