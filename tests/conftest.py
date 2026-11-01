"""Gemeinsame Fixtures: die Mini-Instanzen, an denen jede Einheit von Hand geprüft wird (DEMO-PLAYBOOK §1b)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def hand_set_partitions_of_3():
    """Mengenpartitionen von {1,2,3} von Hand: {123}, {1|23}, {2|13}, {3|12}, {1|2|3} = 5 (Bell(3)); mit Blockgrößen nur 1 oder 2 fehlt {123}: 4."""
    return {"all": [[(1, 2, 3)], [(1,), (2, 3)], [(2,), (1, 3)], [(3,), (1, 2)], [(1,), (2,), (3,)]], "bell": 5, "blocks_up_to_2": 4}


@pytest.fixture
def hand_permutations_of_3():
    """Permutationen von {1,2,3} nach Zyklentyp von Hand: (3): zwei 3-Zyklen, (2,1): drei Transpositionen, (1,1,1): die Identität, zusammen 6. Derangements: 2 (nur die 3-Zyklen); Involutionen: 1 + 3 = 4."""
    return {"types": {(3,): 2, (2, 1): 3, (1, 1, 1): 1}, "derangements": 2, "involutions": 4}


@pytest.fixture
def hand_n4():
    """n = 4 von Hand: Derangements 9 (sechs 4-Zyklen, drei Paare von Transpositionen); S(4,2) = 7 (vier Blöcke 3+1, drei Blöcke 2+2); c(4,2) = 11 (acht Zyklen 3+1, drei 2+2);
    Surjektionen von 4 Aufgaben auf 2 Maschinen: 2^4 − 2 = 14 = 2!·S(4,2); Produkt nichtleere Menge mal Zyklus: 4·2! + 6·1! + 4·0! = 18."""
    return {"derangements": 9, "S42": 7, "c42": 11, "surjections": 14, "set_times_cycle": 18, "types": {(4,): 6, (3, 1): 8, (2, 2): 3, (2, 1, 1): 6, (1, 1, 1, 1): 1}}
