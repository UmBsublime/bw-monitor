#!/usr/bin/env python

from chains import chains
from rules import rules, rule_set

def print_counter(rule_group):
    all_counters = {}
    all_rules = rule_group.get_rules()
    in_rules = all_rules['Input']
    out_rules = all_rules['Output']
    in_out_rules = all_rules['In_Out']

    for chain_name in rule_group.get_chain_names():
        all_counters[chain_name] = {'rules': [],
                                   'counters': rule_group.get_chain_counter(chain_name)}
        if 'in_out' in chain_name:
            all_counters[chain_name]['rules'] = in_out_rules
        elif 'in' in chain_name:
            all_counters[chain_name]['rules'] = in_rules
        elif 'out' in chain_name:
            all_counters[chain_name]['rules'] = out_rules


    from pprint import pprint
    pprint (all_counters)


def main():
    print ':) main brah'





    dicom_in = rules.Input_Rule('DICOM In',protocol= 'tcp', sport=5000)
    dicom_out = rules.Output_Rule('DICOM Out', protocol= 'tcp', dport=5000)
    http_in = rules.In_Out_Rule('HTTP In', sport=80)
    http_out = rules.In_Out_Rule('HTTP Out', dport=80)

    dicom_rules = (dicom_in, dicom_out, http_in, http_out)
    dicom_rules = {'Input': [dicom_in],
                   'Output': [dicom_out],
                   'In_Out': [http_in, http_out]}
    rule_group = rule_set.Rule_Group('TEST',dicom_rules)

    ssh = rules.In_Out_Rule('SSH',dport=22)
    #rule_group.delete_rule(ssh)
    rule_group.add_rule(ssh, )

    #rule_group.delete_rule(ssh)
    rule_group.delete_rule(http_in)
    print rule_group.get_chain_counter('TEST_in_out')
    print_counter(rule_group)

if __name__ == '__main__':
    main()
