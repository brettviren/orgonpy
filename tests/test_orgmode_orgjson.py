#!/usr/bin/env python
import common
from orgmode import orgjson

def test_convert_json():
    orgstring = common.sample_org_data()
    json_want = common.sample_org_json_data()
    json_string_got = orgjson.dumps(orgstring, 'simple.org')
    json_got = common.json.loads(json_string_got)

    s1= common.json.dumps(json_got['tree'],indent=2)
    s2= common.json.dumps(json_want, indent=2)
    print s1
    print s2
    #open('s1.txt','w').write(s1)
    #open('s2.txt','w').write(s2)
    # not exact: diff s1.txt s2.txt

if '__main__' == __name__:
    test_convert_json()
