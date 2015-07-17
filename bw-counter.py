#!/usr/bin/env python

from chains import chains
from rules import rules, rule_set


def main():
    print ':) main brah'

    dicom_in = rules.Input_Rule('DICOM In',protocol= 'tcp', sport=5000)
    dicom_out = rules.Output_Rule('DICOM Out', protocol= 'tcp', dport=5000)
    http_in = rules.In_Out_Rule('HTTP In', sport=80)
    http_out = rules.In_Out_Rule('HTTP Out', dport=80)

    dicom_rules = (dicom_in, dicom_out, http_in, http_out)

    rule_group = rule_set.Rule_Group('TEST',dicom_rules)

    ssh = rules.In_Out_Rule('SSH',dport=22)
    rule_group.add_rule(ssh, 'TEST_in_out')

if __name__ == '__main__':
    main()
