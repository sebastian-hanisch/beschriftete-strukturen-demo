"""Beschriftete Strukturen – wenn die Bausteine Marken tragen - interaktive Konzept-Demo
Sebastian Hanisch - Operations Research und Machine Learning

Stück 6 der Reihe „Abzählen und erzeugende Funktionen“: Der beschriftete Baukasten (Produkt als Binomialfaltung, Menge, Zyklus): Mengenpartitionen und Bell-Zahlen, Permutationen und
Derangements, Stirling-Zahlen beider Arten, beschriftete Wurzelbäume; gegen unbeschriftet (Stück 5) und auf mehreren Rechenwegen gegeneinander geprüft.
Aufbau und Regeln: DEMO-PLAYBOOK.md (§2).

Lauffähig mit: streamlit run app.py
"""

import streamlit as st

import bes_constants as C
from bes_evaluation import (
    Settings,
    analyse,
    big_text,
    de,
    derangement_check,
    derangement_rows,
    effort_rows,
    first_values,
    playground,
    playground_rows,
    row_checks,
    row_experiment,
    share_of_all,
    share_text,
    time_experiment,
    tree_ratio_series,
    tree_why_rows,
    times_text,
    verdict_answers,
    verdict_derangements,
    verdict_effort,
    verdict_playground,
    verdict_rows,
    verdict_time,
    verdict_why,
    way_rows,
    why_rows,
)
from bes_algorithm import digit_count, unlabelled_rooted_trees
from bes_layout import dunkles_design, kopf_css
from bes_pdf_export import build_pdf
from bes_presets import (
    bounds,
    init_session_state_defaults,
    load_permalink_settings,
    sidebar_presets,
    sync_query_params,
)
from bes_visualization import build_derangements, build_effort, build_growth, build_rows, build_tree_ratio, build_why

st.set_page_config(page_title="Beschriftete Strukturen – Sebastian Hanisch", layout="wide")


@st.cache_data(show_spinner=False)
def _analysis(settings):
    return analyse(settings)


@st.cache_data(show_spinner=False)
def _why():
    return why_rows(), tree_why_rows(), tree_ratio_series()


@st.cache_data(show_spinner=False)
def _derangements():
    return derangement_rows(), derangement_check()


@st.cache_data(show_spinner=False)
def _rows():
    res = row_experiment()
    return res, row_checks(res)


@st.cache_data(show_spinner=False)
def _effort():
    return effort_rows()


@st.cache_data(show_spinner=False)
def _play(n, k, c):
    return playground(n, k, c)


def verdict(pair):
    kind, text = pair
    getattr(st, kind)(text)


# Fester Kopf: nur der Titel bleibt beim Scrollen oben (Stylesheet in bes_layout.py).
st.html(kopf_css(dunkles_design()))
with st.container(key="kopf"):
    st.title("🏷️ Beschriftete Strukturen – wenn die Bausteine Marken tragen")
st.markdown(
    """
**Zählen mit Marken.** In Stück 3 und 5 war ein Baustein der Größe 2 einfach ein Baustein der Größe 2. Tragen die Elemente **Marken** (Gegenstände, Aufgaben, Punkte, Mannschaften 1 bis $n$), unterscheidet man „Element 1 mit Element 2“ von
„Element 1 mit Element 3“. Das Produkt zweier Strukturen verteilt dann die Marken auf beide Teile: eine **Binomialfaltung** $c_n = \\sum_k \\binom{n}{k}\\, a_k\\, b_{n-k}$ (hinter ihr steht die **exponentielle** erzeugende Funktion).
Aus drei Bausteinen, **Menge** (Blöcke ohne Reihenfolge), **Zyklus** (Block mit Rotation) und **Folge**, entstehen Permutationen, Derangements, Bell- und Stirling-Zahlen und beschriftete Bäume.
Wer dieselbe Aufgabe mit der Methode ohne Marken rechnet, bekommt eine **andere Zahl**: 115.975 Mengenpartitionen von 10 Elementen, aber nur 42 Zahlpartitionen von 10.

Weiter unten: **fünf Experimente** (**🔬**), eine **🎲 Spielwiese**, **🚧 Wo die Annahmen enden** und der Expander **📐 Mathematische Formulierung**.
"""
)

with st.expander("So funktioniert der beschriftete Baukasten", expanded=True):
    st.markdown(
        """
1. **Blöcke festlegen:** Ein Block der Größe $k$ ist bei den Mengenpartitionen eine ungeordnete Menge ($1$ Möglichkeit je Größe), bei den Permutationen ein Zyklus ($(k-1)!$ Möglichkeiten je Größe). Die Regler „Blockgröße von … bis“ wählen, welche Größen erlaubt sind.
2. **Blöcke zur Menge zusammenfassen:** $\\exp(A)$: Das Element 1 liegt in einem Block der Größe $k$ (dafür gibt es $\\binom{n-1}{k-1}$ Möglichkeiten, die übrigen Marken zu wählen); der Rest ist wieder eine Menge von Blöcken: $E_n = \\sum_k \\binom{n-1}{k-1}\\, a_k\\, E_{n-k}$.
3. **Genau $k$ Blöcke:** $A^k / k!$ (das Produkt von $k$ Blöcken, geteilt durch $k!$, weil die Blöcke keine Reihenfolge haben): die Stirling-Zahlen.
4. **Zweiter Weg:** dieselbe Reihe als gewöhnliche Reihe mit Brüchen, $n\\, \\hat e_n = \\sum_k k\\, \\hat a_k\\, \\hat e_{n-k}$ mit $\\hat a_k = a_k / k!$; dazu Dreiecke (Stirling, Bell), die Derangement-Rekursion und Aufzählen.
        """
    )

st.caption("🔗 Die Adresszeile oben spiegelt Ihre aktuelle Konfiguration wider – einfach kopieren, um ein Szenario zu teilen.")

load_permalink_settings()
init_session_state_defaults()

with st.sidebar:
    sidebar_presets()  # Schnellstart oben, das aktive Preset ist hervorgehoben
    st.header("⚙️ Einstellungen")
    st.markdown("**Struktur**")
    family = st.selectbox("Familie", list(C.FAMILIES), key="family_select",
                          help="Mengenpartitionen: Elemente in Gruppen ohne Reihenfolge zerlegen. Permutationen: Elemente in Zyklen anordnen. Wurzelbäume: beschriftete Bäume mit einer Wurzel (n^(n−1)).")
    n = st.slider("Zahl der Elemente N", *bounds("n_slider"), key="n_slider", help="Die Elemente tragen die Marken 1 bis N. Bei Wurzelbäumen: Zahl der Knoten.")
    lo = st.slider("Blockgröße von", *bounds("lo_slider"), key="lo_slider", help="Kleinste erlaubte Größe eines Blocks (bei Permutationen: Länge eines Zyklus). 2 bei Permutationen heißt: keine Fixpunkte.")
    hi = st.slider("Blockgröße bis", *bounds("hi_slider"), key="hi_slider", help="Größte erlaubte Größe eines Blocks; ab N ist es keine Grenze. Liegt der Wert unter „von“, wird mit „von“ gerechnet.")
    k = st.slider("Genau k Blöcke (0 = beliebig)", *bounds("k_slider"), key="k_slider", help="Mit k > 0 zählt die App nur Zerlegungen in genau k Blöcke (beziehungsweise Permutationen mit genau k Zyklen): die Stirling-Zahlen.")

sync_query_params({"family_select": family, "n_slider": int(n), "lo_slider": int(lo), "hi_slider": int(hi), "k_slider": int(k)})

settings = Settings(family, int(n), int(lo), int(hi), int(k))
a = _analysis(settings)
for note in a.notes:
    st.info(note)

# --- Ergebnis ------------------------------------------------------------------------------------------------------------------------------

st.markdown("## 🎯 Ergebnis")
c_n = a.series[a.n_eff]
m1, m2, m3, m4 = st.columns(4)
m1.metric(f"Anzahl bei {a.n_eff} Elementen", big_text(c_n), help="Wie viele beschriftete Strukturen es mit den Marken 1 bis N gibt.")
m2.metric("Stellen der Anzahl", str(digit_count(c_n)), help="Zahl der Dezimalstellen von „Anzahl bei N“.")
share = share_of_all(a)
if share is None:
    m3.metric("Ohne Marken (Stück 5)", big_text(unlabelled_rooted_trees(a.n_eff)[a.n_eff]), help="Wurzelbäume ohne Reihenfolge und ohne Marken: so viele wären es mit der Methode aus Stück 5.")
else:
    m3.metric("Anteil an allen Möglichkeiten", share_text(share), help="Anteil an allen Mengenpartitionen (Bell-Zahl) beziehungsweise allen Permutationen (N!).")
m4.metric("Schritte der Rechnung", big_text(a.steps), help="Summanden des Hauptwegs (Binomialfaltung), exakt gezählt.")
st.plotly_chart(build_growth(a.series, 1 if family == "Wurzelbäume" else 0), width="stretch", key="main_chart")
st.caption("Zehnerlogarithmus der Anzahl je Zahl der Elemente. Die Zahlen wachsen in den meisten Einstellungen schneller als jede Potenz; nur die logarithmische Achse zeigt sie.")
with st.expander("Die ersten Werte ansehen"):
    st.dataframe(first_values(a), hide_index=True, width="stretch")

if st.button("📄 PDF der aktuellen Aufgabe erstellen", key="pdf_make"):
    st.session_state["pdf_made"] = (settings, build_pdf(a))
made = st.session_state.get("pdf_made")
if made and made[0] == settings:
    st.download_button("⬇️ PDF herunterladen", data=made[1], file_name="beschriftete-strukturen.pdf", mime="application/pdf", key="pdf_download")

# --- Kernfrage -----------------------------------------------------------------------------------------------------------------------------

st.markdown("## ❓ Kernfrage: Warum braucht man die exponentielle erzeugende Funktion?")
verdict(verdict_answers(a))

st.markdown("---")

# --- Experimente ---------------------------------------------------------------------------------------------------------------------------

st.subheader("🔬 Experiment 1: Dieselben Zahlen auf allen Wegen")
st.caption(f"Die eingestellte Aufgabe auf allen Wegen, die für sie gelten: Binomialfaltung, gewöhnliche Reihe mit Brüchen (nur bei kleinem Aufwand), Dreieck, Rekursion oder Formel (nur wenn es sie gibt) und Aufzählen "
           f"(Mengenpartitionen bis N = {C.ENUM_SETS_N}, Permutationen bis N = {C.ENUM_PERMS_N}, Wurzelbäume bis N = {C.ENUM_TREES_N}). Bei Wurzelbäumen kommen die Formel von Cayley und Kirchhoffs Determinante hinzu.")
if a.problems:
    st.error("Die Rechenwege widersprechen sich: " + "; ".join(a.problems))
else:
    st.success("Alle gerechneten Wege geben dieselbe Zahl.")
st.dataframe(way_rows(a), hide_index=True, width="stretch")

st.markdown("---")

st.subheader("🔬 Experiment 2: Warum Marken?")
st.caption("Mengenpartitionen mit Marken (Bell-Zahlen) gegen Zahlpartitionen ohne Marken (Stück 5), und beschriftete gegen unbeschriftete Wurzelbäume. Der Quotient beschriftet / (n!·unbeschriftet) wäre 1, wenn jede unbeschriftete Struktur n! verschiedene Beschriftungen hätte.")
why, tree_why, ratio = _why()
st.plotly_chart(build_why(why), width="stretch", key="why_chart")
st.dataframe([{"n": r["n"], "Bell-Zahl (mit Marken)": big_text(r["Bell-Zahl (mit Marken)"]), "Zahlpartitionen (ohne Marken, Stück 5)": big_text(r["Zahlpartitionen (ohne Marken, Stück 5)"]), "Faktor": times_text(r["Faktor"])} for r in why],
             hide_index=True, width="stretch")
st.plotly_chart(build_tree_ratio(ratio), width="stretch", key="tree_ratio_chart")
st.dataframe([{"n": r["n"], "beschriftet": big_text(r["beschriftet"]), "unbeschriftet (Stück 5)": big_text(r["unbeschriftet (Stück 5)"]), "Faktor": times_text(r["Faktor"]),
               "beschriftet / (n!·unbeschriftet)": de(r["beschriftet / (n!·unbeschriftet)"], 4)} for r in tree_why], hide_index=True, width="stretch")
verdict(verdict_why(why, tree_why))

st.markdown("---")

st.subheader("🔬 Experiment 3: Derangements und n!/e")
st.caption(f"Permutationen ohne Fixpunkt als Menge von Zyklen der Länge mindestens 2. Die Zahl wird gegen die Rundung von n!/e geprüft (e als Bruch aus {C.E_TERMS} Summanden), für n = 1 bis {C.DERANGEMENT_CHECK_N}.")
der_rows, der_problems = _derangements()
st.plotly_chart(build_derangements(der_rows), width="stretch", key="derangement_chart")
st.dataframe([{"n": r["n"], "D_n": big_text(r["D_n"]), "D_n / n!": de(r["D_n / n!"], 5), "Fehler·(n+1)!": de(r["Fehler·(n+1)!"], 4)} for r in der_rows], hide_index=True, width="stretch")
verdict(verdict_derangements(der_rows, der_problems))

st.markdown("---")

st.subheader("🔬 Experiment 4: Stirling-Zeilen und Zyklentypen")
st.caption(f"Für n = {C.ROW_N}: wie viele Mengenpartitionen mit k Blöcken (zweite Art) und Permutationen mit k Zyklen (erste Art) es gibt, und in wie viele Zyklentypen die Permutationen zerfallen (jeder Typ ist eine Zahlpartition aus Stück 5).")
row_res, row_problems = _rows()
st.plotly_chart(build_rows(row_res), width="stretch", key="rows_chart")
st.dataframe([{"k": i + 1, "S(n,k)": big_text(row_res["S"][i]), "c(n,k)": big_text(row_res["c"][i])} for i in range(row_res["n"])], hide_index=True, width="stretch")
st.dataframe([{"Zyklentyp": r["Zyklentyp"], "Permutationen": big_text(r["Permutationen"])} for r in row_res["top"]], hide_index=True, width="stretch")
verdict(verdict_rows(row_res, row_problems))

st.markdown("---")

st.subheader("🔬 Experiment 5: Aufwand")
st.caption("Summanden (exakt gezählt) des exp-Kalküls und des Bell-Dreiecks gegen die Zahl der Mengenpartitionen, die Aufzählen anfassen müsste. Die Zeit messen Sie auf Klick; sie ist eine Messung dieses Rechners.")
effort = _effort()
st.plotly_chart(build_effort(effort), width="stretch", key="effort_chart")
st.dataframe([{"n": r["n"], "Summanden exp-Kalkül": big_text(r["Summanden exp-Kalkül"]), "Additionen Bell-Dreieck": big_text(r["Additionen Bell-Dreieck"]), "Stellen von B(n)": r["Stellen von B(n)"],
               "Mengenpartitionen B(n)": big_text(r["Mengenpartitionen B(n)"])} for r in effort], hide_index=True, width="stretch")
verdict(verdict_effort(effort))
if st.button("⏱️ Zeit messen", key="time_run"):
    st.session_state["time_res"] = time_experiment()
timing = st.session_state.get("time_res")
if timing:
    st.dataframe([{"n": r["n"], "exp-Kalkül (Sekunden)": de(r["exp-Kalkül (Sekunden)"], 3), "Bell-Dreieck (Sekunden)": de(r["Bell-Dreieck (Sekunden)"], 3)} for r in timing], hide_index=True, width="stretch")
    verdict(verdict_time(timing))

st.markdown("---")

# --- Spielwiese ----------------------------------------------------------------------------------------------------------------------------

st.subheader("🎲 Spielwiese: Zuordnen, Clustern, Packen")
st.caption("Dieselben Zahlen als Suchraum: Wie viele Zerlegungen und Zuordnungen gibt es, bevor ein Verfahren zu suchen beginnt?")
p1, p2, p3 = st.columns(3)
play_n = p1.slider("Elemente n", 1, C.PLAY_MAX, 10, key="play_n", help="Punkte, Aufgaben oder Gegenstände.")
play_k = p2.slider("Gruppen oder Maschinen k", 1, C.PLAY_MAX, 3, key="play_k", help="Zahl der Cluster beziehungsweise Maschinen.")
play_c = p3.slider("Höchstgröße einer Gruppe c", 1, C.PLAY_MAX, 4, key="play_c", help="Mehr als c Elemente passen nicht in eine Gruppe.")
play = _play(int(play_n), int(play_k), int(play_c))
st.dataframe(playground_rows(play), hide_index=True, width="stretch")
verdict(verdict_playground(play))

st.markdown("---")

# --- Grenzen -------------------------------------------------------------------------------------------------------------------------------

st.subheader("🚧 Wo die Annahmen enden")
st.markdown(
    f"""
| Annahme | Was passiert, wenn sie verletzt ist | Wer setzt an |
|---|---|---|
| **Die Elemente tragen unterscheidbare Marken** | Ohne Marken zählt die Methode aus Stück 5 etwas anderes: 42 Zahlpartitionen von 10 statt 115.975 Mengenpartitionen (Experiment 2). | Stück 5 der Reihe |
| **Die Blöcke haben keine Reihenfolge** | Mit Reihenfolge der Blöcke wären es geordnete Zerlegungen: $k!\\,S(n,k)$ (Surjektionen, Spielwiese). | Stück 7: Siebformel |
| **Jede Beschriftung ist eine eigene Struktur** | „Bis auf Symmetrie“ zählt anders: beschriftet / (n!·unbeschriftet) fällt bei den Wurzelbäumen von 0,58 (n = 5) auf 0,006 (n = 60), denn die meisten unbeschrifteten Bäume haben Symmetrie (Experiment 2). | Stück 11 der Reihe: Burnside und Pólya |
| **Die Blöcke sind unabhängig** | Verbotene Paare oder Nachbarschaftsbedingungen (zum Beispiel Zuordnungen in einem gegebenen Graphen) lassen sich so nicht zählen; bei 1:1-Zuordnungen mit verbotenen Paaren zählt die Permanente. | Stück 7 und die Komplexitätslinie |
| **Ganze Zahlen im Rechner** | Die Zahlen wachsen schnell: B(1000) hat 1.928 Stellen. Die App rechnet exakt, begrenzt aber den Kalkül auf N = {C.N_MAX} Elemente (Zeit). | – |
| **Nur Mengen, Zyklen und Wurzelbäume** | Beschriftete Graphen, zusammenhängende Graphen und Funktionalgraphen brauchen weitere Bausteine; die Reihe ist dann nicht mehr diese. | – |
| **Wachstum nur als Zahl** | Wie schnell B(n) und D_n/n! wachsen oder sich einpendeln, steht hier als Tabelle, nicht als Satz. | Stück 9 der Reihe: Asymptotik |
"""
)

st.markdown("---")

with st.expander("📐 Mathematische Formulierung"):
    st.markdown(
        r"""
**Beschriftet.** Eine Klasse beschrifteter Strukturen hat die exponentielle erzeugende Funktion $A(z) = \sum_n a_n z^n / n!$ mit $a_n$ = Zahl der Strukturen mit den Marken $1, \dots, n$. Das Produkt zweier Klassen (die Marken auf beide Teile verteilen) entspricht dem Produkt der Reihen:
$(A \cdot B)_n = \sum_k \binom{n}{k} a_k b_{n-k}$.

**Menge, Folge, Zyklus.**
$$\mathrm{SET}(A) = e^{A(z)}, \qquad \mathrm{SEQ}(A) = \frac{1}{1 - A(z)}, \qquad \mathrm{CYC}(A) = \log \frac{1}{1 - A(z)}.$$
Das Element 1 liegt in einem Block der Größe $k$: $E_n = \sum_{k=1}^{n} \binom{n-1}{k-1}\, a_k\, E_{n-k}$ für $E = \mathrm{SET}(A)$.

**Bekannte Folgen.** Mengenpartitionen: $\exp(e^z - 1)$, Bell-Zahlen $B_n$. Stirling-Zahlen zweiter Art: $S(n,k) = n!\,[z^n]\,(e^z - 1)^k / k!$. Permutationen: $\mathrm{SET}(\mathrm{CYC}(Z)) = \exp(\log\frac{1}{1-z}) = \frac{1}{1-z}$, also $n!$.
Stirling-Zahlen erster Art (ohne Vorzeichen): $c(n,k) = n!\,[z^n]\,(\log\frac{1}{1-z})^k / k!$, mit $\sum_k c(n,k)\, x^k = x (x+1) \cdots (x+n-1)$.
Derangements: $\mathrm{SET}(\mathrm{CYC}_{\ge 2}(Z))$ hat die erzeugende Funktion $e^{-z}/(1-z)$, also $D_n = n! \sum_{j=0}^{n} (-1)^j / j!$, und $D_n$ ist für $n \ge 1$ die nächste ganze Zahl zu $n!/e$.
Beschriftete Wurzelbäume: $T(z) = z\, e^{T(z)}$, nach der Lagrange-Inversion $t_n = n^{n-1}$.

**Surjektionen.** $k!\,S(n,k) = \sum_{j=0}^{k} (-1)^{k-j} \binom{k}{j}\, j^n$ (Siebformel).

**Zyklentypen.** Eine Permutation mit $m_j$ Zyklen der Länge $j$: $n! / \prod_j j^{m_j}\, m_j!$ Permutationen je Typ; die Typen sind die Zahlpartitionen von $n$.

**Literatur** (Titel und Fundstelle aus dem Gedächtnis, nicht eingesehen).
P. Flajolet und R. Sedgewick: *Analytic Combinatorics*, Cambridge University Press, 2009 (beschriftete Konstruktionen, exponentielle erzeugende Funktionen).
R. P. Stanley: *Enumerative Combinatorics, Volume 2*, Cambridge University Press, 1999 (Kapitel 5, exponentielle Formeln, Stirling-Zahlen).
A. Cayley: *A theorem on trees*, Quarterly Journal of Pure and Applied Mathematics 23, 1889, S. 376–378 (Formel $n^{n-2}$).
        """
    )

st.markdown("---")
st.caption(
    "Diese Demo ist Teil des Portfolios von [Sebastian Hanisch](https://sebastianhanisch.net) – "
    "Operations Research und Machine Learning ([Über mich](https://sebastianhanisch.net/ueber-mich.html)). "
    "Mehr zu den Demos: [Interaktive Demos](https://sebastianhanisch.net/demos.html)."
)
