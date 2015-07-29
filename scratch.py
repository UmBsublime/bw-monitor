#! /usr/bin/env python

from core import chains, rules, counters
from pprint import pprint
from time import sleep

dicom_in = rules.InputRule('DICOM In', protocol='tcp', sport=5000)
dicom_out = rules.OutputRule('DICOM Out', protocol='tcp', dport=5000)
http_in = rules.InOutRule('HTTP In', sport=80)


ssh = rules.InOutRule('SSH', sport=22)
test = counters.Counter('test', [dicom_in, dicom_out, http_in])
test.add_rule(ssh)
pprint(test.get_counters())
#test.remove_rule(ssh)
test.reset_counters()
#pprint(test.get_counters())
#test.flush_rules()
#pprint(test.get_counters())
#sleep(2)
#print(test.get_counters())

test.delete()
