import iptc

table = iptc.Table(iptc.Table.FILTER)


def get_rule_comment(r):
    for m in r.matches:
        if m.comment is not None:
            return m.comment
    return None


def get_rule_spec(rule):
    src_net = rule.src
    dst_net = rule.dst
    dport = rule.matches[0].dport
    sport = rule.matches[0].sport
    name = None
    for m in rule.matches:
        if m.dport is not None:
            dport = m.dport
        if m.sport is not None:
            sport = m.sport
        if m.comment is not None:
            name = m.comment

    if dport is None:
        dport = 0
    if sport is None:
        sport = 0
    if name is None:
        name = ''

    spec = {'src_net': src_net,
            'dst_net': dst_net,
            'dport': int(dport),
            'sport': int(sport),
            'name': name}

    return spec


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
