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

    def __init__(self, name, input_rules=(), output_rules=(), in_out_rules=()):

        self.name = name
        self.name_in = name + '_in'
        self.name_out = name + '_out'
        self.name_in_out = name + '_in_out'
        self.input_rules = list(input_rules)
        self.output_rules = list(output_rules)
        self.in_out_rules = list(in_out_rules)

        self.chains = []
        self._create_group()

    def _create_group(self):

        if len(self.output_rules) > 0:
            chains.create_chain(self.name_out)
            rules.redirect_chain1_to_chain2('OUTPUT', self.name_out)
            self.chains.append(self.name_out)

            for r in self.output_rules:
                r.add_to_chain(self.name_out)

        if len(self.input_rules) > 0:
            chains.create_chain(self.name_in)
            rules.redirect_chain1_to_chain2('INPUT', self.name_in)
            self.chains.append(self.name_in)

            for r in self.input_rules:
                r.add_to_chain(self.name_in)

        if len(self.in_out_rules) > 0:
            chains.create_chain(self.name_in_out)
            rules.redirect_chain1_to_chain2('OUTPUT', self.name_in_out)
            rules.redirect_chain1_to_chain2('INPUT', self.name_in_out)
            self.chains.append(self.name_in_out)

            for r in self.in_out_rules:
                r.add_to_chain(self.name_in_out)

    def add_rule(self, rule, chain):
        rule.add_to_chain(chain)

    def delete_rule(self, rule, chain):
        return

    def get_rules(self):
        return

    def clear_chain(self):
        return

    def clear_all(self):
        return

    def reset_chain_counters(self):
        return

    def reset_all_counters(self):
        return

    def get_chain_counter(self, chain):
        return

    def get_chain_counters(self):
        return

