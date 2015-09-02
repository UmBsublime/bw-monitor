import rules


class Unit(object):

    def __init__(self, name, port, network, local):
        self.name = name
        self.port = port
        self.network = network
        self.local = local

        if self.local:
            self.incoming_rule = rules.Rule(self.name+'_incoming', src_net=self.network, dport=self.port)
            self.outgoing_tule = rules.Rule(self.name+'_outgoing',dst_net=self.network, sport=self.port)

        else:
            self.incoming_rule = rules.Rule(self.name+'_incoming', src_net=self.network, sport=self.port)
            self.outgoing_tule = rules.Rule(self.name+'_outgoing',dst_net=self.network, dport=self.port)

    def get_incoming_rule(self):
        return self.incoming_rule

    def get_outgoing_rule(self):
        return self.outgoing_tule

