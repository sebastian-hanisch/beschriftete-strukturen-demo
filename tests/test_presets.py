"""Presets: Vollständigkeit, gültige Werte, Standard-Preset = Standardeinstellungen, jedes Preset zeigt etwas anderes."""

import bes_constants as C
import bes_evaluation as ev
import bes_presets as P


def test_every_preset_has_help_and_all_keys():
    assert set(C.PRESETS) == set(C.PRESET_HELP)
    for name, preset in C.PRESETS.items():
        assert set(preset) == set(P.PRESET_KEYS), name
        assert C.PRESET_HELP[name]


def test_preset_values_are_inside_the_regler_bounds():
    for name, preset in C.PRESETS.items():
        assert preset["family"] in C.FAMILIES and C.N_MIN <= preset["n"] <= C.N_MAX, name
        assert C.LO_MIN <= preset["lo"] <= C.LO_MAX and C.HI_MIN <= preset["hi"] <= C.HI_MAX and C.K_MIN <= preset["k"] <= C.K_MAX, name
        assert preset["lo"] <= preset["hi"], name


def test_every_preset_passes_the_checker_without_notes():
    for name, preset in C.PRESETS.items():
        a = ev.analyse(ev.Settings(**preset))
        assert a.problems == [] and a.notes == [] and a.n_eff == preset["n"], name


def test_first_preset_equals_the_default_settings():
    assert ev.Settings(**C.PRESETS[next(iter(C.PRESETS))]) == ev.Settings()


def test_setting_specs_cover_every_preset_key():
    assert set(P.PRESET_KEYS.values()) == set(P.SETTING_SPECS)


def test_presets_show_what_their_help_says():
    stats = {name: ev.analyse(ev.Settings(**p)) for name, p in C.PRESETS.items()}
    assert stats["Clustering: 10 Punkte in 3 Cluster"].k == 3 and stats["Permutationen mit 3 Zyklen (Stirling erster Art)"].k == 3
    assert stats["Derangements von 10"].lo == 2 and stats["Involutionen von 10"].hi == 2 and stats["Dreiergruppen: 12 Personen"].lo == stats["Dreiergruppen: 12 Personen"].hi == 3
    assert stats["Beschriftete Wurzelbäume (Cayley)"].settings.family == "Wurzelbäume"
    assert len({(a.settings.family, a.n_eff, a.lo, a.hi, a.k) for a in stats.values()}) == len(C.PRESETS) == len({a.series[a.n_eff] for a in stats.values()})
