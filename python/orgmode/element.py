#!/usr/bin/env python
'''orgmode.element - Python side emulation of org-element

This module provides Python objects that attempt to adhere to the
schema that is followed by org-element as documented at:

http://orgmode.org/worg/exporters/org-element-docstrings.html

'''

class Node(object):
    '''Node - a minimal representation of high level org-element objects.

    <params> is a dictionary of org-element parameters (likely minus a
    'parent' item)

    <parent> is the node representing the org-element parent.

    <body> can be None, a string or a list of other Node objects.
    '''
    def __init__(self, type, params=None, parent=None, body=None):
        self.type = type
        self.params = params or dict()
        self.parent = parent
        self.body = body or list()

    def __str__(self):
        p = None
        if self.parent:
            p = id(self.parent)
        keys = ','.join(sorted(self.keys()))
        return '<Node:%s [%s] (parent:%s) (%d children) keys:{%s}>' % \
            (id(self), self.type, p, len(self.body), keys)

    def __getattr__(self, name):
        if self.istext():
            raise KeyError('No such keyword "%s"' % name) # node body isn't a list
        for child in self.body:
            if child.type != 'keyword':
                continue
            if child.params['key'].lower() == name.lower():
                return child.params['value']
        raise KeyError('No such keyword "%s"' % name)

    def get(self, name, default=None):
        'Return a keyword value by name or default.'
        try:
            return self[name]
        except KeyError:
            return default

    def keys(self):
        'Return list of keyword node keys which may exist as direct children.'
        if self.istext():
            return []
        ret = list()
        for child in self.body:
            if child.type != 'keyword':
                continue
            ret.append(child.params['key'].lower())
        return ret
            
    def __getitem__(self, index):
        'Return child at <index>.  Will return a character if body is text'
        if type(index) == int:
            return self.body[index]
        return self.__getattr__(index) # is this evil?

    def istext(self):
        'Return True if body is text'
        return type(self.body) != type([])
        

    pass

def dump(node, depth=0, tab='  '):
    print '%s%s' % (tab*depth, node)
    if node.istext():
        print'%s<Text:%s...>' % (tab*depth, node.body[:20].strip())
    else:
        for child in node.body:
            dump(child, depth+1)



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

