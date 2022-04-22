import data_structures as ds


class Effect:
    def __init__(self, condition, effect):
        self.condition = condition
        self.effect = effect

    def __str__(self):
        if isinstance(self.condition, ds.TRUE):
            return str(self.effect)
        else:
            return '(when {} {})'.format(str(self.condition), str(self.effect))

    def __eq__(self, other):
        if not isinstance(other, Effect):
            return False
        return self.condition == other.condition and self.effect == other.effect


class Action:
    def __init__(self, name, pre, eff):
        self.name = name
        if not isinstance(pre, list):
            pre = [pre]
        self.precondition = pre
        self.effects = eff

    def __str__(self):
        action_str = '(:action {name}\n' \
                     ':parameters ()\n' \
                     ':precondition {preconditions}\n' \
                     ':effect (and {effects}))'
        eff_str = ''
        for eff in self.effects:
            eff_str += str(eff)

        pre_str = str(ds.And(self.precondition).simplified())
        return action_str.format(name=self.name, preconditions=pre_str, effects=eff_str)

    def __eq__(self, other):
        if not isinstance(other, Action):
            return False
        return self.name == other.name and \
               self.precondition == other.precondition and \
               self.effects == other.effects
