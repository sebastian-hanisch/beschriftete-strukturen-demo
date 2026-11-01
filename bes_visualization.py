"""Plotly-Abbildungen. Alle Achsen sind gesperrt (fixedrange), damit Touch-Geräte beim Scrollen nicht am Diagramm hängen bleiben."""

import plotly.graph_objects as go

import bes_algorithm as A
import bes_constants as C


def lock_axes(fig):
    fig.update_xaxes(fixedrange=True)
    fig.update_yaxes(fixedrange=True)
    return fig


def _base(fig, height=360):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=50, b=10), legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), plot_bgcolor="rgba(0,0,0,0)")
    return lock_axes(fig)


def build_growth(series: list[int], first_index: int = 0):
    """Zehnerlogarithmus der Anzahl je Größe (die Zahlen sprengen jede lineare Achse)."""
    xs = [n for n in range(first_index, len(series)) if series[n] >= 1]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=[A.log10_int(series[n]) for n in xs], mode="lines+markers" if len(xs) <= 60 else "lines", name="Anzahl", line=dict(color=C.COLOR_MAIN)))
    fig.update_xaxes(title_text="Zahl der Elemente n")
    fig.update_yaxes(title_text="Anzahl (Zehnerlogarithmus)")
    return _base(fig, 320)


def build_why(rows: list[dict]):
    """Mengenpartitionen (mit Marken) gegen Zahlpartitionen (ohne Marken), logarithmische Achse."""
    fig = go.Figure()
    names = [str(r["n"]) for r in rows]
    fig.add_trace(go.Bar(x=names, y=[A.log10_int(r["Bell-Zahl (mit Marken)"]) for r in rows], name="mit Marken (Bell)", marker_color=C.COLOR_MAIN))
    fig.add_trace(go.Bar(x=names, y=[A.log10_int(r["Zahlpartitionen (ohne Marken, Stück 5)"]) for r in rows], name="ohne Marken (Zahlpartitionen)", marker_color=C.COLOR_ALL))
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="n")
    fig.update_yaxes(title_text="Anzahl (Zehnerlogarithmus)")
    return _base(fig, 340)


def build_tree_ratio(res: dict):
    """beschriftet / (n!·unbeschriftet) für Wurzelbäume: 1 hieße, jede Struktur hat n! verschiedene Beschriftungen."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=res["n"], y=res["Verhältnis"], mode="lines", name="beschriftet / (n!·unbeschriftet)", line=dict(color=C.COLOR_MAIN)))
    fig.add_hline(y=1, line=dict(color=C.COLOR_ALL, dash="dash"))
    fig.update_xaxes(title_text="Knoten n")
    fig.update_yaxes(title_text="Verhältnis", range=[0, 1.05])
    return _base(fig, 320)


def build_rows(res: dict):
    """Zeilen S(n, k) (zweite Art) und c(n, k) (erste Art) für festes n."""
    fig = go.Figure()
    ks = list(range(1, res["n"] + 1))
    fig.add_trace(go.Bar(x=ks, y=res["S"], name="Mengenpartitionen S(n,k)", marker_color=C.COLOR_MAIN))
    fig.add_trace(go.Bar(x=ks, y=res["c"], name="Permutationen c(n,k)", marker_color=C.COLOR_LINE))
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="Zahl k der Blöcke beziehungsweise Zyklen", dtick=1)
    fig.update_yaxes(title_text="Anzahl")
    return _base(fig, 340)


def build_derangements(rows: list[dict]):
    """D_n / n! gegen 1/e."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[r["n"] for r in rows], y=[r["D_n / n!"] for r in rows], mode="lines+markers", name="D_n / n!", line=dict(color=C.COLOR_MAIN)))
    fig.add_hline(y=0.36787944117144233, line=dict(color=C.COLOR_ALL, dash="dash"))
    fig.update_xaxes(title_text="n", type="log")
    fig.update_yaxes(title_text="Anteil der Derangements", range=[0, 0.6])
    return _base(fig, 320)


def build_effort(rows: list[dict]):
    """Zehnerlogarithmus der Summanden gegen den der Mengenpartitionen B(n) (B(1000) passt in keine Gleitkommazahl)."""
    fig = go.Figure()
    names = [str(r["n"]) for r in rows]
    fig.add_trace(go.Bar(x=names, y=[A.log10_int(r["Summanden exp-Kalkül"]) for r in rows], name="Summanden (Kalkül, Dreieck)", marker_color=C.COLOR_MAIN))
    fig.add_trace(go.Bar(x=names, y=[A.log10_int(r["Mengenpartitionen B(n)"]) for r in rows], name="Mengenpartitionen B(n) (Aufzählen)", marker_color=C.COLOR_ALL))
    fig.update_layout(barmode="group")
    fig.update_xaxes(title_text="n")
    fig.update_yaxes(title_text="Anzahl (Zehnerlogarithmus)")
    return _base(fig, 340)
