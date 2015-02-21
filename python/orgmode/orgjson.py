#!/usr/bin/env python
'''Support code for using JSON files written by org-json.

This module provides Python objects that attempt to adhere to the
schema that is followed by org-element as documented at:

http://orgmode.org/worg/exporters/org-element-docstrings.html

This module provides an expression of this schema.

'''

import os
import shutil
import tempfile
import subprocess

def dumps(orgstring, temporg='orgjson.org', debug = False):
    '''
    Return JSON string representing org-element tree made from <orgstring>.
    '''
    tmpdir = tempfile.mkdtemp()

    el_fname = os.path.join(os.path.dirname(__file__), 'orgjson.el')
    org_fname = os.path.join(tmpdir, temporg)
    json_fname = os.path.join(tmpdir, 'orgjson.json')

    open(org_fname,'w').write(orgstring)

    # fixme: make independent from user env?
    cmd = ['/usr/bin/emacs','--batch','-l',el_fname,'--eval']
    cmd += ["(org2jsonfile \"%s\" \"%s\")" % (org_fname, json_fname)]
    stderr = subprocess.STDOUT
    if debug:
        print ('Running: %s' % ' '.join(cmd))
        stderr = None
    subprocess.check_output(cmd, stderr=stderr)
    json_string = open(json_fname).read()
    shutil.rmtree(tmpdir)
    return json_string




