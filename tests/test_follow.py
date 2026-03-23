# Tests para el calculo de FOLLOW

import sys
import os
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from parser import parse_grammar
from first_follow import compute_first, compute_follow

GRAMMARS_DIR = os.path.join(os.path.dirname(__file__), 'grammars')


# Gramatica simple: S -> A B, A -> a, B -> b c
class TestFollowSimple(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'simple.txt')
        start, nts, terms, prods = parse_grammar(path)
        first = compute_first(nts, terms, prods, verbose=False)
        self.follow = compute_follow(start, nts, terms, prods, first,
                                     verbose=False)

    def test_follow_S(self):
        self.assertEqual(self.follow['S'], {'$'})

    def test_follow_A(self):
        self.assertEqual(self.follow['A'], {'b'})

    def test_follow_B(self):
        self.assertEqual(self.follow['B'], {'$'})


# Gramatica con epsilon: S -> A B, A -> a | ε, B -> b A
class TestFollowEpsilon(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'epsilon.txt')
        start, nts, terms, prods = parse_grammar(path)
        first = compute_first(nts, terms, prods, verbose=False)
        self.follow = compute_follow(start, nts, terms, prods, first,
                                     verbose=False)

    def test_follow_S(self):
        self.assertEqual(self.follow['S'], {'$'})

    def test_follow_A(self):
        self.assertEqual(self.follow['A'], {'b', '$'})

    def test_follow_B(self):
        self.assertEqual(self.follow['B'], {'$'})


# Gramatica de expresiones con EP, TP
class TestFollowIndirect(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'indirect.txt')
        start, nts, terms, prods = parse_grammar(path)
        first = compute_first(nts, terms, prods, verbose=False)
        self.follow = compute_follow(start, nts, terms, prods, first,
                                     verbose=False)

    def test_follow_E(self):
        self.assertEqual(self.follow['E'], {'$', ')'})

    def test_follow_EP(self):
        self.assertEqual(self.follow['EP'], {'$', ')'})

    def test_follow_T(self):
        self.assertEqual(self.follow['T'], {'+', '$', ')'})

    def test_follow_TP(self):
        self.assertEqual(self.follow['TP'], {'+', '$', ')'})

    def test_follow_F(self):
        self.assertEqual(self.follow['F'], {'*', '+', '$', ')'})


# Gramatica obligatoria del curso con notacion E', T'
class TestFollowCourse(unittest.TestCase):

    def setUp(self):
        path = os.path.join(GRAMMARS_DIR, 'course.txt')
        start, nts, terms, prods = parse_grammar(path)
        first = compute_first(nts, terms, prods, verbose=False)
        self.follow = compute_follow(start, nts, terms, prods, first,
                                     verbose=False)

    def test_follow_E(self):
        self.assertEqual(self.follow['E'], {'$', ')'})

    def test_follow_EP(self):
        self.assertEqual(self.follow["E'"], {'$', ')'})

    def test_follow_T(self):
        self.assertEqual(self.follow['T'], {'+', '$', ')'})

    def test_follow_TP(self):
        self.assertEqual(self.follow["T'"], {'+', '$', ')'})

    def test_follow_F(self):
        self.assertEqual(self.follow['F'], {'*', '+', '$', ')'})


if __name__ == '__main__':
    unittest.main()
