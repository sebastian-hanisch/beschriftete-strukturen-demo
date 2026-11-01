"""Orakel-Tests: der beschriftete Kalkül gegen unabhängige Rechenwege (DEMO-PLAYBOOK §12, ORACLE-PLAYBOOK §5).

Unabhängig heißt: Aufzählen aller Mengenpartitionen über Wachstumsfolgen (restricted growth strings, ohne die Erzeugung des Moduls), Aufzählen aller Permutationen mit ihren Zyklen,
die Dreiecke von Stirling und Bell, Rekursionen, e als Bruch, Kirchhoffs Determinante, die Siebformel und die Reihe mit Brüchen. Feste Zufallsstände."""

import itertools
import math
import random
from fractions import Fraction

import pytest

import bes_algorithm as A


def _rgs_partitions(n):
    """Mengenpartitionen von {0..n−1} als Wachstumsfolgen: a_0 = 0, a_i <= max(a_0..a_(i−1)) + 1."""
    def rec(prefix, top):
        if len(prefix) == n:
            yield tuple(prefix)
            return
        for v in range(top + 2):
            yield from rec(prefix + [v], max(top, v))

    if n == 0:
        yield ()
        return
    yield from rec([0], 0)


def _block_sizes(rgs):
    counts = {}
    for v in rgs:
        counts[v] = counts.get(v, 0) + 1
    return sorted(counts.values())


def _random_sizes(seed):
    rng = random.Random(seed)
    lo = rng.randint(1, 3)
    return lo, rng.randint(lo, 6)


@pytest.mark.parametrize("seed", range(80))
def test_set_partitions_with_block_sizes_in_a_range_equal_the_enumeration(seed):
    lo, hi = _random_sizes(seed)
    n = 8
    got = A.structures("Mengenpartitionen", lo, hi, None, n)
    want = [sum(1 for r in _rgs_partitions(m) if all(lo <= s <= hi for s in _block_sizes(r))) for m in range(n + 1)]
    assert got == want


@pytest.mark.parametrize("seed", range(40))
def test_set_partitions_with_exactly_k_blocks_equal_the_enumeration(seed):
    lo, hi = _random_sizes(seed)
    k = random.Random(seed).randint(1, 4)
    n = 7
    got = A.structures("Mengenpartitionen", lo, hi, k, n)
    want = [sum(1 for r in _rgs_partitions(m) if len(_block_sizes(r)) == k and all(lo <= s <= hi for s in _block_sizes(r))) for m in range(n + 1)]
    assert got == want


@pytest.mark.parametrize("seed", range(40))
def test_permutations_with_cycle_lengths_in_a_range_equal_the_enumeration(seed):
    lo, hi = _random_sizes(seed)
    n = 7
    got = A.structures("Permutationen", lo, hi, None, n)
    want = [sum(1 for p in itertools.permutations(range(m)) if all(lo <= c <= hi for c in A.cycle_lengths(p))) for m in range(n + 1)]
    assert got == want


@pytest.mark.parametrize("kind", ["Mengenpartitionen", "Permutationen"])
@pytest.mark.parametrize("seed", range(20))
def test_fraction_series_equals_the_integer_calculus(kind, seed):
    lo, hi = _random_sizes(seed)
    n = 12
    a = A.blocks(kind, lo, hi, n)
    assert A.egf_fraction_exp(a, n) == A.l_exp(a, n)
    k = random.Random(seed).randint(1, 4)
    assert A.egf_fraction_power(a, k, n) == A.l_pow_over_fact(a, k, n)


def test_stirling_and_bell_equal_their_triangles():
    n = 30
    s2, s1, bell = A.stirling2_triangle(n), A.stirling1_triangle(n), A.bell_triangle(n)
    cyc = A.blocks("Permutationen", 1, n, n)
    sets = A.blocks("Mengenpartitionen", 1, n, n)
    for k in range(0, 8):
        assert A.l_pow_over_fact(sets, k, n) == [s2[m][k] for m in range(n + 1)]
        assert A.l_pow_over_fact(cyc, k, n) == [s1[m][k] for m in range(n + 1)]
    assert A.l_exp(sets, n) == bell


def test_stirling_rows_satisfy_their_sum_rules():
    n = 30
    s2, s1, bell = A.stirling2_triangle(n), A.stirling1_triangle(n), A.bell_triangle(n)
    assert all(sum(s2[m]) == bell[m] for m in range(n + 1)) and all(sum(s1[m]) == math.factorial(m) for m in range(n + 1))
    assert all(sum(s1[m][k] * x ** k for k in range(m + 1)) == math.prod(x + i for i in range(m)) for m in range(1, 16) for x in range(-3, 6))


def test_surjections_equal_the_sieve_formula_and_the_enumeration():
    s2 = A.stirling2_triangle(20)
    assert all(math.factorial(k) * s2[n][k] == A.surjections_sieve(n, k) for n in range(1, 21) for k in range(1, n + 1))
    assert all(A.enumerate_surjections(n, k) == A.surjections_sieve(n, k) for n in range(1, 7) for k in range(1, 5))


def test_derangements_equal_n_factorial_over_e_rounded_and_the_sum_formula():
    e = sum(Fraction(1, math.factorial(j)) for j in range(420))
    d = A.derangements(300)
    assert all(d[n] == round(Fraction(math.factorial(n)) / e) for n in range(1, 301))
    assert all(d[n] == sum((-1) ** j * math.factorial(n) // math.factorial(j) for j in range(n + 1)) for n in range(1, 40))
    assert A.structures("Permutationen", 2, 300, None, 40) == d[:41]
    assert all(abs(Fraction(d[n], math.factorial(n)) - 1 / e) < Fraction(1, math.factorial(n + 1)) for n in range(1, 60))


def test_involutions_equal_the_enumeration_and_the_set_partitions_into_pairs_and_singletons():
    ref = [sum(1 for p in itertools.permutations(range(m)) if all(c <= 2 for c in A.cycle_lengths(p))) for m in range(8)]
    assert A.involutions(7) == ref == A.structures("Permutationen", 1, 2, None, 7) == A.structures("Mengenpartitionen", 1, 2, None, 7)


def test_cycle_types_sum_to_n_factorial_and_the_mean_cycle_count_is_harmonic():
    for n in range(1, 21):
        assert sum(A.cycle_type_counts(n).values()) == math.factorial(n)
    s1 = A.stirling1_triangle(30)
    assert all(Fraction(sum(k * s1[m][k] for k in range(m + 1)), math.factorial(m)) == sum(Fraction(1, j) for j in range(1, m + 1)) for m in range(1, 31))
    assert len(A.cycle_type_counts(10)) == A.partition_numbers(10)[10] == 42


def test_labelled_rooted_trees_equal_cayley_kirchhoff_and_the_enumeration():
    t = A.labelled_rooted_trees(40)
    assert all(t[n] == n ** (n - 1) for n in range(1, 41))
    assert all(n * A.kirchhoff_trees(n) == t[n] for n in range(1, 13))
    assert [A.enumerate_rooted_trees(n) for n in (1, 2, 3, 4, 5)] == [1, 2, 9, 64, 625]


def test_unlabelled_counts_match_stueck_5_constants():
    """Festgeschriebene Zahlen aus Stück 5: Zahlpartitionen und Wurzelbäume ohne Reihenfolge."""
    assert A.partition_numbers(10)[1:] == [1, 2, 3, 5, 7, 11, 15, 22, 30, 42]
    assert A.unlabelled_rooted_trees(14)[1:] == [1, 1, 2, 4, 9, 20, 48, 115, 286, 719, 1842, 4766, 12486, 32973]
    assert A.partition_numbers(100)[100] == 190569292


def test_known_values_agree_with_the_calculus_across_settings():
    for kind in ("Mengenpartitionen", "Permutationen"):
        for lo in (1, 2, 3):
            for hi in (2, 3, 4, 150):
                if hi < lo:
                    continue
                for k in (None, 1, 2, 3):
                    for n in (4, 6, 9, 12):
                        known = A.known_value(kind, lo, hi, k, n)
                        if known is not None:
                            assert known[1] == A.structures(kind, lo, hi, k, n)[n], (kind, lo, hi, k, n, known[0])
