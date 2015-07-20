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


def create_chain(name, policy='ACCEPT'):
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
