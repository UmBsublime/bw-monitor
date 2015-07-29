import iptc

table = iptc.Table(iptc.Table.FILTER)


def check_chain_exists(name):
    for i in table.chains:
        if name == i.name:
            return True
    return False


def get_chain(name):
    if check_chain_exists(name):
        for i in table.chains:
            if name == i.name:
                return i
    return None


def create_chain(name):
    if not check_chain_exists(name):
        table.create_chain(name)
        return True
    return False


def remove_chain(name):
    if check_chain_exists(name):
        table.delete_chain(name)
        return True
    return False


def get_chain_counters(name):
    chain = get_chain(name)
    if chain:
        counters = []
        for r in chain.rules:
            counters.append(r.get_counters())
        return counters
    return None


def reset_chain_counters(name):
    chain = get_chain(name)
    if chain:
        chain.zero_counters()
        return True
    return False


def flush_chain_rules(name):
    chain = get_chain(name)
    if chain:
        chain.flush()
        return True
    return False


class Chain(object):

    def __init__(self, name):
        self.name = name
        self.reference = []
        self.create_chain()

    def _check_chain_exists(self):
        for i in table.chains:
            if self.name == i.name:
                return True
        return False

    def _find_references(self):
        pass

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
                        self.reference.remove(reference)

    def get_chain(self):
        return self.chain

    def create_chain(self):
        if self._check_chain_exists():
            for i in table.chains:
                if self.name == i.name:
                    self.chain = i
        else:
            self.chain = table.create_chain(self.name)

    def remove(self):
        for r in self.reference:
            self.remove_reference(r)
        table.delete_chain(self.name)

    def get_counters(self):
        counters = []
        for r in self.chain.rules:
            counters.append(r.get_counters())
        return counters

    def reset_counters(self):
        self.chain.zero_counters()

    def flush_rules(self):
        self.chain.flush()

    def add_rule(self, new_rule):
        new_rule.add_to_chain(self.name)

    def delete_rule(self, del_rule):
        del_rule.remove_from_chain(self.name)

if __name__ == '__main__':
    import rules

    t_rule = rules.Rule('http In',protocol= 'tcp', sport=80)
    t_rule2 = rules.Rule('http In',protocol= 'tcp', dport=80)
    t = Chain('banana')


    t.add_reference('OUTPUT')
    t.add_reference('INPUT')
    #t.add_reference('INPUT')
    t.add_rule(t_rule)
    t.add_rule(t_rule2)
    print t.get_counters()
    t.reset_counters()
    #t.delete_rule(t_rule)
    #t.flush_rules()
    print t.get_chain()
    # t.remove()
    # t.remove()
