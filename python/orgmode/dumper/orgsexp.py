#!/usr/bin/env python
'''
Dump into a sexp rep
'''

def stringify(s):
    '''
    Return weird lisp version of a string.
    '''
    return '#("%s" 0 %d (:parent "none"))' % (s, len(s))

def keyvalue(k, v):
    if k == 'title':
        return ':title (%s)' % stringify(v[0])

    if v is None or v in ['nil']:
        return ':%s nil'%k

    # Stuff not needing quoting, this really should use the schema somehow
    if k in ['level', 'begin', 'end',
             'contents-begin', 'contents-end',
             'pre-blank', 'post-blank',
             'pre-afilliated', 'post-affiliated']:
        return ':%s %s' % (k, v)

    return ':%s "%s"' % (k, v)

def params(p):
    if not p:
        return 'nil'
    body = [keyvalue(k,v) for k,v in p.items()] + [':parent "none"']
    return '(' + ' '.join(body) + ')'

def node(n):
    rest = ''
    if n.body:
        if isinstance(n.body, list):
            rest = [node(x) for x in n.body]
            rest = ' ' + ' '.join(rest)
        else:
            rest = ' ' + stringify(n.body)
    return '(%s %s%s)' % (n.type, params(n.params), rest)

