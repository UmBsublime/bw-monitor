import ConfigParser


def parse_file(filename):
    config = ConfigParser.RawConfigParser()
    config.read(filename)
    rules = []
    for section in config.sections():
        dport = config.getint(section, 'dport')
        sport = config.getint(section, 'sport')
        src_net = config.get(section, 'src_net')
        dst_net = config.get(section, 'dst_net')
        d_chain = config.get(section, 'chain')
        name = section
        new_rule = {'dport': dport,
                    'sport': sport,
                    'src_net': src_net,
                    'dst_net': dst_net,
                    'name': name,
                    'chain': d_chain}

        rules.append(new_rule)

    return rules
