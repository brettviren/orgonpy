#!/usr/bin/env python

import common

from orgmode.element import nodify
from orgmode.dumper import orgsexp

def test_node():
    d = common.sample_org_json_data()
    assert len(d) >= 3
    n = nodify(d)
    text = orgsexp.node(n)
    print text


if '__main__' == __name__:
    test_node()

