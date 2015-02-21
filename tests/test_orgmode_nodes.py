#!/usr/bin/env python

import common
from orgmode import util
from orgmode.element import dump

def test_nodes():
    org_text = common.sample_org_data('blog.org')
    html, top = util.htmltree(org_text)
    dump(top)

    first = top[0]

    for n in 'title author date category slug'.split():
        v = first.get(n, "(dne)")
        if n == 'date':
            v = util.date(v)
        print ('\t%s = %s' % (n, v))

    print html

if '__main__' == __name__:
    test_nodes()

