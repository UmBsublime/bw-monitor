import iptc


from chains import get_chain_counters
import helper
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


def print_rules(chain_name, convert_units=True):
    print '*'*30
    print '*{:^28}*'.format(chain_name)
    print '*'*30
    rule_format = '{src_net} --> {dst_net} {match}\npkts: {packets:<7}size: {bytes_count:<7}\n---'
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)

    counters = get_chain_counters(chain_name)
    i = 0
    for r in chain.rules:
        packets, bytes_count = counters[i]
        src_net = r.src
        dst_net = r.dst

        if convert_units:
            bytes_count = helper.convert_to_smallest_repr(bytes_count)
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

        print rule_format.format(packets=packets, bytes_count=bytes_count, src_net=src_net, dst_net=dst_net, match=match)
        i += 1


class Rule(object):

    def __init__(self, name, protocol='tcp', src_net='0.0.0.0/0', dst_net='0.0.0.0/0', dport=0, sport=0):

        if not isinstance(src_net, str):
            raise TypeError
        if not isinstance(dst_net, str):
            raise TypeError
        if not isinstance(sport, int):
            raise TypeError
        if not isinstance(dport, int):
            raise TypeError
        self.name = name
        self.src_net = src_net
        self.dst_net = dst_net
        self.sport = sport
        self.dport = dport
        self.protocol = protocol
        self.chain_name = []

        rule = iptc.Rule()
        rule.protocol = self.protocol
        rule.src = self.src_net
        rule.dst = self.dst_net
        if self.sport > 0:
            match = rule.create_match(self.protocol)
            match.sport = str(self.sport)
        if self.dport > 0:
            match = rule.create_match(self.protocol)
            match.dport = str(self.dport)
        rule.target = iptc.Target(rule, '')

        self.rule = rule

    def add_to_chain(self, chain_name):
        self.chain_name.append(chain_name)
        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
        if not test_rule_exists(chain_name, self.rule):
            chain.insert_rule(self.rule)

    def remove_from_chain(self, chain_name):
        c_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), chain_name)
        if test_rule_exists(chain_name, self.rule):
            c_chain.delete_rule(self.rule)
            self.chain_name.remove(chain_name)
            return True
        return False


class InputRule(Rule):

    def __init__(self, name, protocol='tcp', src_net='0.0.0.0/0', dst_net='0.0.0.0/0', dport=0, sport=0):
        super(InputRule, self).__init__(name, protocol, src_net, dst_net, dport, sport)


class OutputRule(Rule):
    def __init__(self, name, protocol='tcp', src_net='0.0.0.0/0', dst_net='0.0.0.0/0', dport=0, sport=0):
        super(OutputRule, self).__init__(name, protocol, src_net, dst_net, dport, sport)


class InOutRule(Rule):
    def __init__(self, name, protocol='tcp', src_net='0.0.0.0/0', dst_net='0.0.0.0/0', dport=0, sport=0):
        super(InOutRule, self).__init__(name, protocol, src_net, dst_net, dport, sport)


def main():
    pass


if __name__ == '__main__':
    main()