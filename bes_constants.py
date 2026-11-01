"""Konstanten: Regler-Grenzen, feste Annahmen, Farben und Presets."""

FAMILIES = ("Mengenpartitionen", "Permutationen", "Wurzelbäume")
DEFAULT_FAMILY = "Mengenpartitionen"
N_MIN, N_MAX, DEFAULT_N = 1, 150, 10            # Zahl der Elemente (Marken 1 bis N) beziehungsweise Knoten
LO_MIN, LO_MAX, DEFAULT_LO = 1, 30, 1           # kleinste Blockgröße (Zykellänge)
HI_MIN, HI_MAX, DEFAULT_HI = 1, 150, 150        # größte Blockgröße (Zykellänge); 150 = keine Grenze bei N <= 150
K_MIN, K_MAX, DEFAULT_K = 0, 150, 0             # genau k Blöcke (Zyklen); 0 = beliebig viele

FRACTION_BUDGET = 60_000                         # zweiter Weg mit Brüchen nur, wenn k·(n+1)² darunter liegt (Rechenzeit)
ENUM_SETS_N = 9                                  # Aufzählen aller Mengenpartitionen bis hier
ENUM_PERMS_N = 7                                 # ... aller Permutationen bis hier
ENUM_TREES_N = 6                                 # ... aller beschrifteten Wurzelbäume (Elternfunktionen) bis hier
KIRCHHOFF_N = 40                                 # Kirchhoff-Determinante für n^(n−2) bis hier

WHY_NS = (5, 10, 15, 20)                         # Experiment 2: Bell gegen Zahlpartitionen
TREE_NS = (5, 10, 20, 40, 60)                    # ... Wurzelbäume mit und ohne Marken
TREE_RATIO_N = 60                                # ... Verlauf bis hier
DERANGEMENT_NS = (1, 2, 3, 4, 5, 6, 7, 8, 10, 20, 50, 100)   # Experiment 3
DERANGEMENT_CHECK_N = 300                        # D_n = Rundung von n!/e bis hier
E_TERMS = 420                                    # Summanden der Reihe für e als Bruch
ROW_N = 10                                       # Experiment 4: Zeilen S(n,k) und c(n,k) für dieses n
ROW_TOP = 5                                      # ... so viele größte Zyklentypen werden gezeigt
EFFORT_NS = (100, 200, 500, 1000)                # Experiment 5
TIME_NS = (200, 300, 500)                        # ... gemessene Zeit (nur auf Klick, nicht getestet)
PLAY_MAX = 30                                    # Spielwiese: n, k, c bis hier
PLAY_BRUTE_LIMIT = 100_000                       # ... Aufzählen der Zuordnungen, wenn k^n darunter liegt

COLOR_MAIN = "#2F6B65"
COLOR_ALL = "rgba(150,150,150,0.75)"
COLOR_WARN = "#c0504d"
COLOR_LINE = "#4c78a8"

PRESETS = {
    "Standardfall: Bell-Zahl von 10": {"family": "Mengenpartitionen", "n": 10, "lo": 1, "hi": 150, "k": 0},
    "Clustering: 10 Punkte in 3 Cluster": {"family": "Mengenpartitionen", "n": 10, "lo": 1, "hi": 150, "k": 3},
    "Packen: 12 Gegenstände, Gruppen bis 4": {"family": "Mengenpartitionen", "n": 12, "lo": 1, "hi": 4, "k": 0},
    "Dreiergruppen: 12 Personen": {"family": "Mengenpartitionen", "n": 12, "lo": 3, "hi": 3, "k": 0},
    "Turnier: 8 Mannschaften in Paare": {"family": "Mengenpartitionen", "n": 8, "lo": 2, "hi": 2, "k": 0},
    "Derangements von 10": {"family": "Permutationen", "n": 10, "lo": 2, "hi": 150, "k": 0},
    "Involutionen von 10": {"family": "Permutationen", "n": 10, "lo": 1, "hi": 2, "k": 0},
    "Permutationen mit 3 Zyklen (Stirling erster Art)": {"family": "Permutationen", "n": 10, "lo": 1, "hi": 150, "k": 3},
    "Beschriftete Wurzelbäume (Cayley)": {"family": "Wurzelbäume", "n": 10, "lo": 1, "hi": 150, "k": 0},
}
PRESET_HELP = {
    "Standardfall: Bell-Zahl von 10": "Auf wie viele Weisen lassen sich 10 verschiedene Elemente in Gruppen ohne Reihenfolge zerlegen? 115.975 (Bell-Zahl), gegen 42 Zahlpartitionen ohne Marken.",
    "Clustering: 10 Punkte in 3 Cluster": "10 verschiedene Punkte in genau 3 nichtleere Cluster: 9.330 Zerlegungen (Stirling-Zahl zweiter Art). Der Suchraum eines Clusterverfahrens.",
    "Packen: 12 Gegenstände, Gruppen bis 4": "12 verschiedene Gegenstände in beliebig viele Gruppen mit höchstens 4 Gegenständen: 3.305.017 Zerlegungen.",
    "Dreiergruppen: 12 Personen": "12 Personen in vier Dreiergruppen: 12!/(3!⁴·4!) = 15.400.",
    "Turnier: 8 Mannschaften in Paare": "8 Mannschaften in 4 Paare: 7·5·3·1 = 105 Paarungen.",
    "Derangements von 10": "Permutationen ohne Fixpunkt: 1.334.961, das sind 36,8 % von 10! (gleich n!/e gerundet).",
    "Involutionen von 10": "Permutationen, die ihre eigene Umkehrung sind (nur Zyklen der Länge 1 und 2): 9.496.",
    "Permutationen mit 3 Zyklen (Stirling erster Art)": "Permutationen von 10 Elementen mit genau 3 Zyklen: 1.172.700 (Stirling-Zahl erster Art).",
    "Beschriftete Wurzelbäume (Cayley)": "Wurzelbäume mit 10 beschrifteten Knoten: 10⁹ = 10^(10−1); ohne Marken (Stück 5) wären es 719.",
}
