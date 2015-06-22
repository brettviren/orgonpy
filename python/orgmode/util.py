#!/usr/bin/env python

import json
import orgjson
import element
import datetime

def htmltree(orgfile, debug=False):
    '''
    Return tuple (html,tree) from org-mode text where <tree> is the top element.Node
    '''
    json_text = orgjson.dumpf(orgfile, debug=debug)
    dat = json.loads(json_text)
    #print json.dumps(dat,indent=2)
    node = element.nodify(dat['tree'])
    assert(node, "No node for %s" % orgfile)
    return (dat['html'], node)

def date(org_text = None):
    '''
    Convert org text to date object.
    '''
    if org_text is None:
        return datetime.date.today()

    org_text = org_text.strip()
    if org_text[0] in '[<':
        org_text = org_text[1:]
    if org_text[-1] in '>]':
        org_text = org_text[:-1]
    y,m,d = map(int, org_text.split()[0].split('-')) # super brittle
    return datetime.datetime(y,m,d)
