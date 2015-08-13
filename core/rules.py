import iptc

import helper
table = iptc.Table(iptc.Table.FILTER)



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


def get_rule_comment(r):
    for m in r.matches:
        if m.comment != None:
            return m.comment
    return None

def get_rule_spec(rule):
    src_net = rule.src
    dst_net = rule.dst
    dport = rule.matches[0].dport
    sport = rule.matches[0].sport

    for m in rule.matches:
        if m.dport != None:
            dport = m.dport
        if m.sport != None:
            sport = m.sport
        if m.comment != None:
            name = m.comment

    if dport == None:
        dport = 0
    if sport == None:
        sport = 0
    if name == None:
        name = ''

    spec = {'src_net': src_net,
            'dst_net': dst_net,
            'dport': int(dport),
            'sport': int(sport),
            'name': name}

    return spec


def wrap_existing_rule():
    pass



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

        comt = rule.create_match("comment")
        comt.comment = self.name
        rule.target = iptc.Target(rule, '')

        self.rule = rule


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
