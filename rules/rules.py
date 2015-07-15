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

class Rule():

    def __init__(self, chain_name, direction, src_net='0.0.0.0/0', dst_net='0.0.0.0/0', port=0):

        if not isinstance(direction, str):
            raise TypeError
        else:
            if direction.upper() != 'INPUT' and direction.upper() != 'OUTPUT':
                raise TypeError
        if not isinstance(src_net, str):
            raise TypeError
        if not isinstance(dst_net, str):
            raise TypeError
        if not isinstance(port, int):
            raise TypeError

        self.chain_name = chain_name
        self.direction = direction
        self.src_net = src_net
        self.dst_net = dst_net
        self.port = port

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
        rule = iptc.Rule()
        rule.protocol = 'tcp'
        rule.src = self.src_net
        rule.dst = self.dst_net
        if self.port > 0:
            match = rule.create_match('tcp')
            match.sport = str(self.port)
        rule.target = iptc.Target(rule, '')
        if not test_rule_exists(chain_name, rule):
            chain.insert_rule(rule)


test = Rule('TEST_out', 'OUTPUT', '10.93.12.0/24', '10.93.12.0/24', 80)


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


