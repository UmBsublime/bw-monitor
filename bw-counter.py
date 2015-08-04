#!/usr/bin/env python

from core import chains, rules, counters

def main():
    from pprint import pprint
    from time import sleep

    print ':) main brah'

    dicom_in = rules.InputRule('DICOM In',protocol= 'tcp', sport=5000)
    dicom_out = rules.OutputRule('DICOM Out', protocol= 'tcp', dport=5000)
    http_in = rules.InOutRule('HTTP In', sport=80)
    http_out = rules.InOutRule('HTTP Out', dport=80)

    dicom_rules = [dicom_in, dicom_out, http_out, http_in]
    dicom_counter = counters.Counter('TEST',dicom_rules)

    ssh = rules.InOutRule('SSH',dport=22)
    dicom_counter.add_rule(ssh)

    while True:
        pprint(dicom_counter.get_counters())
        sleep(5)



if __name__ == '__main__':
    main()
