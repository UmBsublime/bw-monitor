import iptc

from chains.chains import  get_chain_counters

table = iptc.Table(iptc.Table.FILTER)

def test_rule_exists(chain_name, rule):
    for chain in table.chains:
        if chain_name == chain.name:
            for r in chain.rules:
                if r == rule:
                    return True
    return False

def redirect_chain1_to_chain2(chain1, chain2):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain1)
    rule = iptc.Rule()
    target = iptc.Target(rule, chain2)
    rule.target = target
    if not test_rule_exists(chain1, rule):
        chain.insert_rule(rule)
        return True
    return False


def dst_tcp_port_rule(chain_name, port):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
    rule = iptc.Rule()
    rule.protocol = 'tcp'
    match = rule.create_match('tcp')
    match.dport = str(port)
    rule.target = iptc.Target(rule, '')
    if not test_rule_exists(chain_name, rule):
        chain.insert_rule(rule)
        return True
    return False


def src_tcp_port_rule(chain_name, port):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
    rule = iptc.Rule()
    rule.protocol = 'tcp'
    match = rule.create_match('tcp')
    match.sport = str(port)
    rule.target = iptc.Target(rule, '')
    if not test_rule_exists(chain_name, rule):
        chain.insert_rule(rule)
        return True
    return False


def dst_ip_rule(chain_name, ip):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
    rule = iptc.Rule()
    rule.protocol = 'tcp'
    rule.dst = ip
    rule.target = iptc.Target(rule, '')
    if not test_rule_exists(chain_name, rule):
        chain.insert_rule(rule)
        return True
    return False


def src_ip_rule(chain_name, ip):
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
    rule = iptc.Rule()
    rule.protocol = 'tcp'
    rule.src = ip
    rule.target = iptc.Target(rule, '')
    if not test_rule_exists(chain_name, rule):
        chain.insert_rule(rule)
        return True
    return False

IN_SRC_RULE = 'in_src_rule'
OUT_SRC_RULE = 'out_src_rule'
IN_DST_RULE = 'in_dst_rule'
OUT_DST_RULE = 'out_dst_rule'

class Rule():

    def __init__(self, rule_type, rule_params):
        self.rule_type = rule_params
        self.rule_params = rule_params


        if self.rule_type == IN_SRC_RULE:
            return
        if self.rule_type == OUT_SRC_RULE:
            return
        if self.rule_type == IN_DST_RULE:
            return
        if self.rule_type == OUT_DST_RULE:
            return



import helper
def print_rules(chain_name, convert_units = True):
    print '*'*30
    print '*{:^28}*'.format(chain_name)
    print '*'*30
    rule_format = '{src_net} --> {dst_net} {match}\npkts: {packets:<7}size: {bytes:<7}\n---'
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)

    counters = get_chain_counters(chain_name)
    i = 0
    for r in chain.rules:
        packets, bytes = counters[i]
        src_net =  r.src
        dst_net = r.dst

        if convert_units:
            bytes = helper.convert_to_smallest_repr(bytes)
            src_net, subnet = src_net.split('/')
            src_net = src_net + '/' + helper.convert_submask_to_cidr(subnet)
            dst_net, subnet = dst_net.split('/')
            dst_net = dst_net + '/' + helper.convert_submask_to_cidr(subnet)

        match = "match: "
        for m in r.matches:
            match += m.name
            if m.sport:
                match += " src port " + m.sport
            elif m.dport:
                match += " dst port " + m.dport
        if match == 'match: ':
            match += '*'

        print rule_format.format(packets=packets, bytes=bytes, src_net=src_net, dst_net=dst_net, match=match)
        i += 1


