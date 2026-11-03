"""Kennzahlen, Experimente und Verdikte. Jedes Verdikt ist eine reine Funktion (Art, Text); die App ruft st.<Art>(Text)."""

import math
import time
from dataclasses import dataclass
from fractions import Fraction

import bes_algorithm as A
import bes_constants as C
from bes_scenario import normalise

_SUPER = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


@dataclass(frozen=True)
class Settings:
    family: str = C.DEFAULT_FAMILY
    n: int = C.DEFAULT_N
    lo: int = C.DEFAULT_LO
    hi: int = C.DEFAULT_HI
    k: int = C.DEFAULT_K


@dataclass(frozen=True, eq=False)
class Analysis:
    settings: Settings
    n_eff: int
    lo: int
    hi: int
    k: object                              # None (beliebig viele Blöcke) oder genau k
    series: list                           # Zahl der Strukturen mit 0..N Elementen (Wurzelbäume: t_0 = 0)
    ways: list                             # Rechenwege: {"Weg", "Wert", "Schritte", "Grund"}
    steps: int                             # Schritte des Hauptwegs
    problems: list                         # Meldungen des Vergleichs der Rechenwege
    notes: list                            # Hinweise zu begrenzten Eingaben


# ----------------------------------------------------------------------------- Formatierung

def de(x: float, digits: int = 2) -> str:
    return f"{x:.{digits}f}".replace(".", ",")


def big_text(x: int) -> str:
    """Ganze Zahl lesbar: bis 12 Stellen mit Tausenderpunkt, darüber Mantisse mal Zehnerpotenz mit Stellenzahl (ohne Stringumwandlung der ganzen Zahl)."""
    if x < 10 ** 12:
        return f"{x:,}".replace(",", ".")
    d = A.digit_count(x)
    s = str(x // 10 ** (d - 3))
    return f"{s[0]},{s[1:3]}·10{str(d - 1).translate(_SUPER)} ({d} Stellen)"


def times_text(x: float) -> str:
    if x < 1000:
        return de(x, 1)
    if x < 10 ** 12:
        return f"{round(x):,}".replace(",", ".")
    return big_text(round(x))


def share_text(x: float) -> str:
    """Anteil als Zahl zwischen 0 und 1: vier Nachkommastellen, sehr kleine Anteile als Zehnerpotenz."""
    if x == 0:
        return "0"
    if x >= 0.001:
        return de(x, 4)
    mant, exp = f"{x:.2e}".split("e")
    return f"{mant.replace('.', ',')}·10{str(int(exp)).translate(_SUPER)}"


def range_text(lo: int, hi: int) -> str:
    """Größenbereich als Text: 3, 2 bis 5 oder mindestens 2 (wenn es keine obere Grenze gibt)."""
    if lo == hi:
        return str(lo)
    if hi >= C.HI_MAX:
        return f"mindestens {lo}"
    return f"{lo} bis {hi}"


def label_of(family: str, n: int, lo: int, hi: int, k):
    """Bekannter Name der gezählten Zahl für diese Einstellung, sonst None."""
    full = hi >= n
    if family == "Wurzelbäume":
        return "nⁿ⁻¹ nach Cayley"
    if family == "Mengenpartitionen":
        if lo == 1 and full:
            return "Bell-Zahl" if k is None else f"Stirling-Zahl zweiter Art S({n},{k})"
        if k is None and lo == 1 and hi == 2:
            return "Involutionszahl"
        if k is None and lo == hi == 2:
            return "Zerlegungen in Paare, Doppelfakultät"
        return None
    if lo == 1 and full:
        return "alle Permutationen, n!" if k is None else f"Stirling-Zahl erster Art c({n},{k})"
    if k is None and lo == 2 and full:
        return "Derangements"
    if k is None and lo == 1 and hi == 2:
        return "Involutionen"
    return None


def noun(family: str, lo: int, hi: int, k) -> str:
    if family == "Wurzelbäume":
        return "beschriftete Wurzelbäume"
    word = "Mengenpartitionen" if family == "Mengenpartitionen" else "Permutationen"
    unit = "Blöcken" if family == "Mengenpartitionen" else "Zyklen"
    size = "Blockgröße" if family == "Mengenpartitionen" else "Zykellänge"
    text = word
    ranged = lo > 1 or hi < C.HI_MAX
    if ranged:
        text += f" mit {size} {range_text(lo, hi)}"
    if k is not None:
        text += f" {'und' if ranged else 'mit'} genau {k} {unit}"
    return text


# ----------------------------------------------------------------------------- Analyse der eingestellten Aufgabe

def _total(family: str, n: int) -> int:
    return A.bell_triangle(n)[n] if family == "Mengenpartitionen" else math.factorial(n)


def analyse(s: Settings) -> Analysis:
    n, lo, hi, k, notes = normalise(s.family, s.n, s.lo, s.hi, s.k)
    ways, problems = [], []

    def add(name, value, steps, reason=""):
        ways.append({"Weg": name, "Wert": value, "Schritte": steps, "Grund": reason})

    if s.family == "Wurzelbäume":
        series = A.labelled_rooted_trees(n)
        steps = n * (n - 1) // 2
        add("Kalkül T = z·exp(T)", series[n], steps)
        add("Formel von Cayley nⁿ⁻¹", n ** (n - 1), 1)
        if any(series[m] != m ** (m - 1) for m in range(1, n + 1)):
            problems.append("Kalkül und Cayley-Formel weichen ab")
        if n <= C.KIRCHHOFF_N:
            kir = n * A.kirchhoff_trees(n)
            add("Kirchhoff (Spannbäume von Kₙ mal n Wurzeln)", kir, n ** 3)
            if kir != series[n]:
                problems.append(f"Kirchhoff ({kir}) und Kalkül ({series[n]}) weichen bei n = {n} ab")
        else:
            add("Kirchhoff (Spannbäume von Kₙ mal n Wurzeln)", None, None, f"nur bis n = {C.KIRCHHOFF_N}")
        if n <= C.ENUM_TREES_N:
            count = A.enumerate_rooted_trees(n)
            add("Aufzählen aller Elternfunktionen", count, n ** n)
            if count != series[n]:
                problems.append(f"Aufzählen ({count}) und Kalkül ({series[n]}) weichen bei n = {n} ab")
        else:
            add("Aufzählen aller Elternfunktionen", None, None, f"nur bis n = {C.ENUM_TREES_N}")
        return Analysis(s, n, lo, hi, k, series, ways, steps, problems, notes)

    series = A.structures(s.family, lo, hi, k, n)
    steps = A.exp_steps(n) if k is None else k * A.mul_steps(n)
    add("Binomialfaltung (exp-Kalkül)", series[n], steps)
    a = A.blocks(s.family, lo, hi, n)
    cost = (1 if k is None else k) * (n + 1) ** 2
    if cost <= C.FRACTION_BUDGET:
        frac = A.egf_fraction_exp(a, n) if k is None else A.egf_fraction_power(a, k, n)
        add("Reihe mit Brüchen (exponentielle EGF)", frac[n], cost)
        if frac != series:
            problems.append("Reihe mit Brüchen und Binomialfaltung weichen ab")
    else:
        add("Reihe mit Brüchen (exponentielle EGF)", None, None, "übersprungen: zu viele Rechenschritte")
    known = A.known_value(s.family, lo, hi, k, n)
    if known is not None:
        name, value = known
        add(name, value, n * (n + 1) // 2 if "Dreieck" in name else n if "Rekursion" in name else 1)
        if value != series[n]:
            problems.append(f"{name} ({value}) und Binomialfaltung ({series[n]}) weichen bei n = {n} ab")
    else:
        add("Dreieck, Rekursion oder Formel", None, None, "für diese Blockgrößen gibt es keine")
    limit = C.ENUM_SETS_N if s.family == "Mengenpartitionen" else C.ENUM_PERMS_N
    if n <= limit:
        count = A.enumerate_count(s.family, lo, hi, k, n)
        add("Aufzählen aller Möglichkeiten", count, _total(s.family, n))
        if count != series[n]:
            problems.append(f"Aufzählen ({count}) und Binomialfaltung ({series[n]}) weichen bei n = {n} ab")
    else:
        add("Aufzählen aller Möglichkeiten", None, None, f"nur bis n = {limit}")
    return Analysis(s, n, lo, hi, k, series, ways, steps, problems, notes)


def way_rows(a: Analysis) -> list[dict]:
    """Tabelle der Rechenwege: Wert bei N, Schritte, Übereinstimmung."""
    rows = []
    reference = a.series[a.n_eff]
    for w in a.ways:
        if w["Wert"] is None:
            rows.append({"Weg": w["Weg"], "Anzahl bei N": "–", "Schritte": "–", "Ergebnis": w["Grund"]})
        else:
            rows.append({"Weg": w["Weg"], "Anzahl bei N": big_text(w["Wert"]), "Schritte": big_text(w["Schritte"]), "Ergebnis": "gleich" if w["Wert"] == reference else "weicht ab"})
    return rows


def first_values(a: Analysis, count: int = 16) -> list[dict]:
    """Die ersten Werte der Reihe (und der letzte), als Tabelle."""
    start = 1 if a.settings.family == "Wurzelbäume" else 0
    idx = list(range(start, min(a.n_eff, start + count - 1) + 1))
    if a.n_eff not in idx:
        idx.append(a.n_eff)
    return [{"Elemente": i, "Anzahl": big_text(a.series[i])} for i in idx]


def share_of_all(a: Analysis):
    """Anteil an allen Mengenpartitionen beziehungsweise Permutationen (None bei Wurzelbäumen)."""
    if a.settings.family == "Wurzelbäume":
        return None
    return a.series[a.n_eff] / _total(a.settings.family, a.n_eff)


def _one(text: str) -> str:
    """Einzahl für genau eine Struktur."""
    return text.replace("Mengenpartitionen", "Mengenpartition", 1).replace("Permutationen", "Permutation", 1)


def verdict_answers(a: Analysis):
    s = a.settings
    c = a.series[a.n_eff]
    if a.problems:
        return "error", "Die Rechenwege widersprechen sich: " + "; ".join(a.problems)
    checked = [w["Weg"] for w in a.ways if w["Wert"] is not None]
    if s.family == "Wurzelbäume":
        what = "beschriftete Wurzelbäume" if c != 1 else "beschrifteten Wurzelbaum"
        head = f"Mit {a.n_eff} Knoten gibt es {big_text(c)} {what}; ohne Marken (Stück 5) wären es {big_text(A.unlabelled_rooted_trees(a.n_eff)[a.n_eff])}."
    else:
        label = label_of(s.family, a.n_eff, a.lo, a.hi, a.k)
        subject = f"{a.n_eff} verschiedene Elemente ergeben" if a.n_eff > 1 else "Ein Element ergibt"
        what = noun(s.family, a.lo, a.hi, a.k)
        head = f"{subject} {big_text(c)} {_one(what) if c == 1 else what}" + (f" ({label})." if label else ".")
    return "success", f"{head} {len(checked)} Rechenweg(e) ({', '.join(checked)}) geben dieselbe Zahl."


# ----------------------------------------------------------------------------- Experiment 2: warum Marken?

def why_rows() -> list[dict]:
    top = max(C.WHY_NS)
    bell, p = A.bell_triangle(top), A.partition_numbers(top)
    return [{"n": n, "Bell-Zahl (mit Marken)": bell[n], "Zahlpartitionen (ohne Marken, Stück 5)": p[n], "Faktor": bell[n] / p[n]} for n in C.WHY_NS]


def tree_why_rows() -> list[dict]:
    top = max(C.TREE_NS)
    lab, unl = A.labelled_rooted_trees(top), A.unlabelled_rooted_trees(top)
    return [{"n": n, "beschriftet": lab[n], "unbeschriftet (Stück 5)": unl[n], "Faktor": lab[n] / unl[n], "beschriftet / (n!·unbeschriftet)": lab[n] / (math.factorial(n) * unl[n])} for n in C.TREE_NS]


def tree_ratio_series() -> dict:
    top = C.TREE_RATIO_N
    lab, unl = A.labelled_rooted_trees(top), A.unlabelled_rooted_trees(top)
    ns = list(range(1, top + 1))
    return {"n": ns, "Verhältnis": [lab[n] / (math.factorial(n) * unl[n]) for n in ns]}


def verdict_why(rows: list[dict], trees: list[dict]):
    r, t = rows[-1], trees[-1]
    return "warning", (f"Bei n = {r['n']} gibt es {big_text(r['Bell-Zahl (mit Marken)'])} Mengenpartitionen, aber nur {big_text(r['Zahlpartitionen (ohne Marken, Stück 5)'])} Zahlpartitionen: "
                       f"die Methode ohne Marken zählt etwas anderes. Auch „n! mal unbeschriftet“ trifft die beschrifteten Bäume nicht: bei n = {t['n']} ist das Verhältnis beschriftet / (n!·unbeschriftet) nur {de(t['beschriftet / (n!·unbeschriftet)'], 4)}, "
                       "denn die meisten unbeschrifteten Bäume haben Symmetrie (Stück 11).")


# ----------------------------------------------------------------------------- Experiment 3: Derangements

def derangement_rows() -> list[dict]:
    e = sum(Fraction(1, math.factorial(j)) for j in range(C.E_TERMS))
    top = max(C.DERANGEMENT_NS)
    d = A.derangements(top)
    rows = []
    for n in C.DERANGEMENT_NS:
        err = abs(Fraction(d[n], math.factorial(n)) - 1 / e) * math.factorial(n + 1)
        rows.append({"n": n, "D_n": d[n], "D_n / n!": d[n] / math.factorial(n), "Fehler·(n+1)!": float(err)})
    return rows


def derangement_check() -> list[str]:
    """D_n gleich der Rundung von n!/e für n = 1..DERANGEMENT_CHECK_N, und die Rekursion gleich der Reihe SET(CYC mit Länge ≥ 2)."""
    e = sum(Fraction(1, math.factorial(j)) for j in range(C.E_TERMS))
    top = C.DERANGEMENT_CHECK_N
    d = A.derangements(top)
    problems = [f"n = {n}: D_n weicht von der Rundung von n!/e ab" for n in range(1, top + 1) if d[n] != round(Fraction(math.factorial(n)) / e)]
    series = A.structures("Permutationen", 2, top, None, 40)
    if series != d[:41]:
        problems.append("Reihe SET(CYC ≥ 2) und Rekursion weichen ab")
    return problems


def verdict_derangements(rows: list[dict], problems: list[str]):
    if problems:
        return "error", "Die Derangement-Zahlen widersprechen n!/e: " + "; ".join(problems)
    r = next(x for x in rows if x["n"] == 10)
    return "success", (f"D₁₀ = {big_text(r['D_n'])}, also {de(100 * r['D_n / n!'], 2)} % aller Permutationen; ab n = 4 hängt die Wahrscheinlichkeit D_n/n! kaum von n ab (1/e = 0,36788) und der Fehler bleibt unter 1/(n+1)! (ein Satz; "
                       f"gemessen für die angezeigten n: höchstens das {de(max(x['Fehler·(n+1)!'] for x in rows), 4)}-fache). D_n ist für n = 1 bis {C.DERANGEMENT_CHECK_N} die Rundung von n!/e.")


# ----------------------------------------------------------------------------- Experiment 4: Stirling-Zeilen und Zyklentypen

def row_experiment() -> dict:
    n = C.ROW_N
    s2, s1 = A.stirling2_triangle(n), A.stirling1_triangle(n)
    types = A.cycle_type_counts(n)
    top = sorted(types.items(), key=lambda kv: (-kv[1], kv[0]))[: C.ROW_TOP]
    return {"n": n, "S": s2[n][1:n + 1], "c": s1[n][1:n + 1], "bell": A.bell_triangle(n)[n], "types": len(types), "perms": math.factorial(n),
            "top": [{"Zyklentyp": " + ".join(str(x) for x in t), "Permutationen": v} for t, v in top], "H": sum(Fraction(1, j) for j in range(1, n + 1))}


def row_checks(res: dict) -> list[str]:
    n = res["n"]
    problems = []
    if sum(res["S"]) != res["bell"]:
        problems.append("Summe der Stirling-Zahlen zweiter Art ist nicht die Bell-Zahl")
    if sum(res["c"]) != res["perms"]:
        problems.append("Summe der Stirling-Zahlen erster Art ist nicht n!")
    if sum(res["S"]) != A.structures("Mengenpartitionen", 1, n, None, n)[n]:
        problems.append("Bell-Zahl weicht vom Kalkül ab")
    if sum(A.cycle_type_counts(n).values()) != res["perms"]:
        problems.append("Zyklentypen ergeben nicht n!")
    if Fraction(sum((k + 1) * v for k, v in enumerate(res["c"])), res["perms"]) != res["H"]:
        problems.append("mittlere Zahl der Zyklen ist nicht H_n")
    return problems


def verdict_rows(res: dict, problems: list[str]):
    if problems:
        return "error", "Die Zeilen widersprechen den Summenregeln: " + "; ".join(problems)
    top = res["top"][0]
    return "success", (f"Für n = {res['n']}: Zeilensumme der Stirling-Zahlen zweiter Art = Bell-Zahl {big_text(res['bell'])}, der ersten Art = n! = {big_text(res['perms'])}. "
                       f"Die {big_text(res['perms'])} Permutationen fallen in nur {res['types']} Zyklentypen (die Zahlpartitionen aus Stück 5); die größte Klasse ist {top['Zyklentyp']} mit {big_text(top['Permutationen'])} Permutationen. "
                       f"Die mittlere Zahl der Zyklen ist H_{res['n']} = {de(float(res['H']), 4)}.")


# ----------------------------------------------------------------------------- Experiment 5: Aufwand

def effort_rows() -> list[dict]:
    top = max(C.EFFORT_NS)
    bell = A.bell_triangle(top)
    return [{"n": n, "Summanden exp-Kalkül": A.exp_steps(n), "Additionen Bell-Dreieck": A.bell_triangle_steps(n), "Stellen von B(n)": A.digit_count(bell[n]), "Mengenpartitionen B(n)": bell[n]} for n in C.EFFORT_NS]


def verdict_effort(rows: list[dict]):
    last = rows[-1]
    return "success", (f"Für n = {last['n']} sind es {big_text(last['Summanden exp-Kalkül'])} Summanden im exp-Kalkül und ebenso viele Additionen im Bell-Dreieck; die Bell-Zahl hat {big_text(last['Stellen von B(n)'])} Stellen, "
                       "Aufzählen aller Mengenpartitionen wäre unmöglich. Gleich viele Schritte heißt nicht gleich viel Zeit: der Kalkül berechnet in dieser Implementierung Binomialkoeffizienten neu und multipliziert große Zahlen, das Dreieck addiert nur (Zeit auf Klick).")


def time_experiment() -> list[dict]:
    rows = []
    for n in C.TIME_NS:
        a = A.blocks("Mengenpartitionen", 1, n, n)
        t0 = time.perf_counter()
        A.l_exp(a, n)
        t1 = time.perf_counter()
        A.bell_triangle(n)
        t2 = time.perf_counter()
        rows.append({"n": n, "exp-Kalkül (Sekunden)": t1 - t0, "Bell-Dreieck (Sekunden)": t2 - t1})
    return rows


def verdict_time(rows: list[dict]):
    last = rows[-1]
    return "info", (f"Gemessen auf diesem Rechner (Python): n = {last['n']}: exp-Kalkül {de(last['exp-Kalkül (Sekunden)'], 3)} s, Bell-Dreieck {de(last['Bell-Dreieck (Sekunden)'], 3)} s "
                    f"(etwa das {de(last['exp-Kalkül (Sekunden)'] / max(last['Bell-Dreieck (Sekunden)'], 1e-9), 0)}-fache). Eine Messung, keine Garantie.")


# ----------------------------------------------------------------------------- Spielwiese: Zuordnen, Clustern, Packen

def playground(n: int, k: int, c: int) -> dict:
    n = max(1, min(n, C.PLAY_MAX))
    k = max(1, min(k, C.PLAY_MAX))
    c = max(1, min(c, C.PLAY_MAX))
    s2 = A.stirling2_triangle(n)
    cluster = s2[n][k] if k <= n else 0
    capped_blocks = A.blocks("Mengenpartitionen", 1, c, n)
    cluster_cap = A.l_pow_over_fact(capped_blocks, k, n)[n]
    pack = A.l_exp(capped_blocks, n)[n]
    surj = math.factorial(k) * cluster
    brute = A.enumerate_surjections(n, k) if k ** n <= C.PLAY_BRUTE_LIMIT else None
    return {"n": n, "k": k, "c": c, "cluster": cluster, "cluster_cap": cluster_cap, "pack": pack, "surjections": surj, "all": k ** n,
            "sieve": A.surjections_sieve(n, k), "brute": brute, "bell": A.bell_triangle(n)[n]}


def playground_rows(res: dict) -> list[dict]:
    return [
        {"Frage": f"{res['n']} Punkte in genau {res['k']} nichtleere Cluster (Clustering)", "Anzahl": big_text(res["cluster"])},
        {"Frage": f"... und jeder Cluster höchstens {res['c']} Punkte", "Anzahl": big_text(res["cluster_cap"])},
        {"Frage": f"{res['n']} Gegenstände in beliebig viele Gruppen der Größe höchstens {res['c']} (Packen)", "Anzahl": big_text(res["pack"])},
        {"Frage": f"{res['n']} Aufgaben auf {res['k']} verschiedene Maschinen, jede mindestens eine (Zuordnung)", "Anzahl": big_text(res["surjections"])},
        {"Frage": f"{res['n']} Aufgaben auf {res['k']} Maschinen, beliebig", "Anzahl": big_text(res["all"])},
    ]


def verdict_playground(res: dict):
    if res["surjections"] != res["sieve"]:
        return "error", f"k!·S(n,k) ({res['surjections']}) und die Siebformel ({res['sieve']}) weichen ab."
    if res["brute"] is not None and res["brute"] != res["surjections"]:
        return "error", f"Aufzählen ({res['brute']}) und k!·S(n,k) ({res['surjections']}) weichen ab."
    share = res["surjections"] / res["all"]
    check = "Aufzählen und Siebformel bestätigen" if res["brute"] is not None else "die Siebformel bestätigt"
    return "success", (f"{big_text(res['surjections'])} von {big_text(res['all'])} Zuordnungen ({de(100 * share, 1)} %) lassen keine Maschine leer; {check} k!·S(n,k). "
                       f"Der Suchraum der Zerlegungen: {big_text(res['bell'])} Mengenpartitionen von {res['n']} Elementen insgesamt.")
