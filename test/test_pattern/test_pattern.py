import unittest

import converter
import data_structures as ds
from downwardActionConstraints.FDgrounder import ground


def effect_conversion(action_effects):
    new_effects = []
    for cond, eff in action_effects:
        if not cond:
            new_effects.append(ds.Effect(ds.TRUE(), eff))
        else:
            new_effects.append(ds.Effect(ds.And(cond).simplified(), eff))
    return new_effects


class TestPatternGrounding(unittest.TestCase):

    def test1(self):
        F, A, I, G, C = ground('domain.pddl', 'tpp_p05_01.pddl')
        F, A, I, G, C = converter.convert(F, A, I, G, C)
        self.assertEqual(len(C), 3)

        constr_str = [str(c) for c in C]
        self.assertTrue('(pattern (drive__truck1__depot1__market2) (drive__truck1__market2__market1))' in constr_str)
        self.assertTrue('(pattern (drive__truck2__depot1__market2) (drive__truck2__market2__market1))' in constr_str)
        self.assertTrue('(pattern (drive__truck3__depot1__market2) (drive__truck3__market2__market1))' in constr_str)

    def test2(self):
        F, A, I, G, C = ground('domain.pddl', 'tpp_p05_02.pddl')
        F, A, I, G, C = converter.convert(F, A, I, G, C)
        self.assertEqual(len(C), 3)

        constr_str = [str(c) for c in C]
        self.assertTrue('(pattern (drive__truck1__depot1__market2) (drive__truck1__market2__market1))' in constr_str)
        self.assertTrue('(pattern (drive__truck2__depot1__market2) (drive__truck2__market2__market1))' in constr_str)
        self.assertTrue('(pattern (drive__truck3__depot1__market2) (drive__truck3__market2__market1))' in constr_str)






