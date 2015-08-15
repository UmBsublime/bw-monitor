#!/usr/bin/env python

import logging
import datetime
import sys

from pprint import pprint
from time import sleep
from os import path, makedirs

from core import rules, counters, config_parser

USER = 'cvaillancourt'
LOG_PATH = '/home/{}/log/{}.log'.format(USER, path.basename(__file__))

def setup_logging():

    fpath, fname = path.split(LOG_PATH)
    if not path.isdir(fpath):
        ans = raw_input('\nFolder {} doesn\'t exist.'
                        'Would you like to create it? [y/n] '.format(fpath))
        if ('y' in ans) or ('Y' in ans):
            makedirs(fpath)
        else:
            print ('Program can not continue')
            exit(1)

    logging.basicConfig(filename=LOG_PATH,
                        level=logging.DEBUG,
                        format='[%(asctime)s][%(levelname)s] %(message)s')


def main():

    print ':) main brah'
    setup_logging()

    test_rule_config = config_parser.parse_file(sys.argv[1])

    test_rules = []
    for r in test_rule_config:
        d_chain = r.pop('chain', None)
        if d_chain == 'in':
            t = rules.InputRule(**r)
        if d_chain == 'out':
            t = rules.OutputRule(**r)

        test_rules.append(t)

    test_counter = counters.Counter('TEST', test_rules)

    counter = 0
    while True:
        counter += 1

        print 'Loop #: ' + str(counter)
        print datetime.datetime.now()
        print '*'*80

        for k,v in test_counter.get_counters(False).items():
            if len(v) > 0:
                for c in v:

                    logging.info('{}, {}: {}'.format(k, c['name'],c['bytes']))
                    print '{}, {}: {}'.format(k, c['name'],c['bytes'])

        print '*'*80
        sleep(60)



    #logging.info()
if __name__ == '__main__':
    main()
