from chains import chains
import rules

def create_rule_set(name, dst_port_list=(), src_port_list=(), dst_addr_list=(), src_addr_list=()):
    all_chains = []
    if len(dst_addr_list) > 0:
        chain_name = name + '_out'
        all_chains.append(chain_name)
        chains.create_chain(chain_name)
        rules.redirect_chain1_to_chain2('OUTPUT', chain_name)

        for ip in dst_addr_list:
            rules.dst_ip_rule(chain_name, ip)

    if len(src_addr_list) > 0:
        chain_name = name + '_in'
        all_chains.append(chain_name)
        chains.create_chain(chain_name)
        rules.redirect_chain1_to_chain2('INPUT', chain_name)

        for ip in src_addr_list:
            rules.src_ip_rule(chain_name, ip)

    if len(dst_port_list) > 0 or len(src_port_list) > 0:
        chain_name = name + '_port'
        all_chains.append(chain_name)
        chains.create_chain(chain_name)
        rules.redirect_chain1_to_chain2('OUTPUT', chain_name)
        rules.redirect_chain1_to_chain2('INPUT', chain_name)

        if len(dst_port_list) > 0:
            for port in dst_port_list:
                rules.dst_tcp_port_rule(chain_name, port)
        if len(src_port_list) > 0:
            for port in src_port_list:
                rules.src_tcp_port_rule(chain_name, port)
    return all_chains


input_rules = []
output_rules = []
in_out_rules = []

class Rule_Group(object):

    def __init__(self, name, group_rules=None):

        self.name = name
        self.name_in = name + '_in'
        self.name_out = name + '_out'
        self.name_in_out = name + '_in_out'
        self.group_rules = group_rules

        self.chains = []
        self._create_group()

    def _create_group(self):
        for rule in self.group_rules['Output']:
            chains.create_chain(self.name_out)
            rules.redirect_chain1_to_chain2('OUTPUT', self.name_out)
            self.chains.append(self.name_out)
            rule.add_to_chain(self.name_out)

        for rule in self.group_rules['Input']:
            chains.create_chain(self.name_in)
            rules.redirect_chain1_to_chain2('INPUT', self.name_in)
            self.chains.append(self.name_in)
            rule.add_to_chain(self.name_in)

        for rule in self.group_rules['In_Out']:
            chains.create_chain(self.name_in_out)
            rules.redirect_chain1_to_chain2('OUTPUT', self.name_in_out)
            rules.redirect_chain1_to_chain2('INPUT', self.name_in_out)
            self.chains.append(self.name_in_out)
            rule.add_to_chain(self.name_in_out)

    def add_rule(self, rule):
        from pprint import pprint
        print '* ADDING* ' + str(rule)
        print '*BEFORE*'
        pprint (self.group_rules)
        if type(rule) is rules.Input_Rule:
            self.group_rules['Input'].append(rule)
            rule.add_to_chain(self.name_in)
        if type(rule) is rules.Output_Rule:
            self.group_rules['Output'].append(rule)
            rule.add_to_chain(self.name_in_out)
        if type(rule) is rules.In_Out_Rule:
            self.group_rules['In_Out'].append(rule)
            rule.add_to_chain(self.name_in_out)

        print '*AFTER*'
        pprint (self.group_rules)
    def delete_rule(self, rule):
        from pprint import pprint
        print '* DELETING* ' + str(rule)
        print '*BEFORE*'
        pprint (self.group_rules)
        if rule.remove_from_chain(self.name_in):
            self.group_rules['Input'].remove(rule)
            rule.remove_from_chain(self.name_in)
        if rule.remove_from_chain(self.name_out):
            self.group_rules['Output'].remove(rule)
            rule.remove_from_chain(self.name_out)
        if rule.remove_from_chain(self.name_in_out):
            self.group_rules['In_Out'].remove(rule)
            rule.remove_from_chain(self.name_in_out)
        print '*AFTER*'
        pprint (self.group_rules)

    def get_rules(self):
        return self.group_rules

    def clear_chain(self, chain_name):
        if chain_name in self.chains:
            chains.flush_chain_rules(chain_name)

    def clear_all(self):
        for c in self.chains:
            self.clear_chain(c)

    def reset_chain_counters(self, chain_name):
        if chain_name in self.chains:
            chains.reset_chain_counters(chain_name)

    def reset_all_counters(self):
        for c in self.chains:
            chains.reset_chain_counters(c)

    def get_chain_counter(self, chain_name):
        if chain_name in self.chains:
            return chains.get_chain_counters(chain_name)

    def get_chain_counters(self):
        return

    def get_chain_names(self):
        return self.chains
