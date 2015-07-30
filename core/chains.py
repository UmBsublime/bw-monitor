import iptc

table = iptc.Table(iptc.Table.FILTER)


class Chain(object):
    def __init__(self, name):
        self.name = name
        self.reference = []
        self.rules = []
        self.create_chain()

    def _check_chain_exists(self):
        for i in table.chains:
            if self.name == i.name:
                return True
        return False

    def _find_references(self):
        for c in table.chains:
            #if c.name == 'INPUT' or c.name == 'OUTPUT':
                for r in c.rules:
                    if r.target.name == self.name:
                        self.reference.append(c.name)

    def add_reference(self, reference):
        reference_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), reference)
        rule = iptc.Rule()
        target = iptc.Target(rule, self.name)
        rule.target = target

        for chain in table.chains:
            if reference == chain.name:
                for r in chain.rules:
                    if r == rule:
                        return
                reference_chain.insert_rule(rule)
                self.reference.append(reference)

    def remove_reference(self, reference):
        reference_chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), reference)
        rule = iptc.Rule()
        target = iptc.Target(rule, self.name)
        rule.target = target

        for chain in table.chains:
            if reference == chain.name:
                for r in chain.rules:
                    if r == rule:
                        reference_chain.delete_rule(rule)
                        # self.reference.remove(reference)

    def get_chain(self):
        return self.chain

    def create_chain(self):
        if self._check_chain_exists():
            for i in table.chains:
                if self.name == i.name:
                    self.chain = i
                    self._find_references()
        else:
            self.chain = table.create_chain(self.name)

    def remove(self):
        self.flush_rules()
        for ref in self.reference:
            self.remove_reference(ref)
        table.delete_chain(self.name)

    def get_counters(self):
        counters = []

        for r in self.rules:
            result = {'counter':r.rule.get_counters(),
                      'name': r.name,
                      'dst_port': r.dport,
                      'src_port': r.sport,
                      'dst_net': r.dst_net,
                      'src_net': r.src_net}
            counters.append(result)

        return counters

    def reset_counters(self):
        self.chain.zero_counters()

    def flush_rules(self):
        self.chain.flush()

    def add_rule(self, new_rule):
        self.rules.append(new_rule)
        new_rule.add_to_chain(self.name)

    def delete_rule(self, del_rule):
        self.rules.remove(del_rule)
        del_rule.remove_from_chain(self.name)


if __name__ == '__main__':
    import rules

    t_rule = rules.Rule('http In', protocol='tcp', sport=80)
    t_rule2 = rules.Rule('http In', protocol='tcp', dport=80)
    t = Chain('banana')

    t.add_reference('OUTPUT')
    t.add_reference('INPUT')
    # t.add_reference('INPUT')
    t.add_rule(t_rule)
    t.add_rule(t_rule2)
    print t.get_counters()
    #t.reset_counters()
    # t.delete_rule(t_rule)
    # t.flush_rules()
    print t.get_chain()
    # t.remove()
    # t.remove()
