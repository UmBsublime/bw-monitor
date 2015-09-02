import chains

class Group(object):

    def __init__(self, name, unit_list):
        self.name = name
        self.unit_list = unit_list
        self.in_chain = chains.Chain(self.name+'_in')
        self.ou_chain = chains.Chain(self.name+'_out')

    def add_unit(self, new_unit):
        pass

    def remove_unit(self, del_unit):
        pass

    def get_counters(self):
        pass

    def log_counters(self):
        pass

    def create_new_unit(self, name, port, network, local):
        pass