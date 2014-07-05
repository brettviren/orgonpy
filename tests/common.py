#!/usr/bin/env python

import os
import sys
import json

testdir = os.path.dirname(os.path.realpath(__file__))
srcdir =  os.path.dirname(testdir)

sys.path.insert(0,os.path.join(srcdir, 'python'))


def sample_org_json_data(filename = 'simple.json'):
    return json.loads(open(os.path.join(testdir, "samples/simple.json")).read())

