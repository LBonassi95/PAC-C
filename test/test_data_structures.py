import unittest
import data_structures as ds


class FormulaTest(unittest.TestCase):

    def setUp(self):
        self.a = ds.Literal('A', False)
        self.b = ds.Literal('B', False)
        self.c = ds.Literal('C', False)
        self.d = ds.Literal('D', False)

    def test_literal_hashing(self):
        h1 = hash(True)
        h2 = hash(False)
        self.assertNotEqual(hash(self.a), hash(self.a.negate()))
        self.assertNotEqual(hash(self.a), hash(self.b))
        self.assertNotEqual(hash(self.a), hash(self.c))
        self.assertNotEqual(hash(self.a), hash(self.d))
        self.assertEqual(hash(self.a), hash(ds.Literal('A', False)))
        self.assertNotEqual(hash(self.a), hash(ds.Literal('A', True)))

    def test_negation1(self):
        self.assertEqual(self.a.negate(), ds.Literal('A', True))

    def test_negation2(self):
        disj = ds.Or([self.a, self.b])
        conj = ds.And([self.a.negate(), self.b.negate()])
        self.assertEqual(disj.negate(), conj)
        self.assertEqual(disj, conj.negate())

    def test_negation3(self):
        disj = ds.Or([self.a, ds.And([self.c.negate(), self.d]), self.b.negate()])
        conj = ds.And([self.a.negate(), ds.Or([self.c, self.d.negate()]), self.b])
        self.assertEqual(disj.negate(), conj)
        self.assertEqual(disj, conj.negate())

        disj = ds.Or([self.a, ds.And([self.c.negate(), self.d]), self.b.negate()])
        conj = ds.Or([self.a.negate(), ds.And([self.c, self.d.negate()]), self.b])
        self.assertNotEqual(disj.negate(), conj)

        disj = ds.Or([self.a, ds.And([self.c.negate(), self.d]), self.b.negate()])
        conj = ds.And([self.a.negate(), ds.And([self.c, self.d.negate()]), self.b])
        self.assertNotEqual(disj.negate(), conj)

    def test_negation4(self):
        disj = ds.Or([self.a, ds.And([self.c.negate(), ds.Or([self.d.negate(), self.a])]), self.b.negate()])
        conj = ds.And([self.a.negate(), ds.Or([self.c, ds.And([self.d, self.a.negate()])]), self.b])
        self.assertEqual(disj.negate(), conj)
        self.assertEqual(disj, conj.negate())

        disj = ds.Or([self.a, ds.And([self.c.negate(), ds.Or([self.d.negate(), self.a])]), self.b.negate()])
        conj = ds.And([self.a.negate(), ds.Or([self.c, ds.And([self.d, self.a])]), self.b])
        self.assertNotEqual(disj.negate(), conj)
        self.assertNotEqual(disj, conj.negate())

    def test_simplification1(self):
        conj = ds.And([self.a])
        self.assertEqual(conj.simplified(), self.a)

        conj = ds.And([self.a, self.b])
        self.assertEqual(conj.simplified(), conj)

        disj = ds.Or([self.a])
        self.assertEqual(disj.simplified(), self.a)

        disj = ds.Or([self.a, self.b])
        self.assertEqual(disj.simplified(), disj)

    def test_simplification2(self):
        conj = ds.And([self.a, ds.TRUE()])
        self.assertEqual(conj.simplified(), self.a)

        conj = ds.And([self.a])
        self.assertEqual(ds.And([conj]).simplified(), self.a)

        conj = ds.And([self.a, ds.FALSE()])
        self.assertEqual(conj.simplified(), ds.FALSE())

        conj = ds.And([ds.TRUE()])
        self.assertEqual(conj.simplified(), ds.TRUE())

        conj = ds.And([ds.FALSE()])
        self.assertEqual(conj.simplified(), ds.FALSE())

        conj = ds.And([])
        self.assertEqual(conj.simplified(), ds.TRUE())

        disj = ds.Or([self.a, ds.TRUE()])
        self.assertEqual(disj.simplified(), ds.TRUE())

        disj = ds.Or([self.a, ds.FALSE()])
        self.assertEqual(disj.simplified(), self.a)

        disj = ds.Or([ds.TRUE()])
        self.assertEqual(disj.simplified(), ds.TRUE())

        disj = ds.Or([ds.FALSE()])
        self.assertEqual(disj.simplified(), ds.FALSE())

        disj = ds.Or([])
        self.assertEqual(disj.simplified(), ds.FALSE())

        disj = ds.Or([self.a])
        self.assertEqual(ds.Or([disj]).simplified(), self.a)

    def test_simplification3(self):
        conj_1 = ds.And([self.a, self.b, ds.TRUE()])
        disj_1 = ds.Or([ds.FALSE(), conj_1])
        conj = ds.And([disj_1, self.c, ds.And([ds.And([self.d, ds.TRUE()])])])
        expected = ds.And([self.a, self.b, self.c, self.d])
        self.assertEqual(conj.simplified(), expected)
        print(conj.simplified())

    def test_simplification4(self):
        conj_1 = ds.And([self.b, ds.FALSE()])
        conj_2 = ds.And([self.c, ds.FALSE()])
        conj_3 = ds.And([self.d, ds.FALSE()])
        disj = ds.Or([conj_1, conj_2, conj_3])
        conj = ds.And([self.a, disj])
        expected = ds.FALSE()
        self.assertEqual(conj.simplified(), expected)
        print(conj.simplified())

    def test_simplification5(self):
        conj_1 = ds.Or([self.b, ds.FALSE()])
        conj_2 = ds.Or([self.c, ds.FALSE()])
        conj_3 = ds.Or([self.d, ds.FALSE()])
        disj = ds.Or([conj_1, conj_2, conj_3])
        conj = ds.And([self.a, disj])
        expected = ds.And([self.a, ds.Or([self.b, self.c, self.d])])
        self.assertEqual(conj.simplified(), expected)
        print(conj.simplified())

    def test_simplification6(self):
        conj_1 = ds.Or([self.b, ds.FALSE()])
        conj_2 = ds.Or([self.c, ds.FALSE()])
        conj_3 = ds.Or([self.d, ds.TRUE()])
        disj = ds.Or([conj_1, conj_2, conj_3])
        conj = ds.And([self.a, disj])
        expected = self.a
        self.assertEqual(conj.simplified(), expected)
        print(conj.simplified())

    def test_simplification7(self):
        conj_1 = ds.Or([self.b, ds.FALSE()])
        conj_2 = ds.Or([self.c, ds.TRUE()])
        conj_3 = ds.Or([ds.FALSE()])
        disj = ds.And([conj_1, conj_2, conj_3])
        conj = ds.Or([self.a, disj])
        expected = self.a
        self.assertEqual(conj.simplified(), expected)
        print(conj.simplified())