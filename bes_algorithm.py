"""Rechenkern: der beschriftete Baukasten mit ganzen Zahlen (Binomialfaltung, Menge, Folge, Zyklus), Stirling-, Bell- und Derangement-Zahlen, beschriftete Wurzelbäume, Aufzählen.

Eine Folge `a` bedeutet a[n] = n!·[zⁿ]A(z), also die Zahl der beschrifteten Strukturen der Größe n (die Elemente 1 bis n sind verschieden). Alle Rechnungen mit `int` und `Fraction`;
keine Gleitkommazahlen im Zählen."""

import itertools
import math
from fractions import Fraction

C = math.comb


# ----------------------------------------------------------------------------- Zahlen

def digit_count(x: int) -> int:
    """Zahl der Dezimalstellen einer ganzen Zahl x >= 0, ohne sie in einen String zu wandeln (Python begrenzt die Umwandlung auf 4300 Stellen)."""
    if x < 0:
        raise ValueError("x darf nicht negativ sein")
    d = max(1, int(x.bit_length() * 0.30102999566398))
    while 10 ** d <= x:
        d += 1
    while d > 1 and 10 ** (d - 1) > x:
        d -= 1
    return d


def log10_int(x: int) -> float:
    """Zehnerlogarithmus einer ganzen Zahl x >= 1 (auch weit über der Gleitkommagrenze), auf etwa 15 Stellen genau."""
    if x < 1:
        raise ValueError("x muss mindestens 1 sein")
    d = digit_count(x)
    if d <= 15:
        return math.log10(x)
    shift = d - 15
    return shift + math.log10(x // 10 ** shift)


# ----------------------------------------------------------------------------- Baukasten (a[0] = 0 für exp, Folge, Zyklus)

def _check(a, n_max):
    if len(a) < n_max + 1:
        raise ValueError("die Folge ist kürzer als n_max + 1")


def l_mul(a, b, n_max):
    """Produkt zweier beschrifteter Strukturen: die Marken auf die beiden Teile verteilen, c_n = Summe_k C(n, k)·a_k·b_(n−k)."""
    _check(a, n_max)
    _check(b, n_max)
    return [sum(C(n, k) * a[k] * b[n - k] for k in range(n + 1)) for n in range(n_max + 1)]


def l_exp(a, n_max):
    """Menge von Blöcken, exp(A) mit a[0] = 0: E_n = Summe_{k=1..n} C(n−1, k−1)·a_k·E_(n−k) (das Element 1 liegt in einem Block der Größe k)."""
    _check(a, n_max)
    if a[0] != 0:
        raise ValueError("a[0] muss 0 sein")
    e = [1] + [0] * n_max
    for n in range(1, n_max + 1):
        e[n] = sum(C(n - 1, k - 1) * a[k] * e[n - k] for k in range(1, n + 1))
    return e


def l_exp_pascal(a, n_max):
    """Dieselbe Summe wie `l_exp`, aber die Binomialkoeffizienten kommen aus einem vorberechneten Pascal-Dreieck (nur Additionen) statt aus `math.comb` je Summand.
    Gleiche Ergebnisse und gleiche Summandenzahl; sie zeigt, wie viel der Zeit von `l_exp` im Neuberechnen der Binomialkoeffizienten steckt."""
    _check(a, n_max)
    if a[0] != 0:
        raise ValueError("a[0] muss 0 sein")
    pascal = [[1]]
    for n in range(1, n_max):
        prev = pascal[-1]
        pascal.append([1] + [prev[i] + prev[i + 1] for i in range(n - 1)] + [1])
    e = [1] + [0] * n_max
    for n in range(1, n_max + 1):
        row = pascal[n - 1]
        e[n] = sum(row[k - 1] * a[k] * e[n - k] for k in range(1, n + 1))
    return e


def l_seq(a, n_max):
    """Folge von Blöcken, 1/(1 − A) mit a[0] = 0: S_n = Summe_{k=1..n} C(n, k)·a_k·S_(n−k) (die ersten k Marken bilden den ersten Block)."""
    _check(a, n_max)
    if a[0] != 0:
        raise ValueError("a[0] muss 0 sein")
    s = [1] + [0] * n_max
    for n in range(1, n_max + 1):
        s[n] = sum(C(n, k) * a[k] * s[n - k] for k in range(1, n + 1))
    return s


def l_cyc(a, n_max):
    """Zyklus von Blöcken, log 1/(1 − A): C' = A'·SEQ(A), also C_(n+1) = Summe_k C(n, k)·a_(k+1)·S_(n−k)."""
    _check(a, n_max + 1)
    s = l_seq(a, n_max)
    c = [0] * (n_max + 1)
    for n in range(n_max):
        c[n + 1] = sum(C(n, k) * a[k + 1] * s[n - k] for k in range(n + 1))
    return c


def l_pow_over_fact(a, k, n_max):
    """A^k / k!: genau k Blöcke ohne Reihenfolge. k = 0 gibt nur die leere Struktur."""
    _check(a, n_max)
    if k < 0:
        raise ValueError("k darf nicht negativ sein")
    p = [1] + [0] * n_max
    for _ in range(k):
        p = l_mul(p, a, n_max)
    f = math.factorial(k)
    if any(x % f for x in p):
        raise ArithmeticError("A^k ist nicht durch k! teilbar")
    return [x // f for x in p]


def exp_steps(n_max: int) -> int:
    """Zahl der Summanden von l_exp (n(n+1)/2), ohne zu rechnen."""
    return n_max * (n_max + 1) // 2


def mul_steps(n_max: int) -> int:
    """Zahl der Summanden von l_mul ((n+1)(n+2)/2), ohne zu rechnen."""
    return (n_max + 1) * (n_max + 2) // 2


def blocks(kind: str, lo: int, hi: int, n_max: int) -> list[int]:
    """Blöcke mit Größe in [lo, hi]: Mengenblock (1 Struktur je Größe) oder Zyklus ((k−1)! Strukturen der Größe k)."""
    if kind not in ("Mengenpartitionen", "Permutationen"):
        raise ValueError(f"unbekannte Art {kind!r}")
    if lo < 1 or hi < lo:
        raise ValueError("verlangt 1 <= lo <= hi")
    return [0] + [(1 if kind == "Mengenpartitionen" else math.factorial(k - 1)) if lo <= k <= hi else 0 for k in range(1, n_max + 1)]


def structures(kind: str, lo: int, hi: int, k, n_max: int) -> list[int]:
    """Zahl der Mengenpartitionen beziehungsweise Permutationen von 0..n_max Elementen mit Blockgrößen (Zykellängen) in [lo, hi], wahlweise genau k Blöcke (Zyklen)."""
    a = blocks(kind, lo, hi, n_max)
    return l_exp(a, n_max) if k is None else l_pow_over_fact(a, k, n_max)


def labelled_rooted_trees(n_max: int) -> list[int]:
    """t[n] = Zahl der beschrifteten Wurzelbäume mit n Knoten, aus T = z·exp(T): t_n = n·E_(n−1), E = exp(T)."""
    t = [0]
    e = [1]
    for n in range(1, n_max + 1):
        m = n - 1
        if m >= 1:
            e.append(sum(C(m - 1, j - 1) * t[j] * e[m - j] for j in range(1, m + 1)))
        t.append(n * e[m])
    return t


# ----------------------------------------------------------------------------- zweiter Weg: gewöhnliche Reihe mit Brüchen

def egf_fraction_exp(a, n_max):
    """exp der exponentiellen erzeugenden Funktion â_k = a_k/k! über Brüche: n·ê_n = Summe_k k·â_k·ê_(n−k); gibt n!·ê_n zurück (ganze Zahlen)."""
    _check(a, n_max)
    ah = [Fraction(a[k], math.factorial(k)) for k in range(n_max + 1)]
    e = [Fraction(1)] + [Fraction(0)] * n_max
    for n in range(1, n_max + 1):
        e[n] = sum(k * ah[k] * e[n - k] for k in range(1, n + 1)) / n
    out = []
    for n in range(n_max + 1):
        v = e[n] * math.factorial(n)
        if v.denominator != 1:
            raise ArithmeticError("n!·ê_n ist nicht ganzzahlig")
        out.append(int(v))
    return out


def egf_fraction_power(a, k, n_max):
    """Â^k / k! über Brüche (genau k Blöcke); gibt n!·Koeffizient zurück."""
    _check(a, n_max)
    ah = [Fraction(a[j], math.factorial(j)) for j in range(n_max + 1)]
    p = [Fraction(1)] + [Fraction(0)] * n_max
    for _ in range(k):
        p = [sum(p[j] * ah[n - j] for j in range(n + 1)) for n in range(n_max + 1)]
    out = []
    for n in range(n_max + 1):
        v = p[n] / math.factorial(k) * math.factorial(n)
        if v.denominator != 1:
            raise ArithmeticError("nicht ganzzahlig")
        out.append(int(v))
    return out


# ----------------------------------------------------------------------------- unabhängige Rechenwege: Dreiecke, Rekursionen, Formeln

def stirling2_triangle(n_max):
    s = [[0] * (n_max + 2) for _ in range(n_max + 1)]
    s[0][0] = 1
    for n in range(1, n_max + 1):
        for k in range(1, n + 1):
            s[n][k] = k * s[n - 1][k] + s[n - 1][k - 1]
    return s


def stirling1_triangle(n_max):
    c = [[0] * (n_max + 2) for _ in range(n_max + 1)]
    c[0][0] = 1
    for n in range(1, n_max + 1):
        for k in range(1, n + 1):
            c[n][k] = (n - 1) * c[n - 1][k] + c[n - 1][k - 1]
    return c


def bell_triangle(n_max):
    """Bell-Zahlen B(0)..B(n_max) über das Dreieck von Aitken (nur Additionen)."""
    row = [1]
    out = [1]
    for _ in range(n_max):
        new = [row[-1]]
        for x in row:
            new.append(new[-1] + x)
        row = new
        out.append(row[0])
    return out


def bell_triangle_steps(n_max: int) -> int:
    return n_max * (n_max + 1) // 2


def derangements(n_max):
    """D_n = (n − 1)·(D_(n−1) + D_(n−2))."""
    d = [1, 0]
    for n in range(2, n_max + 1):
        d.append((n - 1) * (d[n - 1] + d[n - 2]))
    return d[: n_max + 1]


def involutions(n_max):
    """a_n = a_(n−1) + (n − 1)·a_(n−2): Permutationen mit Zykeln der Länge 1 und 2 (und Paarungen mit Einzelnen)."""
    a = [1, 1]
    for n in range(2, n_max + 1):
        a.append(a[n - 1] + (n - 1) * a[n - 2])
    return a[: n_max + 1]


def known_value(kind: str, lo: int, hi: int, k, n: int):
    """Wert aus einem unabhängigen Rechenweg (Dreieck, Rekursion oder Formel), wenn es für diese Einstellung einen gibt; sonst None. Rückgabe (Name, Wert)."""
    full = hi >= n
    if kind == "Mengenpartitionen":
        if lo == 1 and full:
            if k is None:
                return "Bell-Dreieck", bell_triangle(n)[n]
            return "Stirling-Dreieck (zweite Art)", stirling2_triangle(n)[n][k] if k <= n else 0
        if k is None and lo == 1 and hi == 2:
            return "Rekursion der Involutionen", involutions(n)[n]
        if k is None and lo == hi:
            g = lo
            return "Formel n!/((g!)^(n/g)·(n/g)!)", math.factorial(n) // (math.factorial(g) ** (n // g) * math.factorial(n // g)) if n % g == 0 else 0
        return None
    if kind == "Permutationen":
        if lo == 1 and full:
            if k is None:
                return "Fakultät", math.factorial(n)
            return "Stirling-Dreieck (erste Art)", stirling1_triangle(n)[n][k] if k <= n else 0
        if k is None and lo == 2 and full:
            return "Rekursion der Derangements", derangements(n)[n]
        if k is None and lo == 1 and hi == 2:
            return "Rekursion der Involutionen", involutions(n)[n]
        return None
    return None


def kirchhoff_trees(n: int) -> int:
    """Zahl der aufspannenden Bäume von K_n (reduzierte Laplace-Determinante mit Brüchen); beschriftete Wurzelbäume sind n mal so viele."""
    if n == 1:
        return 1
    m = [[Fraction(n - 1 if i == j else -1) for j in range(n - 1)] for i in range(n - 1)]
    det = Fraction(1)
    for c in range(n - 1):
        piv = next((r for r in range(c, n - 1) if m[r][c] != 0), None)
        if piv is None:
            return 0
        if piv != c:
            m[c], m[piv] = m[piv], m[c]
            det = -det
        det *= m[c][c]
        for r in range(c + 1, n - 1):
            f = m[r][c] / m[c][c]
            m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return int(det)


# ----------------------------------------------------------------------------- Aufzählen

def set_partitions(items):
    """Alle Mengenpartitionen als Listen von Blöcken."""
    if not items:
        yield []
        return
    first, rest = items[0], items[1:]
    for p in set_partitions(rest):
        yield [[first]] + p
        for i in range(len(p)):
            yield p[:i] + [[first] + p[i]] + p[i + 1:]


def cycle_lengths(perm) -> list[int]:
    seen, out = set(), []
    for s in range(len(perm)):
        if s in seen:
            continue
        length, x = 0, s
        while x not in seen:
            seen.add(x)
            x = perm[x]
            length += 1
        out.append(length)
    return out


def enumerate_count(kind: str, lo: int, hi: int, k, n: int) -> int:
    """Zählt durch Aufzählen: alle Mengenpartitionen beziehungsweise alle Permutationen von n Elementen mit Blockgrößen in [lo, hi] (und genau k Blöcken)."""
    if kind == "Mengenpartitionen":
        parts = (len(p) for p in set_partitions(list(range(n))) if all(lo <= len(b) <= hi for b in p) and (k is None or len(p) == k))
        return sum(1 for _ in parts)
    total = 0
    for perm in itertools.permutations(range(n)):
        cl = cycle_lengths(perm)
        if all(lo <= c <= hi for c in cl) and (k is None or len(cl) == k):
            total += 1
    return total


def enumerate_rooted_trees(n: int) -> int:
    """Beschriftete Wurzelbäume durch Aufzählen aller Elternfunktionen: für jede Wurzel jede Zuordnung Elternknoten, die zu einem Baum führt."""
    count = 0
    for root in range(n):
        others = [v for v in range(n) if v != root]
        for parent in itertools.product(range(n), repeat=n - 1):
            par = dict(zip(others, parent))
            ok = True
            for v in others:
                x, steps = v, 0
                while x != root and steps <= n:
                    x = par[x]
                    steps += 1
                if x != root:
                    ok = False
                    break
            count += ok
    return count


def enumerate_surjections(n: int, k: int) -> int:
    """Zuordnungen von n Aufgaben auf k Maschinen, jede Maschine mindestens eine, durch Aufzählen."""
    return sum(1 for f in itertools.product(range(k), repeat=n) if len(set(f)) == k)


def surjections_sieve(n: int, k: int) -> int:
    """k!·S(n, k) über die Siebformel Summe_j (−1)^(k−j) C(k, j) jⁿ (Stück 7)."""
    return sum((-1) ** (k - j) * C(k, j) * j ** n for j in range(k + 1))


# ----------------------------------------------------------------------------- beschriftet gegen unbeschriftet (Stück 5)

def partition_numbers(n_max):
    """Zahlpartitionen p(0)..p(n_max) (Stück 5), zum Vergleich mit den Bell-Zahlen."""
    c = [1] + [0] * n_max
    for k in range(1, n_max + 1):
        for m in range(k, n_max + 1):
            c[m] += c[m - k]
    return c


def unlabelled_rooted_trees(n_max):
    """Wurzelbäume ohne Reihenfolge und ohne Marken (Stück 5): t[0] = 0, t[1] = 1, 1, 2, 4, 9, 20, …"""
    t = [0, 1] if n_max >= 1 else [0]
    c = [1]
    for size in range(1, n_max):
        b = [0] * (size + 1)
        for d in range(1, size + 1):
            for j in range(d, size + 1, d):
                b[j] += d * t[d]
        s = sum(b[j] * c[size - j] for j in range(1, size + 1))
        if s % size:
            raise ArithmeticError("Division geht nicht auf")
        c.append(s // size)
        t.append(c[size])
    return t


def cycle_type_counts(n: int) -> dict:
    """Zahl der Permutationen von n Elementen je Zyklentyp: n!/(Produkt j^(m_j)·m_j!)."""
    def parts(m, mx):
        if m == 0:
            yield ()
            return
        for j in range(min(m, mx), 0, -1):
            for rest in parts(m - j, j):
                yield (j,) + rest

    out = {}
    for p in parts(n, n):
        denom = 1
        for j in set(p):
            denom *= j ** p.count(j) * math.factorial(p.count(j))
        out[p] = math.factorial(n) // denom
    return out
