#!/usr/bin/env python

import common

from orgmode.element import nodify

def test_nodify():
    d = common.sample_org_json_data()
    assert len(d) >= 3

    n = nodify(d)
    assert (n)
    

if '__main__' == __name__:
    test_nodify()

