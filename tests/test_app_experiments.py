"""AppTest-Durchläufe der Experimente, des Permalinks und der Spielwiese (die allgemeinen Rauchtests stehen in test_app.py)."""

import os
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import bes_constants as C

APP = str(Path(__file__).resolve().parent.parent / "app.py")
TIMEOUT = int(os.environ.get("APPTEST_TIMEOUT", "300"))


def _app(query: dict | None = None) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=TIMEOUT)
    for key, value in (query or {}).items():
        at.query_params[key] = value
    at.run()
    assert not at.exception, [str(e) for e in at.exception]
    return at


def _all_text(at) -> str:
    return " | ".join(e.value for e in list(at.success) + list(at.info) + list(at.warning) + list(at.error))


def _metrics(at) -> dict:
    return {m.label: m.value for m in at.metric}


def test_standard_case_shows_the_known_values_and_no_error():
    at = _app()
    assert not at.error
    assert _metrics(at) == {"Anzahl bei 10 Elementen": "115.975", "Stellen der Anzahl": "6", "Anteil an allen Möglichkeiten": "1,0000", "Schritte der Rechnung": "55"}
    assert any(e.value.startswith("10 verschiedene Elemente ergeben 115.975 Mengenpartitionen (Bell-Zahl).") for e in at.success)
    assert any(e.value == "Alle gerechneten Wege geben dieselbe Zahl." for e in at.success)


def test_experiments_two_to_five_show_their_verdicts_without_a_click():
    text = _all_text(_app())
    assert "Bei n = 20 gibt es 5,17·10¹³ (14 Stellen) Mengenpartitionen, aber nur 627 Zahlpartitionen" in text
    assert "D₁₀ = 1.334.961, also 36,79 % aller Permutationen" in text
    assert "fallen in nur 42 Zyklentypen" in text and "die größte Klasse ist 9 + 1 mit 403.200 Permutationen" in text
    assert "Für n = 1000 sind es 500.500 Summanden im exp-Kalkül" in text
    assert "55.980 von 59.049 Zuordnungen (94,8 %) lassen keine Maschine leer" in text


def test_time_measurement_runs_on_click():
    at = _app()
    at.button(key="time_run").click().run(timeout=TIMEOUT)
    assert not at.exception and any("Gemessen auf diesem Rechner (Python)" in i.value for i in at.info)


@pytest.mark.parametrize("name,value", [("Clustering: 10 Punkte in 3 Cluster", "9.330"), ("Derangements von 10", "1.334.961"), ("Involutionen von 10", "9.496"), ("Beschriftete Wurzelbäume (Cayley)", "1.000.000.000")])
def test_presets_show_their_number(name, value):
    at = _app()
    at.sidebar.button(key=f"preset_{name}").click().run(timeout=TIMEOUT)
    assert not at.exception and not at.error
    assert _metrics(at)["Anzahl bei 10 Elementen"] == value


def test_trees_show_the_unlabelled_count_as_a_metric():
    at = _app({"family": "Wurzelbäume", "n": "10"})
    assert _metrics(at)["Ohne Marken (Stück 5)"] == "719" and any("ohne Marken (Stück 5) wären es 719" in e.value for e in at.success)


def test_trees_with_block_settings_show_a_note():
    at = _app({"family": "Wurzelbäume", "n": "10", "lo": "3", "k": "2"})
    assert not at.exception and any("werden ignoriert" in i.value for i in at.info)


def test_wrong_range_shows_a_note():
    at = _app({"family": "Permutationen", "n": "8", "lo": "5", "hi": "2"})
    assert not at.exception and any("liegt unter der kleinsten" in i.value for i in at.info)


def test_permalink_loads_and_clamps_the_values():
    at = _app({"family": "Permutationen", "n": "99999", "lo": "0", "hi": "99999", "k": "77"})
    assert at.sidebar.selectbox(key="family_select").value == "Permutationen" and at.sidebar.slider(key="n_slider").value == C.N_MAX
    assert at.sidebar.slider(key="lo_slider").value == C.LO_MIN and at.sidebar.slider(key="hi_slider").value == C.HI_MAX and at.sidebar.slider(key="k_slider").value == 77
    assert _metrics(at)["Anzahl bei 150 Elementen"]


def test_permalink_with_garbage_is_ignored():
    at = _app({"family": "kein Name", "n": "abc", "lo": "x", "hi": "-", "k": "zz"})
    assert at.sidebar.selectbox(key="family_select").value == C.DEFAULT_FAMILY and at.sidebar.slider(key="n_slider").value == C.DEFAULT_N
    assert at.sidebar.slider(key="k_slider").value == C.DEFAULT_K


def test_every_family_and_k_combination_renders_without_error():
    for family in C.FAMILIES:
        for k in (0, 1, 3):
            at = _app({"family": family, "n": "12", "k": str(k)})
            assert not at.error, (family, k, [e.value for e in at.error])


@pytest.mark.parametrize("name", list(C.PRESETS))
def test_every_preset_renders_without_error_or_checker_message(name):
    at = _app()
    at.sidebar.button(key=f"preset_{name}").click().run(timeout=TIMEOUT)
    assert not at.exception and not at.error, name


def test_playground_changes_with_its_sliders():
    at = _app()
    at.slider(key="play_n").set_value(12).run(timeout=TIMEOUT)
    at.slider(key="play_k").set_value(4).run(timeout=TIMEOUT)
    assert not at.exception and not at.error
    assert any("von" in e.value and "Zuordnungen" in e.value and "lassen keine Maschine leer" in e.value for e in at.success)
    at.slider(key="play_n").set_value(3).run(timeout=TIMEOUT)
    assert not at.exception and any(e.value.startswith("0 von 64 Zuordnungen (0,0 %)") for e in at.success)


def test_pdf_can_be_made_for_the_extreme_settings():
    for query in ({"n": "1"}, {"family": "Mengenpartitionen", "n": "150"}, {"family": "Wurzelbäume", "n": "150"}, {"family": "Permutationen", "n": "150", "lo": "2", "k": "40"}):
        at = _app(query)
        at.button(key="pdf_make").click().run(timeout=TIMEOUT)
        assert not at.exception, query
