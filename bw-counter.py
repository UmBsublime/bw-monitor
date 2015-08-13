#!/usr/bin/env python

from core import chains, rules, counters, config_parser

def main():
    from pprint import pprint
    from time import sleep

    print ':) main brah'

    dicom_rule_config = config_parser.parse_file('config/dicom.ini')

    dicom_rules = []
    for r in dicom_rule_config:
        d_chain = r.pop('chain', None)
        if d_chain == 'in':
            t = rules.InputRule(**r)
        if d_chain == 'out':
            t = rules.OutputRule(**r)

        dicom_rules.append(t)

    dicom_counter = counters.Counter('TEST',dicom_rules)

    counter = 0
    while True:
        counter += 1
        print 'Loop #: ' + str(counter)
        print '*'*80
        pprint(dicom_counter.get_counters())
        print '*'*80
        sleep(5)

if __name__ == '__main__':
    main()
