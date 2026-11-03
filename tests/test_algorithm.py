"""Einheitentests des Rechenkerns an von Hand gerechneten Werten (DEMO-PLAYBOOK §1b)."""

import math

import pytest

import bes_algorithm as A


def test_product_set_times_cycle_by_hand(hand_n4):
    ones = [0, 1, 1, 1, 1]
    cyc = [0] + [math.factorial(k - 1) for k in range(1, 5)]
    assert A.l_mul(ones, cyc, 4)[4] == hand_n4["set_times_cycle"] == 18
    assert A.l_mul(ones, cyc, 4) == A.l_mul(cyc, ones, 4)                              # die Binomialfaltung ist kommutativ


def test_set_of_blocks_of_size_one_or_two_is_the_involution_count():
    assert A.l_exp([0, 1, 1, 0, 0], 4) == [1, 1, 2, 4, 10]


def test_exp_pascal_equals_exp_and_refuses_the_same_input():
    import random
    rng = random.Random(7)
    for n in (0, 1, 2, 5, 12, 40):
        a = [0] + [rng.randint(0, 9) for _ in range(n)]
        assert A.l_exp_pascal(a, n) == A.l_exp(a, n)
    assert A.l_exp_pascal(A.blocks("Mengenpartitionen", 1, 60, 60), 60) == A.bell_triangle(60)
    with pytest.raises(ValueError):
        A.l_exp_pascal([1, 1, 1], 2)
    with pytest.raises(ValueError):
        A.l_exp_pascal([0, 1], 3)


def test_set_of_nonempty_blocks_is_bell():
    assert A.l_exp([0, 1, 1, 1, 1, 1, 1], 6) == [1, 1, 2, 5, 15, 52, 203]


def test_sequence_of_a_single_element_is_n_factorial_and_cycle_is_n_minus_1_factorial():
    z = [0, 1, 0, 0, 0, 0, 0]
    assert A.l_seq(z, 5) == [1, 1, 2, 6, 24, 120]
    assert A.l_cyc(z, 5) == [0, 1, 1, 2, 6, 24]


def test_set_of_cycles_is_the_permutation_count():
    assert A.l_exp(A.l_cyc([0, 1, 0, 0, 0, 0, 0], 5), 5) == [math.factorial(n) for n in range(6)]


def test_exactly_k_blocks_by_hand(hand_n4):
    assert A.l_pow_over_fact([0, 1, 1, 1, 1], 2, 4)[4] == hand_n4["S42"] == 7
    cyc = [0] + [math.factorial(k - 1) for k in range(1, 5)]
    assert A.l_pow_over_fact(cyc, 2, 4)[4] == hand_n4["c42"] == 11
    assert A.l_pow_over_fact([0, 1, 1, 1], 0, 3) == [1, 0, 0, 0]


def test_step_formulas_by_hand():
    assert A.exp_steps(4) == 1 + 2 + 3 + 4 == 10 and A.mul_steps(3) == 1 + 2 + 3 + 4 == 10 and A.bell_triangle_steps(4) == 10 and A.exp_steps(0) == 0


def test_blocks_by_hand():
    assert A.blocks("Mengenpartitionen", 2, 3, 5) == [0, 0, 1, 1, 0, 0]
    assert A.blocks("Permutationen", 2, 4, 5) == [0, 0, 1, 2, 6, 0]


def test_structures_by_hand(hand_set_partitions_of_3, hand_permutations_of_3):
    assert A.structures("Mengenpartitionen", 1, 3, None, 3)[3] == hand_set_partitions_of_3["bell"]
    assert A.structures("Mengenpartitionen", 1, 2, None, 3)[3] == hand_set_partitions_of_3["blocks_up_to_2"]
    assert A.structures("Permutationen", 2, 3, None, 3)[3] == hand_permutations_of_3["derangements"]
    assert A.structures("Permutationen", 1, 2, None, 3)[3] == hand_permutations_of_3["involutions"]
    assert A.structures("Permutationen", 1, 3, None, 3)[3] == sum(hand_permutations_of_3["types"].values()) == 6


def test_labelled_rooted_trees_by_hand():
    assert A.labelled_rooted_trees(5) == [0, 1, 2, 9, 64, 625]
    assert A.labelled_rooted_trees(0) == [0] and A.labelled_rooted_trees(1) == [0, 1]


def test_triangles_by_hand(hand_n4):
    s2, s1 = A.stirling2_triangle(4), A.stirling1_triangle(4)
    assert s2[4][1:5] == [1, 7, 6, 1] and s1[4][1:5] == [6, 11, 6, 1] and s2[4][2] == hand_n4["S42"] and s1[4][2] == hand_n4["c42"]
    assert A.bell_triangle(6) == [1, 1, 2, 5, 15, 52, 203]


def test_recursions_by_hand():
    assert A.derangements(6) == [1, 0, 1, 2, 9, 44, 265] and A.involutions(6) == [1, 1, 2, 4, 10, 26, 76]


def test_kirchhoff_by_hand():
    assert [A.kirchhoff_trees(n) for n in (1, 2, 3, 4, 5)] == [1, 1, 3, 16, 125]


def test_enumeration_by_hand(hand_set_partitions_of_3, hand_permutations_of_3, hand_n4):
    as_sets = {frozenset(frozenset(b) for b in p) for p in A.set_partitions([1, 2, 3])}
    assert as_sets == {frozenset(frozenset(b) for b in p) for p in hand_set_partitions_of_3["all"]} and len(as_sets) == 5
    assert A.enumerate_count("Mengenpartitionen", 1, 3, None, 3) == 5 and A.enumerate_count("Mengenpartitionen", 1, 2, None, 3) == 4
    assert A.enumerate_count("Permutationen", 2, 4, None, 4) == hand_n4["derangements"]
    assert A.enumerate_count("Permutationen", 1, 4, 2, 4) == hand_n4["c42"] and A.enumerate_count("Mengenpartitionen", 1, 4, 2, 4) == hand_n4["S42"]
    assert A.enumerate_rooted_trees(3) == 9 and A.enumerate_rooted_trees(2) == 2
    assert A.enumerate_surjections(4, 2) == hand_n4["surjections"] == A.surjections_sieve(4, 2) == 14


def test_cycle_types_by_hand(hand_n4, hand_permutations_of_3):
    assert A.cycle_type_counts(4) == hand_n4["types"] and A.cycle_type_counts(3) == hand_permutations_of_3["types"]


def test_unlabelled_counts_by_hand():
    assert A.partition_numbers(8) == [1, 1, 2, 3, 5, 7, 11, 15, 22] and A.unlabelled_rooted_trees(7) == [0, 1, 1, 2, 4, 9, 20, 48]


def test_known_value_by_hand():
    assert A.known_value("Mengenpartitionen", 1, 150, None, 4) == ("Bell-Dreieck", 15)
    assert A.known_value("Mengenpartitionen", 1, 150, 2, 4) == ("Stirling-Dreieck (zweite Art)", 7)
    assert A.known_value("Mengenpartitionen", 3, 3, None, 6)[1] == 10 and A.known_value("Mengenpartitionen", 3, 3, None, 7)[1] == 0
    assert A.known_value("Mengenpartitionen", 2, 2, None, 4)[1] == 3
    assert A.known_value("Permutationen", 2, 150, None, 4) == ("Rekursion der Derangements", 9)
    assert A.known_value("Permutationen", 1, 2, None, 4)[1] == 10 and A.known_value("Mengenpartitionen", 1, 2, None, 4)[1] == 10
    assert A.known_value("Permutationen", 1, 150, 2, 4) == ("Stirling-Dreieck (erste Art)", 11) and A.known_value("Permutationen", 1, 150, None, 4) == ("Fakultät", 24)
    assert A.known_value("Permutationen", 3, 4, None, 6) is None and A.known_value("Mengenpartitionen", 2, 5, 2, 6) is None
    assert A.known_value("Mengenpartitionen", 1, 150, 9, 4)[1] == 0


def test_fraction_paths_by_hand():
    a = A.blocks("Mengenpartitionen", 1, 6, 6)
    assert A.egf_fraction_exp(a, 6) == [1, 1, 2, 5, 15, 52, 203]
    assert A.egf_fraction_power(a, 2, 4)[4] == 7


def test_digit_count_and_log10():
    assert A.digit_count(0) == 1 and A.digit_count(999) == 3 and A.digit_count(1000) == 4 and A.digit_count(10 ** 5000) == 5001
    with pytest.raises(ValueError):
        A.digit_count(-1)
    assert A.log10_int(1) == 0 and abs(A.log10_int(10 ** 500) - 500) < 1e-9
    with pytest.raises(ValueError):
        A.log10_int(0)


def test_invalid_input_is_refused():
    with pytest.raises(ValueError):
        A.l_exp([1, 1, 1], 2)                                   # a[0] muss 0 sein
    with pytest.raises(ValueError):
        A.l_seq([1, 1, 1], 2)
    with pytest.raises(ValueError):
        A.l_exp([0, 1], 3)                                      # Folge zu kurz
    with pytest.raises(ValueError):
        A.l_pow_over_fact([0, 1, 1], -1, 2)
    with pytest.raises(ValueError):
        A.blocks("Unsinn", 1, 2, 3)
    with pytest.raises(ValueError):
        A.blocks("Permutationen", 0, 2, 3)
    with pytest.raises(ValueError):
        A.blocks("Permutationen", 3, 2, 3)
