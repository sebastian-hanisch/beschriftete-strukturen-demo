"""Jede Zahl aus der README und aus den Texten der App, nachgerechnet (DEMO-PLAYBOOK §4). Es gibt keine Zeit als Zahl; die Zahlen sind exakt oder Bänder."""

import itertools
import math
from fractions import Fraction

import bes_algorithm as A
import bes_constants as C
import bes_evaluation as ev
from test_oracle_bes import _block_sizes, _rgs_partitions


def test_readme_hand_instances():
    assert A.bell_triangle(6) == [1, 1, 2, 5, 15, 52, 203]
    assert A.stirling2_triangle(4)[4][2] == 7 and A.stirling1_triangle(4)[4][2] == 11
    assert A.derangements(6) == [1, 0, 1, 2, 9, 44, 265] and A.involutions(6) == [1, 1, 2, 4, 10, 26, 76]
    assert A.labelled_rooted_trees(5)[1:] == [1, 2, 9, 64, 625]
    assert A.cycle_type_counts(4) == {(4,): 6, (3, 1): 8, (2, 2): 3, (2, 1, 1): 6, (1, 1, 1, 1): 1}


def test_readme_bell_and_stirling_numbers():
    bell = A.bell_triangle(200)
    assert (bell[10], bell[20], bell[30]) == (115975, 51724158235372, 846749014511809332450147) and A.digit_count(bell[200]) == 276
    s2, s1 = A.stirling2_triangle(10), A.stirling1_triangle(10)
    assert s2[10][1:11] == [1, 511, 9330, 34105, 42525, 22827, 5880, 750, 45, 1] and max(range(1, 11), key=lambda k: s2[10][k]) == 5
    assert s1[10][1:11] == [362880, 1026576, 1172700, 723680, 269325, 63273, 9450, 870, 45, 1]


def test_readme_derangements():
    d = A.derangements(100)
    assert (d[5], d[10], d[20]) == (44, 1334961, 895014631192902121)
    assert [round(d[n] / math.factorial(n), 5) for n in range(1, 9)] == [0.0, 0.5, 0.33333, 0.375, 0.36667, 0.36806, 0.36786, 0.36788]
    e = sum(Fraction(1, math.factorial(j)) for j in range(420))
    assert [round(float(abs(Fraction(d[n], math.factorial(n)) - 1 / e) * math.factorial(n + 1)), 4) for n in (5, 10, 50, 100)] == [0.8732, 0.9226, 0.9811, 0.9903]
    assert round(float(1 / e), 5) == 0.36788 and round(d[10] / math.factorial(10), 4) == 0.3679


def test_readme_cycle_types():
    types = A.cycle_type_counts(10)
    assert len(types) == 42 and sum(types.values()) == 3628800 and types[(9, 1)] == 403200 and types[(10,)] == 362880 and min(types.values()) == 1
    assert max(types, key=types.get) == (9, 1) and sorted(types.values())[-2] == 362880
    assert [len(A.cycle_type_counts(n)) for n in (5, 10, 20)] == [7, 42, 627] and [math.factorial(n) for n in (5, 10, 20)] == [120, 3628800, 2432902008176640000]
    assert sum(Fraction(1, j) for j in range(1, 11)) == Fraction(7381, 2520) and round(7381 / 2520, 4) == 2.929


def test_readme_labelled_trees():
    t = A.labelled_rooted_trees(40)
    assert all(t[n] == n ** (n - 1) for n in range(1, 41)) and [A.kirchhoff_trees(n) for n in range(2, 9)] == [n ** (n - 2) for n in range(2, 9)]
    assert [A.enumerate_rooted_trees(n) for n in (3, 4, 5, 6)] == [9, 64, 625, 7776]


def test_readme_labelled_against_unlabelled():
    bell, p = A.bell_triangle(20), A.partition_numbers(20)
    assert [(n, bell[n], p[n], round(bell[n] / p[n], 1)) for n in (5, 10, 15, 20)] == [(5, 52, 7, 7.4), (10, 115975, 42, 2761.3), (15, 1382958545, 176, 7857719.0), (20, 51724158235372, 627, 82494670231.9)]
    lab, unl = A.labelled_rooted_trees(60), A.unlabelled_rooted_trees(60)
    assert [(n, lab[n], unl[n]) for n in (5, 10, 20)] == [(5, 625, 9), (10, 10 ** 9, 719), (20, 20 ** 19, 12826228)]
    assert [round(lab[n] / unl[n], 1) for n in (5, 10)] == [69.4, 1390820.6] and 4.0e17 < lab[20] / unl[20] < 4.1e17
    assert [round(lab[n] / (math.factorial(n) * unl[n]), 4) for n in (5, 10, 20, 40, 60)] == [0.5787, 0.3833, 0.168, 0.0316, 0.0059]


def test_readme_bridge_to_assignment_clustering_packing():
    s2 = A.stirling2_triangle(10)
    assert s2[10][3] == 9330 and 6 * s2[10][3] == 55980 and 3 ** 10 == 59049 and round(55980 / 59049, 3) == 0.948
    assert [A.structures("Mengenpartitionen", 1, c, None, n)[n] for n, c in ((12, 4), (10, 3), (12, 2))] == [3305017, 61136, 140152]
    assert A.structures("Mengenpartitionen", 3, 3, None, 12)[12] == 15400 == math.factorial(12) // (6 ** 4 * 24)
    assert A.structures("Mengenpartitionen", 2, 2, None, 8)[8] == 105 == 7 * 5 * 3 * 1
    # unabhängig durch Aufzählen der Wachstumsfolgen: 10 Elemente, Gruppen bis 4 (alle und mit genau 3 Gruppen)
    sizes = [_block_sizes(r) for r in _rgs_partitions(10)]
    assert sum(1 for s in sizes if max(s) <= 4) == 99146 and sum(1 for s in sizes if len(s) == 3 and max(s) <= 4) == 3675


def test_readme_the_surjection_sieve():
    assert [A.surjections_sieve(4, 2), 2 ** 4 - 2, math.factorial(2) * A.stirling2_triangle(4)[4][2]] == [14, 14, 14]


def test_readme_effort_numbers():
    rows = ev.effort_rows()
    assert [(r["n"], r["Summanden exp-Kalkül"], r["Stellen von B(n)"]) for r in rows] == [(100, 5050, 116), (200, 20100, 276), (500, 125250, 844), (1000, 500500, 1928)]
    assert A.digit_count(A.bell_triangle(2000)[2000]) == 4350 > 4300
    assert A.exp_steps(1000) == A.bell_triangle_steps(1000) == 500500


def test_readme_product_set_times_cycle():
    assert A.l_mul([0, 1, 1, 1, 1], [0, 1, 1, 2, 6], 4)[4] == 18 == 4 * 2 + 6 * 1 + 4 * 1


def test_readme_presets():
    s = ev.Settings
    expected = {"Standardfall: Bell-Zahl von 10": 115975, "Clustering: 10 Punkte in 3 Cluster": 9330, "Packen: 12 Gegenstände, Gruppen bis 4": 3305017, "Dreiergruppen: 12 Personen": 15400,
                "Turnier: 8 Mannschaften in Paare": 105, "Derangements von 10": 1334961, "Involutionen von 10": 9496, "Permutationen mit 3 Zyklen (Stirling erster Art)": 1172700,
                "Beschriftete Wurzelbäume (Cayley)": 10 ** 9}
    assert set(expected) == set(C.PRESETS)
    for name, value in expected.items():
        a = ev.analyse(s(**C.PRESETS[name]))
        assert a.series[a.n_eff] == value, name
    assert round(ev.share_of_all(ev.analyse(s(**C.PRESETS["Derangements von 10"]))), 3) == 0.368
    assert A.unlabelled_rooted_trees(10)[10] == 719


def test_app_text_limits_come_from_the_constants():
    assert (C.N_MAX, C.LO_MAX, C.HI_MAX, C.K_MAX, C.FRACTION_BUDGET) == (150, 30, 150, 150, 60_000)
    assert (C.ENUM_SETS_N, C.ENUM_PERMS_N, C.ENUM_TREES_N, C.KIRCHHOFF_N, C.DERANGEMENT_CHECK_N, C.E_TERMS, C.ROW_N, C.ROW_TOP) == (9, 7, 6, 40, 300, 420, 10, 5)
    assert (C.WHY_NS, C.TREE_NS, C.TREE_RATIO_N, C.EFFORT_NS, C.TIME_NS, C.PLAY_MAX, C.PLAY_BRUTE_LIMIT) == ((5, 10, 15, 20), (5, 10, 20, 40, 60), 60, (100, 200, 500, 1000), (200, 300, 500), 30, 100_000)


def test_grenzen_table_number_b_1000_has_1928_digits():
    assert A.digit_count(A.bell_triangle(1000)[1000]) == 1928
