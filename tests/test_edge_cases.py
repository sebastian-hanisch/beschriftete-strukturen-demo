"""Randfälle: leere Eingaben, Grenzen der Regler, große Zahlen (die 4300-Stellen-Grenze von `str`), jede Familie bei den kleinsten Größen."""

import pytest

import bes_algorithm as A
import bes_constants as C
import bes_evaluation as ev
import bes_scenario as S


def test_zero_elements_have_exactly_one_structure():
    for kind in ("Mengenpartitionen", "Permutationen"):
        assert A.structures(kind, 1, 3, None, 0) == [1]
        assert A.structures(kind, 1, 3, 0, 0) == [1]


def test_one_element():
    assert A.structures("Mengenpartitionen", 1, 150, None, 1) == [1, 1] and A.structures("Permutationen", 1, 150, None, 1) == [1, 1]
    assert A.structures("Permutationen", 2, 150, None, 1) == [1, 0]                       # ein Element ist ein Fixpunkt
    assert A.structures("Mengenpartitionen", 2, 150, None, 1) == [1, 0]


def test_block_size_one_only_gives_the_identity():
    assert A.structures("Permutationen", 1, 1, None, 6) == [1] * 7 and A.structures("Mengenpartitionen", 1, 1, None, 6) == [1] * 7


def test_blocks_larger_than_n_are_irrelevant():
    assert A.structures("Mengenpartitionen", 1, 150, None, 5) == A.structures("Mengenpartitionen", 1, 5, None, 5)
    assert A.structures("Mengenpartitionen", 7, 9, None, 5) == [1, 0, 0, 0, 0, 0]


def test_stirling_edges():
    assert A.structures("Mengenpartitionen", 1, 150, 0, 4) == [1, 0, 0, 0, 0]              # k = 0: nur die leere Struktur
    assert A.structures("Mengenpartitionen", 1, 150, 9, 4) == [0] * 5                      # mehr Blöcke als Elemente
    assert A.structures("Permutationen", 1, 150, 1, 5)[5] == 24                            # ein Zyklus: (n−1)!
    assert A.structures("Mengenpartitionen", 1, 150, 1, 5)[5] == 1 and A.structures("Mengenpartitionen", 1, 150, 5, 5)[5] == 1


def test_huge_numbers_never_pass_through_str():
    big = A.bell_triangle(2000)[2000]
    assert A.digit_count(big) == 4350 and ev.big_text(big).endswith("(4350 Stellen)") and abs(A.log10_int(big) - 4349.5) < 1


def test_large_calculus_is_exact_and_formatted():
    a = ev.analyse(ev.Settings("Mengenpartitionen", 150, 1, 150, 0))
    assert a.series[150] == A.bell_triangle(150)[150] and a.problems == []
    assert [w["Weg"] for w in a.ways if w["Wert"] is not None] == ["Binomialfaltung (exp-Kalkül)", "Reihe mit Brüchen (exponentielle EGF)", "Bell-Dreieck"]


def test_fraction_path_is_skipped_when_too_expensive():
    a = ev.analyse(ev.Settings("Mengenpartitionen", 150, 1, 150, 40))
    row = next(r for r in ev.way_rows(a) if r["Weg"].startswith("Reihe mit Brüchen"))
    assert row["Anzahl bei N"] == "–" and "übersprungen" in row["Ergebnis"]
    assert a.series[150] == A.stirling2_triangle(150)[150][40]


def test_normalise_clamps_and_reports():
    assert S.normalise("Mengenpartitionen", 5000, 0, 3, -2) == (150, 1, 3, None, [])
    n, lo, hi, k, notes = S.normalise("Permutationen", 10, 5, 2, 3)
    assert (n, lo, hi, k) == (10, 5, 5, 3) and "liegt unter der kleinsten" in notes[0]
    assert S.normalise("Wurzelbäume", 10, 4, 7, 2)[:4] == (10, 1, 150, None) and "ignoriert" in S.normalise("Wurzelbäume", 10, 4, 7, 2)[4][0]
    assert S.normalise("Wurzelbäume", 10, 1, 150, 0)[4] == []
    with pytest.raises(ValueError):
        S.normalise("Unsinn", 5, 1, 1, 0)


@pytest.mark.parametrize("family", C.FAMILIES)
@pytest.mark.parametrize("n", [1, 2, 3])
@pytest.mark.parametrize("k", [0, 1, 2])
def test_every_family_works_at_the_smallest_sizes(family, n, k):
    a = ev.analyse(ev.Settings(family, n, 1, 150, k))
    assert a.problems == [] and len(a.series) == a.n_eff + 1 and all(x >= 0 for x in a.series)
    assert ev.verdict_answers(a)[0] == "success" and ev.way_rows(a) and ev.first_values(a)


def test_wrong_order_of_range_is_corrected_with_a_note():
    a = ev.analyse(ev.Settings("Mengenpartitionen", 8, 4, 2, 0))
    assert a.hi == 4 and a.notes and a.series == A.structures("Mengenpartitionen", 4, 4, None, 8)


def test_trees_ignore_the_block_settings():
    base = ev.analyse(ev.Settings("Wurzelbäume", 7))
    odd = ev.analyse(ev.Settings("Wurzelbäume", 7, 3, 5, 2))
    assert base.series == odd.series and odd.notes and not base.notes


def test_trees_skip_slow_oracles_when_large():
    a = ev.analyse(ev.Settings("Wurzelbäume", 100))
    rows = {r["Weg"]: r for r in ev.way_rows(a)}
    assert rows["Kirchhoff (Spannbäume von Kₙ mal n Wurzeln)"]["Anzahl bei N"] == "–" and rows["Aufzählen aller Elternfunktionen"]["Anzahl bei N"] == "–"
    assert rows["Formel von Cayley nⁿ⁻¹"]["Ergebnis"] == "gleich"


def test_enumeration_limits():
    assert next(r for r in ev.way_rows(ev.analyse(ev.Settings("Mengenpartitionen", 10))) if r["Weg"].startswith("Aufzählen"))["Anzahl bei N"] == "–"
    assert next(r for r in ev.way_rows(ev.analyse(ev.Settings("Mengenpartitionen", 9))) if r["Weg"].startswith("Aufzählen"))["Anzahl bei N"] == "21.147"
    assert next(r for r in ev.way_rows(ev.analyse(ev.Settings("Permutationen", 7))) if r["Weg"].startswith("Aufzählen"))["Anzahl bei N"] == "5.040"


def test_playground_clamps_its_input():
    res = ev.playground(500, 0, 99)
    assert (res["n"], res["k"], res["c"]) == (C.PLAY_MAX, 1, C.PLAY_MAX)
    small = ev.playground(-1, 99, 0)
    assert (small["n"], small["k"], small["c"]) == (1, C.PLAY_MAX, 1) and small["surjections"] == 0 and small["cluster"] == 0 and ev.verdict_playground(small)[0] == "success"
