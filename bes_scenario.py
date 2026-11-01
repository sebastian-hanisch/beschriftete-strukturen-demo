"""Szenario: aus den Einstellungen die wirklich gerechneten Werte bestimmen (Begrenzen, Grenzfälle melden)."""

import bes_constants as C


def normalise(family: str, n: int, lo: int, hi: int, k: int):
    """Gerechnete Werte (n, lo, hi, k) und Hinweise. k = None heißt beliebig viele Blöcke; bei Wurzelbäumen gelten lo, hi und k nicht."""
    if family not in C.FAMILIES:
        raise ValueError(f"unbekannte Familie {family!r}")
    notes = []
    n_eff = max(C.N_MIN, min(n, C.N_MAX))
    if family == "Wurzelbäume":
        if (lo, hi, k) != (C.DEFAULT_LO, C.DEFAULT_HI, C.DEFAULT_K):
            notes.append("Bei Wurzelbäumen gelten Blockgröße und Zahl der Blöcke nicht; sie werden ignoriert.")
        return n_eff, C.DEFAULT_LO, C.DEFAULT_HI, None, notes
    lo_eff = max(C.LO_MIN, lo)
    hi_eff = max(hi, lo_eff)
    if hi < lo_eff:
        notes.append(f"Die größte Blockgröße ({hi}) liegt unter der kleinsten ({lo_eff}): gerechnet wird mit {hi_eff}.")
    k_eff = None if k <= 0 else k
    return n_eff, lo_eff, hi_eff, k_eff, notes
