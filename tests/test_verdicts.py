"""Verdikte und Formatierung an von Hand gesetzten Werten (DEMO-PLAYBOOK §12): jede Zahl im Text und jede Schwelle der Art steht hier."""

import bes_algorithm as A
import bes_constants as C
import bes_evaluation as ev

S = ev.Settings


def test_formatting():
    assert ev.de(3.14159, 3) == "3,142" and ev.big_text(0) == "0" and ev.big_text(1234567) == "1.234.567" and ev.big_text(10 ** 12) == "1,00·10¹² (13 Stellen)"
    assert ev.times_text(12.19) == "12,2" and ev.times_text(95801.37) == "95.801" and ev.times_text(3.3e21) == "3,30·10²¹ (22 Stellen)"
    assert ev.share_text(0) == "0" and ev.share_text(1.0) == "1,0000" and ev.share_text(0.3679) == "0,3679" and ev.share_text(0.0000123) == "1,23·10⁻⁵" and ev.share_text(0.0009) == "9,00·10⁻⁴"


def test_range_text_label_and_noun():
    assert ev.range_text(3, 3) == "3" and ev.range_text(2, 5) == "2 bis 5" and ev.range_text(2, 150) == "mindestens 2"
    assert ev.label_of("Mengenpartitionen", 10, 1, 150, None) == "Bell-Zahl" and ev.label_of("Mengenpartitionen", 10, 1, 150, 3) == "Stirling-Zahl zweiter Art S(10,3)"
    assert ev.label_of("Mengenpartitionen", 10, 1, 2, None) == "Involutionszahl" and ev.label_of("Mengenpartitionen", 8, 2, 2, None) == "Zerlegungen in Paare, Doppelfakultät"
    assert ev.label_of("Mengenpartitionen", 12, 1, 4, None) is None and ev.label_of("Mengenpartitionen", 12, 3, 3, None) is None
    assert ev.label_of("Permutationen", 10, 1, 150, None) == "alle Permutationen, n!" and ev.label_of("Permutationen", 10, 1, 150, 3) == "Stirling-Zahl erster Art c(10,3)"
    assert ev.label_of("Permutationen", 10, 2, 150, None) == "Derangements" and ev.label_of("Permutationen", 10, 1, 2, None) == "Involutionen" and ev.label_of("Permutationen", 10, 3, 5, None) is None
    assert ev.label_of("Wurzelbäume", 10, 1, 150, None) == "nⁿ⁻¹ nach Cayley"
    assert ev.noun("Mengenpartitionen", 1, 150, None) == "Mengenpartitionen" and ev.noun("Mengenpartitionen", 1, 150, 3) == "Mengenpartitionen mit genau 3 Blöcken"
    assert ev.noun("Permutationen", 3, 5, 2) == "Permutationen mit Zykellänge 3 bis 5 und genau 2 Zyklen" and ev.noun("Permutationen", 2, 150, None) == "Permutationen mit Zykellänge mindestens 2"
    assert ev.noun("Mengenpartitionen", 3, 3, None) == "Mengenpartitionen mit Blockgröße 3" and ev.noun("Wurzelbäume", 1, 150, None) == "beschriftete Wurzelbäume"


def test_verdict_answers_standard_and_named_cases():
    assert ev.verdict_answers(ev.analyse(S())) == ("success", "10 verschiedene Elemente ergeben 115.975 Mengenpartitionen (Bell-Zahl). "
                                                             "3 Rechenweg(e) (Binomialfaltung (exp-Kalkül), Reihe mit Brüchen (exponentielle EGF), Bell-Dreieck) geben dieselbe Zahl.")
    text = ev.verdict_answers(ev.analyse(S("Mengenpartitionen", 10, 1, 150, 3)))[1]
    assert text.startswith("10 verschiedene Elemente ergeben 9.330 Mengenpartitionen mit genau 3 Blöcken (Stirling-Zahl zweiter Art S(10,3)).")
    text = ev.verdict_answers(ev.analyse(S("Permutationen", 10, 2, 150, 0)))[1]
    assert text.startswith("10 verschiedene Elemente ergeben 1.334.961 Permutationen mit Zykellänge mindestens 2 (Derangements).")
    assert ev.verdict_answers(ev.analyse(S("Mengenpartitionen", 12, 1, 4, 0)))[1].startswith("12 verschiedene Elemente ergeben 3.305.017 Mengenpartitionen mit Blockgröße 1 bis 4. 2 Rechenweg(e)")
    assert ev.verdict_answers(ev.analyse(S("Mengenpartitionen", 8, 2, 2, 0)))[1].startswith("8 verschiedene Elemente ergeben 105 Mengenpartitionen mit Blockgröße 2 (Zerlegungen in Paare, Doppelfakultät). 4 Rechenweg(e)")


def test_verdict_answers_for_trees_and_singular():
    kind, text = ev.verdict_answers(ev.analyse(S("Wurzelbäume", 4)))
    assert kind == "success" and text.startswith("Mit 4 Knoten gibt es 64 beschriftete Wurzelbäume; ohne Marken (Stück 5) wären es 4. 4 Rechenweg(e)")
    assert ev.verdict_answers(ev.analyse(S("Mengenpartitionen", 1)))[1].startswith("Ein Element ergibt 1 Mengenpartition (Bell-Zahl).")
    assert ev.verdict_answers(ev.analyse(S("Wurzelbäume", 1)))[1].startswith("Mit 1 Knoten gibt es 1 beschrifteten Wurzelbaum;")
    assert ev.verdict_answers(ev.analyse(S("Permutationen", 3, 1, 150, 9)))[1].startswith("3 verschiedene Elemente ergeben 0 Permutationen mit genau 9 Zyklen")


def test_verdict_answers_reports_a_disagreement_as_an_error():
    a = ev.analyse(S())
    broken = ev.Analysis(a.settings, a.n_eff, a.lo, a.hi, a.k, a.series, a.ways, a.steps, ["Aufzählen und Kalkül weichen ab"], [])
    assert ev.verdict_answers(broken) == ("error", "Die Rechenwege widersprechen sich: Aufzählen und Kalkül weichen ab")


def test_way_rows_for_a_small_case():
    rows = ev.way_rows(ev.analyse(S("Mengenpartitionen", 8, 2, 2, 0)))
    assert rows == [{"Weg": "Binomialfaltung (exp-Kalkül)", "Anzahl bei N": "105", "Schritte": "36", "Ergebnis": "gleich"},
                    {"Weg": "Reihe mit Brüchen (exponentielle EGF)", "Anzahl bei N": "105", "Schritte": "81", "Ergebnis": "gleich"},
                    {"Weg": "Formel n!/((g!)^(n/g)·(n/g)!)", "Anzahl bei N": "105", "Schritte": "1", "Ergebnis": "gleich"},
                    {"Weg": "Aufzählen aller Möglichkeiten", "Anzahl bei N": "105", "Schritte": "4.140", "Ergebnis": "gleich"}]
    assert ev.way_rows(ev.analyse(S("Mengenpartitionen", 12, 1, 4, 0)))[2] == {"Weg": "Dreieck, Rekursion oder Formel", "Anzahl bei N": "–", "Schritte": "–", "Ergebnis": "für diese Blockgrößen gibt es keine"}


def test_way_rows_flag_a_deviation():
    a = ev.analyse(S("Mengenpartitionen", 8, 2, 2, 0))
    ways = [dict(w) for w in a.ways]
    ways[0]["Wert"] = 106
    assert ev.way_rows(ev.Analysis(a.settings, a.n_eff, a.lo, a.hi, a.k, a.series, ways, a.steps, [], []))[0]["Ergebnis"] == "weicht ab"


def test_steps_of_the_main_path():
    assert ev.analyse(S("Mengenpartitionen", 10)).steps == 55 and ev.analyse(S("Mengenpartitionen", 10, 1, 150, 3)).steps == 3 * 66 == 198
    assert ev.analyse(S("Wurzelbäume", 10)).steps == 45


def test_first_values_and_share():
    a = ev.analyse(S("Permutationen", 5, 2, 150, 0))
    assert ev.first_values(a) == [{"Elemente": i, "Anzahl": str(v)} for i, v in enumerate([1, 0, 1, 2, 9, 44])]
    assert abs(ev.share_of_all(a) - 44 / 120) < 1e-15 and ev.share_of_all(ev.analyse(S("Wurzelbäume", 4))) is None
    assert abs(ev.share_of_all(ev.analyse(S("Mengenpartitionen", 4, 1, 2, 0))) - 10 / 15) < 1e-15
    big = ev.first_values(ev.analyse(S("Mengenpartitionen", 30)))
    assert [r["Elemente"] for r in big] == list(range(16)) + [30]
    trees = ev.first_values(ev.analyse(S("Wurzelbäume", 4)))
    assert [r["Elemente"] for r in trees] == [1, 2, 3, 4] and [r["Anzahl"] for r in trees] == ["1", "2", "9", "64"]


def test_why_rows_and_verdict():
    rows, trees = ev.why_rows(), ev.tree_why_rows()
    assert [(r["n"], r["Bell-Zahl (mit Marken)"], r["Zahlpartitionen (ohne Marken, Stück 5)"]) for r in rows] == [(5, 52, 7), (10, 115975, 42), (15, 1382958545, 176), (20, 51724158235372, 627)]
    assert [(r["n"], r["beschriftet"], r["unbeschriftet (Stück 5)"]) for r in trees][:3] == [(5, 625, 9), (10, 10 ** 9, 719), (20, 20 ** 19, 12826228)]
    assert [round(r["beschriftet / (n!·unbeschriftet)"], 4) for r in trees] == [0.5787, 0.3833, 0.168, 0.0316, 0.0059]
    kind, text = ev.verdict_why(rows, trees)
    assert kind == "warning" and text.startswith("Bei n = 20 gibt es 5,17·10¹³ (14 Stellen) Mengenpartitionen, aber nur 627 Zahlpartitionen") and "bei n = 60 ist das Verhältnis beschriftet / (n!·unbeschriftet) nur 0,0059" in text
    series = ev.tree_ratio_series()
    assert series["n"][0] == 1 and series["n"][-1] == C.TREE_RATIO_N and series["Verhältnis"][0] == 1.0 and series["Verhältnis"][-1] < series["Verhältnis"][0]


def test_derangement_rows_and_verdict():
    rows = ev.derangement_rows()
    assert [(r["n"], r["D_n"]) for r in rows][:8] == [(1, 0), (2, 1), (3, 2), (4, 9), (5, 44), (6, 265), (7, 1854), (8, 14833)]
    assert all(0 <= r["Fehler·(n+1)!"] < 1 for r in rows) and abs(rows[-1]["D_n / n!"] - 0.36787944117144233) < 1e-15
    assert ev.derangement_check() == []
    kind, text = ev.verdict_derangements(rows, [])
    assert kind == "success" and text.startswith("D₁₀ = 1.334.961, also 36,79 % aller Permutationen;") and "für n = 1 bis 300 die Rundung von n!/e" in text
    assert ev.verdict_derangements(rows, ["n = 5: D_n weicht ab"])[0] == "error"


def test_row_experiment_and_verdict():
    res = ev.row_experiment()
    assert res["S"][:3] == [1, 511, 9330] and res["c"][:3] == [362880, 1026576, 1172700] and res["types"] == 42 and res["perms"] == 3628800 and res["bell"] == 115975
    assert res["top"][0] == {"Zyklentyp": "9 + 1", "Permutationen": 403200} and res["top"][1] == {"Zyklentyp": "10", "Permutationen": 362880} and len(res["top"]) == C.ROW_TOP
    assert ev.row_checks(res) == []
    kind, text = ev.verdict_rows(res, [])
    assert kind == "success" and "fallen in nur 42 Zyklentypen" in text and "die größte Klasse ist 9 + 1 mit 403.200 Permutationen" in text and "H_10 = 2,9290" in text
    assert ev.verdict_rows(res, ["x"])[0] == "error"
    assert ev.row_checks(dict(res, S=[1] * 10))
    assert ev.row_checks(dict(res, c=[1] * 10))


def test_effort_rows_and_verdict():
    rows = ev.effort_rows()
    assert [r["n"] for r in rows] == list(C.EFFORT_NS) and [r["Summanden exp-Kalkül"] for r in rows] == [5050, 20100, 125250, 500500] == [r["Additionen Bell-Dreieck"] for r in rows]
    assert [r["Stellen von B(n)"] for r in rows] == [116, 276, 844, 1928]
    kind, text = ev.verdict_effort(rows)
    assert kind == "success" and text.startswith("Für n = 1000 sind es 500.500 Summanden im exp-Kalkül und ebenso viele Additionen im Bell-Dreieck; die Bell-Zahl hat 1.928 Stellen")


def test_time_experiment_shape_and_verdict_text():
    rows = [{"n": 200, "exp-Kalkül (Sekunden)": 0.04, "Bell-Dreieck (Sekunden)": 0.002}, {"n": 500, "exp-Kalkül (Sekunden)": 1.0, "Bell-Dreieck (Sekunden)": 0.05}]
    assert ev.verdict_time(rows) == ("info", "Gemessen auf diesem Rechner (Python): n = 500: exp-Kalkül 1,000 s, Bell-Dreieck 0,050 s (etwa das 20-fache). Eine Messung, keine Garantie.")
    res = ev.time_experiment()
    assert [r["n"] for r in res] == list(C.TIME_NS) and all(r["exp-Kalkül (Sekunden)"] >= 0 and r["Bell-Dreieck (Sekunden)"] >= 0 for r in res)


def test_playground_rows_and_verdict():
    res = ev.playground(10, 3, 4)
    assert (res["cluster"], res["cluster_cap"], res["pack"], res["surjections"], res["all"], res["bell"]) == (9330, 3675, 99146, 55980, 59049, 115975)
    assert res["sieve"] == res["brute"] == 55980
    assert ev.playground_rows(res)[0] == {"Frage": "10 Punkte in genau 3 nichtleere Cluster (Clustering)", "Anzahl": "9.330"} and ev.playground_rows(res)[4]["Anzahl"] == "59.049"
    assert ev.verdict_playground(res) == ("success", "55.980 von 59.049 Zuordnungen (94,8 %) lassen keine Maschine leer; Aufzählen und Siebformel bestätigen k!·S(n,k). Der Suchraum der Zerlegungen: 115.975 Mengenpartitionen von 10 Elementen insgesamt.")
    big = ev.playground(12, 3, 4)
    assert big["brute"] is None and ev.verdict_playground(big)[1].startswith("519.156 von 531.441 Zuordnungen (97,7 %) lassen keine Maschine leer; die Siebformel bestätigt")
    assert ev.verdict_playground(dict(res, sieve=1))[0] == "error" and ev.verdict_playground(dict(res, brute=1))[0] == "error"
    assert res["cluster_cap"] == A.l_pow_over_fact(A.blocks("Mengenpartitionen", 1, 4, 10), 3, 10)[10]
