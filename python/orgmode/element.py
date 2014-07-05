#!/usr/bin/env python
'''orgmode.element - Python side emulation of org-element

This module provides Python objects that attempt to adhere to the
schema that is followed by org-element as documented at:

http://orgmode.org/worg/exporters/org-element-docstrings.html

'''

from collections import namedtuple

NodeType = namedtuple("Node","type params parent body")
def Node(type, params = None, parent = None, body = None):
    '''Node - a minimal representation of high level org-element objects.

    <params> is a dictionary of org-element parameters (likely minus a
    'parent' item)

    <parent> is the node representing the org-element parent.

    <body> can be None, a string or a list of other Node objects.
    '''
    return NodeType(type, params or dict(), parent, body or list())

def nodify(data, parent = None):
    '''Produce a node hierarchy from data.

    Data is expected to be of the form of a list:

    [type, params, rest]

    <rest> can be either <data> or a string.  This is as it is when
    JSON loaded back in after being dumped with org-json.

    The parentage is implicit in the hierarchy of data.  It will be
    restored explicitly into the 'parent' parameter of a node and the
    'parent' key of the params will be removed, if it is found.
    '''
    try:
        typ = data[0]
        par = data[1]
    except IndexError:
        print 'Bad data: %s:"%s"' % (type(data), data)
        raise

    if par:
        par = dict(par)         # don't mess up caller's data
        del(par['parent'])

    if len(data) == 2:          # ain't no body
        return Node(typ, par, parent)

    if isinstance(data[2], list): # body holds more nodes
        thisnode = Node(typ, par, parent)        
        body = [nodify(x, thisnode) for x in data[2:]]
        thisnode.body.extend(body)
        return thisnode

    # body is just a simple string
    return Node(typ, par, parent, data[2])

