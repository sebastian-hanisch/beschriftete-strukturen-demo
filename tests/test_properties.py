"""Eigenschaften (ORACLE-PLAYBOOK §5): Aussagen, die für jede Einstellung gelten, auf festen Zufallsständen."""

import math
import os
import random
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

import bes_algorithm as A
import bes_evaluation as ev

ROOT = Path(__file__).resolve().parent.parent


def _range(seed):
    rng = random.Random(seed)
    lo = rng.randint(1, 4)
    return lo, rng.randint(lo, 9)


@pytest.mark.parametrize("seed", range(40))
def test_a_range_contained_in_another_gives_no_more_structures(seed):
    lo, hi = _range(seed)
    for kind in ("Mengenpartitionen", "Permutationen"):
        inner = A.structures(kind, lo, hi, None, 14)
        outer = A.structures(kind, 1, hi + 2, None, 14)
        assert all(x <= y for x, y in zip(inner, outer))


@pytest.mark.parametrize("seed", range(40))
def test_structures_are_at_most_all_set_partitions_and_all_permutations(seed):
    lo, hi = _range(seed)
    n = 16
    assert all(x <= y for x, y in zip(A.structures("Mengenpartitionen", lo, hi, None, n), A.bell_triangle(n)))
    assert all(x <= math.factorial(m) for m, x in enumerate(A.structures("Permutationen", lo, hi, None, n)))


@pytest.mark.parametrize("seed", range(30))
def test_the_k_block_series_sum_to_the_series_without_k(seed):
    lo, hi = _range(seed)
    n = 12
    for kind in ("Mengenpartitionen", "Permutationen"):
        total = A.structures(kind, lo, hi, None, n)
        parts = [A.structures(kind, lo, hi, k, n) for k in range(0, n + 1)]
        assert [sum(p[m] for p in parts) for m in range(n + 1)] == total


@pytest.mark.parametrize("seed", range(30))
def test_the_binomial_product_is_commutative_and_associative(seed):
    rng = random.Random(seed)
    n = 9
    a, b, c = ([0] + [rng.randint(0, 5) for _ in range(n)] for _ in range(3))
    assert A.l_mul(a, b, n) == A.l_mul(b, a, n)
    assert A.l_mul(A.l_mul(a, b, n), c, n) == A.l_mul(a, A.l_mul(b, c, n), n)


@pytest.mark.parametrize("seed", range(30))
def test_exp_of_a_sum_is_the_product_of_the_exps(seed):
    rng = random.Random(seed)
    n = 10
    a = [0] + [rng.randint(0, 4) for _ in range(n)]
    b = [0] + [rng.randint(0, 4) for _ in range(n)]
    assert A.l_exp([x + y for x, y in zip(a, b)], n) == A.l_mul(A.l_exp(a, n), A.l_exp(b, n), n)


@pytest.mark.parametrize("n", range(1, 25))
def test_set_of_cycles_equals_sequence_of_single_elements(n):
    z = [0, 1] + [0] * n
    assert A.l_exp(A.l_cyc(z, n), n) == A.l_seq(z, n) == [math.factorial(m) for m in range(n + 1)]


@pytest.mark.parametrize("n", range(1, 25))
def test_derangements_plus_permutations_with_fixed_points_equal_n_factorial(n):
    """Mit f Fixpunkten: C(n,f)·D_(n−f); die Summe über f ist n!."""
    d = A.derangements(n)
    assert sum(math.comb(n, f) * d[n - f] for f in range(n + 1)) == math.factorial(n)


@pytest.mark.parametrize("n", range(1, 21))
@pytest.mark.parametrize("k", range(1, 7))
def test_surjections_never_exceed_all_assignments_and_vanish_for_k_above_n(n, k):
    sur = A.surjections_sieve(n, k)
    assert 0 <= sur <= k ** n and (sur == 0) == (k > n)


@pytest.mark.parametrize("n", range(1, 40))
def test_labelled_is_at_most_n_factorial_times_unlabelled(n):
    """Jede unbeschriftete Klasse hat höchstens n! Beschriftungen; für Bäume gilt außerdem: beschriftet >= unbeschriftet."""
    lab, unl = A.labelled_rooted_trees(n)[n], A.unlabelled_rooted_trees(n)[n]
    assert unl <= lab <= math.factorial(n) * unl
    assert A.bell_triangle(n)[n] >= A.partition_numbers(n)[n]


def test_the_labelled_ratio_falls_for_trees():
    lab, unl = A.labelled_rooted_trees(60), A.unlabelled_rooted_trees(60)
    ratio = [Fraction(lab[n], math.factorial(n) * unl[n]) for n in (5, 10, 20, 40, 60)]
    assert all(x > y for x, y in zip(ratio, ratio[1:])) and ratio[0] < 1


def test_the_derangement_probability_settles_down():
    d = A.derangements(60)
    probs = [Fraction(d[n], math.factorial(n)) for n in range(8, 61)]
    assert all(abs(x - y) < Fraction(1, 10 ** 4) for x, y in zip(probs, probs[1:]))


def test_analyses_are_deterministic_across_hash_seeds():
    code = ("import sys; sys.path.insert(0, %r); import bes_evaluation as ev; a = ev.analyse(ev.Settings('Mengenpartitionen', 12, 1, 4, 0)); print(a.series, [w['Wert'] for w in a.ways])" % str(ROOT))
    runs = {subprocess.run([sys.executable, "-X", "utf8", "-c", code], capture_output=True, text=True, encoding="utf-8", env={**os.environ, "PYTHONHASHSEED": str(h)}).stdout for h in (0, 1, 12345)}
    assert len(runs) == 1 and runs.pop().strip()


def test_the_upper_limit_beyond_n_does_not_change_the_series():
    a = ev.analyse(ev.Settings("Permutationen", 9, 2, 9, 0))
    b = ev.analyse(ev.Settings("Permutationen", 9, 2, 150, 0))
    assert a.series == b.series == A.derangements(9)
