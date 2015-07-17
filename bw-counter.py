#!/usr/bin/env python

from chains import chains
from rules import rules, rule_set


def main():
    print ':) main brah'
    #chain_name = 'COUNTERS'
    #chains.create_chain(chain_name)
    #print chains.get_chain_counters(chain_name)
    #chains.reset_chain_counters(chain_name)
    #print chains.get_chain_counters(chain_name)
    #chains.flush_chain_rules(chain_name)
    #chains.remove_chain(chain_name)
    #rules.print_rules(chain_name)

    #if rules.dst_tcp_port_rule(chain_name, '80'):
    #    print 'creating new rule'
    #if rules.src_tcp_port_rule(chain_name, '80'):
    #    print 'creating new rule'
    #if rules.dst_ip_rule(chain_name, '8.8.8.8'):
    #    print 'creating new rule'
    #if rules.src_ip_rule(chain_name, '8.8.8.8'):
    #    print 'creating new rule'
    #if rules.src_ip_rule(chain_name, '192.168.0.0/24'):
    #    print 'creating new rule'
    #if rules.dst_ip_rule(chain_name, '10.93.12.0/255.255.255.0'):
    #    print 'creating new rule'
    #rules.redirect_chain1_to_chain2('OUTPUT', chain_name)
    #rules.redirect_chain1_to_chain2('INPUT', chain_name)


    dicom_in = rules.Rule(protocol= 'tcp', sport=5000)
    dicom_out = rules.Rule(protocol= 'tcp', dport=5000)

    http = rules.Rule(dport=80, sport=80)
    ssh = rules.Rule(dport=22)

    rule_group = rule_set.Rule_Group('TEST',(dicom_in,), (dicom_out,), (http,))

    rule_group.add_rule(ssh, 'TEST_in_out')
    #all_chains = rule_set.create_rule_set('TEST', (22,80,443), (22,80,443),('192.168.1.0/24',),('192.168.1.0/24',))
    #for i in all_chains:
    #    rules.print_rules(i)
if __name__ == '__main__':
    main()