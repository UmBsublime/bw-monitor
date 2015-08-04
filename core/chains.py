import iptc
import rules
table = iptc.Table(iptc.Table.FILTER)


class Chain(object):
    def __init__(self, name):
        self.name = name
        self.reference = []
        self.rules = []
        self._create_chain()

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

    def _rule_exists(self, rule):
        for r in self.chain.rules:
            if r == rule:
                return True
        return False

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

    def _create_chain(self):
        if self._check_chain_exists():
            for i in table.chains:
                if self.name == i.name:
                    self.chain = i
                    self._find_references()
        else:
            self.chain = table.create_chain(self.name)

        for r in self.chain.rules:
            spec = rules.get_rule_spec(r)
            wr = rules.Rule('Auto Gen', sport=spec['sport'], dport=spec['dport'],
                            src_net=spec['src_net'], dst_net=spec['dst_net'])
            wr.rule = r
            self.rules.append(wr)

    def remove(self):
        self.flush_rules()
        for ref in self.reference:
            self.remove_reference(ref)
        table.delete_chain(self.name)

    def get_counters(self):
        #table.refresh()
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

        for r in self.rules:
            spec = rules.get_rule_spec(r.rule)
            n_spec = rules.get_rule_spec(new_rule.rule)
            if spec['dst_net'] == n_spec['dst_net'] and spec['src_net'] == n_spec['src_net'] \
                and spec['sport'] == n_spec['sport'] and spec['dport'] == n_spec['dport']:
                r.name = new_rule.name
                #r = new_rule
                return

        if not self._rule_exists(new_rule.rule):
            self.chain.insert_rule(new_rule.rule)
            self.rules.append(new_rule)

    def delete_rule(self, del_rule):
        if self._rule_exists(del_rule.rule):
            self.chain.delete_rule(del_rule.rule)
            self.rules.remove(del_rule)


if __name__ == '__main__':
    import rules
    from time import sleep
    from pprint import pprint
    import sys

    t_rule = rules.Rule('HTTP In', protocol='tcp', sport=80)
    t_rule2 = rules.Rule('HTTP Out', protocol='tcp', dport=80)
    t_rule3 = rules.Rule('ssh', protocol='tcp', dport=22)
    t = Chain('test_out')

    t.add_reference('OUTPUT')
    t.add_reference('INPUT')
    # t.add_reference('INPUT')
    #t.add_rule(t_rule)
    t.add_rule(t_rule2)
    t.add_rule(t_rule3)
    while True:
        pprint (t.get_counters())
        #print 'ok'
        #print t.alt_get_counters()
        sys.stdout.flush()

        sleep(5)
        #print '\n\n'
    #t.reset_counters()
    # t.delete_rule(t_rule)
    # t.flush_rules()
    #print t.get_chain()
    #t.remove()
    # t.remove()
