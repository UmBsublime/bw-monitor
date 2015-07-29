import chains
import rules


class Counter(object):
    '''

    Counter's consist of 3 chains:
      - 1 Referenced by INPUT
      - 1 Referenced by OUTPUT
      - 1 Referenced by both

    Each chain can can have any amount of rules

    '''

    def __init__(self, name, all_rules):

        self.name = name
        self.rules = all_rules
        self.input_chain = chains.Chain(self.name + '_in')
        self.input_chain.add_reference('INPUT')

        self.output_chain = chains.Chain(self.name + '_out')
        self.output_chain.add_reference('OUTPUT')

        self.dual_chain = chains.Chain(self.name + '_dual')
        self.dual_chain.add_reference('INPUT')
        self.dual_chain.add_reference('OUTPUT')

        for r in self.rules:
            self.add_rule(r)

    def add_rule(self, new_rule):
        if isinstance(new_rule, rules.InputRule):
            self.input_chain.add_rule(new_rule)
        if isinstance(new_rule, rules.OutputRule):
            self.output_chain.add_rule(new_rule)
        if isinstance(new_rule, rules.InOutRule):
            self.dual_chain.add_rule(new_rule)

    def remove_rule(self, del_rule):
        if isinstance(del_rule, rules.InputRule):
            self.input_chain.delete_rule(del_rule)
        if isinstance(del_rule, rules.OutputRule):
            self.output_chain.delete_rule(del_rule)
        if isinstance(del_rule, rules.InOutRule):
            self.dual_chain.delete_rule(del_rule)


    def reset_counters(self):
        self.input_chain.reset_counters()
        self.output_chain.reset_counters()
        self.dual_chain.reset_counters()
        pass

    def get_counters(self):
        result = {'In': self.input_chain.get_counters(),
                  'Out': self.output_chain.get_counters(),
                  'Dual': self.dual_chain.get_counters()}
        return result

    def flush_rules(self):
        self.input_chain.flush_rules()
        self.output_chain.flush_rules()
        self.dual_chain.flush_rules()
        pass

    def delete(self):
        self.input_chain.remove()
        self.output_chain.remove()
        self.dual_chain.remove()


if __name__ == '__main__':
    from pprint import pprint
    from time import sleep

    dicom_in = rules.InputRule('DICOM In', protocol='tcp', sport=5000)
    dicom_out = rules.OutputRule('DICOM Out', protocol='tcp', dport=5000)
    http_in = rules.InOutRule('HTTP In', sport=80)


    ssh = rules.InOutRule('SSH', sport=22)
    test = Counter('test', [dicom_in, dicom_out, http_in])
    test.add_rule(ssh)
    pprint(test.get_counters())
    #test.remove_rule(ssh)
    test.reset_counters()
    #pprint(test.get_counters())
    #test.flush_rules()
    #pprint(test.get_counters())
    #sleep(2)
    #print(test.get_counters())

    test.delete()
