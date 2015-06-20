#!/usr/bin/env python
'''Support code for using JSON files written by org-json.

This module provides Python objects that attempt to adhere to the
schema that is followed by org-element as documented at:

http://orgmode.org/worg/exporters/org-element-docstrings.html

This module provides an expression of this schema.

'''

import os
import sys
import shutil
import tempfile
import subprocess

def dumpf(orgfile, debug = False):
    '''Return the JSON string representing org-element tree made from the
    contenst of the Org file.
    '''
    orgfile = os.path.realpath(orgfile)
    orgdir = os.path.dirname(orgfile)

    el_fname = os.path.join(os.path.dirname(__file__), 'orgjson.el')
    _, json_fname = tempfile.mkstemp('.json',prefix='orgjson')

    sys.stderr.write('Dumping file: %s\n' % orgfile)
    sys.stderr.write('To: %s\n' % str(json_fname))

    # fixme: make independent from user env?
    cmd = ['/usr/bin/emacs','-Q','--batch','-l',el_fname,'--eval']
    cmd += ["(org2jsonfile \"%s\" \"%s\")" % (orgfile, json_fname)]
    stderr = subprocess.STDOUT
    if debug:
        sys.stderr.write('Running emacs command in %s:\n%s\n' % (orgdir, ' '.join(cmd)))
        stderr = None
    subprocess.check_output(cmd, stderr=stderr, cwd=orgdir)
    json_string = open(json_fname).read()
    print 'Not removing temporary json file:\n%s' % json_fname
    return json_string


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
    #shutil.rmtree(tmpdir)
    print 'Not removing working directory:\n%s' % tmpdir
    return json_string




