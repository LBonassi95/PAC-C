ALWAYS = 'always'
SOMETIME = 'sometime'
ATMOSTONCE = 'at-most-once'
SOMETIMEBEFORE = 'sometime-before'
SOMETIMEAFTER = 'sometime-after'
ALWAYSNEXT = 'always-next'
PATTERN = 'pattern'

NARY_KINDS = [PATTERN]

KINDS = [ALWAYS, SOMETIME, ATMOSTONCE, SOMETIMEAFTER, SOMETIMEBEFORE, ALWAYSNEXT, PATTERN]


def isNary(kind):
    return kind in NARY_KINDS


def has2gd(kind):
    return kind == SOMETIMEAFTER or kind == SOMETIMEBEFORE or kind == ALWAYSNEXT


class HardConstraint:
    def __init__(self, condition, kind):
        self.gd1 = condition
        self.kind = kind
        self.monitoring_atom = ''

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.gd1 == other.gd1)

    def set_monitoring_atom_predicate(self, predicate):
        self.monitoring_atom = predicate

    def __str__(self):
        return '({} {})'.format(self.kind, str(self.gd1))


class Always(HardConstraint):
    def __init__(self, condition):
        super().__init__(condition, ALWAYS)


class Sometime(HardConstraint):
    def __init__(self, condition):
        super().__init__(condition, SOMETIME)


class AtMostOnce(HardConstraint):
    def __init__(self, condition):
        super().__init__(condition, ATMOSTONCE)


class SometimeBefore(HardConstraint):
    def __init__(self, condition1, condition2):
        super().__init__(condition1, SOMETIMEBEFORE)
        self.gd2 = condition2

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.gd1 == other.gd1 and self.gd2 == other.gd2)

    def __str__(self):
        return '({} {} {})'.format(self.kind, str(self.gd1), str(self.gd2))


class SometimeAfter(HardConstraint):
    def __init__(self, condition1, condition2):
        super().__init__(condition1, SOMETIMEAFTER)
        self.gd2 = condition2

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.gd1 == other.gd1 and self.gd2 == other.gd2)

    def __str__(self):
        return '({} {} {})'.format(self.kind, str(self.gd1), str(self.gd2))


class AlwaysNext(HardConstraint):
    def __init__(self, condition1, condition2):
        super().__init__(condition1, ALWAYSNEXT)
        self.gd2 = condition2

    def __eq__(self, other):
        return (self.__class__ == other.__class__ and
                self.gd1 == other.gd1 and self.gd2 == other.gd2)

    def __str__(self):
        return '({} {} {})'.format(self.kind, str(self.gd1), str(self.gd2))


class NaryConstraint:
    def __init__(self, condition_list, kind):
        assert isinstance(condition_list, list)
        self.kind = kind
        self.gd1 = condition_list
        self.monitoring_atoms = []

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if len(self.gd1) != len(other.gd1):
            return False
        for i in range(len(self.gd1)):
            if self.gd1[i] != other.gd1[i]:
                return False
        return True

    def __str__(self):
        return '({} {})'.format(self.kind, ' '.join([str(cond) for cond in self.gd1]))

    def set_monitoring_atoms(self, m_atoms):
        self.monitoring_atoms = m_atoms


class Pattern(NaryConstraint):
    def __init__(self, condition_list):
        super(Pattern, self).__init__(condition_list, PATTERN)
