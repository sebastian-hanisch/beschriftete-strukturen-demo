# Beschriftete Strukturen – wenn die Bausteine Marken tragen – Streamlit-Demo

**[→ Demo live ausprobieren](https://sebastianhanisch-beschriftete-strukturen-demo.streamlit.app/)**

Stück 6 von 16 der Reihe **„Abzählen und erzeugende Funktionen“** in der „Konzepte“-Reihe für die Website „Sebastian Hanisch – Operations Research und Machine Learning“ (die Linie wird erst vollständig veröffentlicht). Vorgänger sind `aufzaehlen-rekursion-demo` (Stück 1), `rationale-ef-demo` (Stück 2), `symbolische-methode-demo` (Stück 3), `semiring-rekursion-demo` (Stück 4) und `multimengen-partitionen-demo` (Stück 5). Diese Demo zählt **beschriftete** Strukturen: Die Elemente tragen die Marken 1 bis n und sind verschieden (Gegenstände, Aufgaben, Punkte, Mannschaften). Das Produkt zweier Strukturen verteilt die Marken auf beide Teile (eine Binomialfaltung, hinter der die exponentielle erzeugende Funktion steht), und aus Menge, Zyklus und Folge entstehen Mengenpartitionen mit den Bell-Zahlen, Permutationen und Derangements, die Stirling-Zahlen beider Arten und beschriftete Wurzelbäume (n^(n−1)). Mit „Mengenpartition“ ist hier die Zerlegung einer Menge in Blöcke gemeint, nicht die Zahlpartition (Stück 5) und nicht das Partitionsproblem der Komplexitätstheorie.

## Warum dieses Problem

Stück 5 hat gezählt, wenn die Reihenfolge egal ist; die Bausteine waren dabei nicht unterscheidbar. Bei Zuordnungs-, Clustering- und Packaufgaben sind die Elemente verschieden, und die Methode ohne Marken zählt dann etwas anderes: 115.975 Mengenpartitionen von 10 Elementen gegen 42 Zahlpartitionen von 10. Die Demo zeigt den beschrifteten Baukasten, wie groß der Suchraum der Zerlegungen ist, und wo „beschriftet = n! mal unbeschriftet“ nicht stimmt.

## Befunde und Korrekturen gegenüber dem Plan

- **Hook bestätigt:** Derangements gleich n!/e gerundet (n = 1 bis 300), Zyklentypen und Stirling-Zahlen aus demselben Baukasten.
- **Stärker als geplant:** Die Zahl der Zyklentypen von n Elementen ist die Partitionszahl aus Stück 5 (42 für n = 10), die Permutationen sind die beschriftete Version (3.628.800): dieselben Objekte zweimal gezählt. Die größte Klasse bei n = 10 ist nicht der volle Zyklus (362.880), sondern ein 9-Zyklus mit einem Fixpunkt (403.200).
- **Beschriftet ist nicht n! mal unbeschriftet:** beschriftet / (n!·unbeschriftet) fällt bei den Wurzelbäumen von 0,5787 (n = 5) auf 0,0059 (n = 60); das ist der Mittelwert von 1/|Aut| über alle unbeschrifteten Bäume (Deutung, die Stück 11 belegt; hier gemessen).
- **Zeit und Schritte klaffen auseinander:** Der exp-Kalkül und das Bell-Dreieck haben für Bell(1000) gleich viele Summanden (500.500), aber der Kalkül braucht in dieser Implementierung (Binomialkoeffizienten werden je Summand neu berechnet, dazu große Multiplikationen) in Phase 0 13,3 s gegen 0,3 s (Messung, nicht getestet). Die App begrenzt den Kalkül deshalb auf N = 150 (0,01 s) und zeigt n = 1000 im Aufwandsexperiment über das Dreieck.
- **Zweiter Rechenweg über Brüche:** Der Plan sah als zweite Formulierung die Rekursion „Block des Elements 1“ vor; sie ist dieselbe Formel wie der Kalkül. Der unabhängige zweite Weg ist darum die gewöhnliche Reihe mit Brüchen (n·ê_n = Σ k·â_k·ê_(n−k)); dazu kommen Dreiecke, Rekursionen, Formeln und Aufzählen.
- **Falsche Handrechnung (meine, nicht der Code):** In einem Test hatte ich Derangements für n = 4 mit Zykellängen bis 3 gezählt (3 statt 9): die 4-Zyklen fehlten. Der Test wurde korrigiert, der Code war richtig.
- **Port:** Der Plan sah 9319 vor; die Demo läuft darauf.

## Modell

Eine Folge `a` bedeutet a[n] = n!·[zⁿ]A(z): die Zahl der beschrifteten Strukturen mit den Marken 1 bis n. `l_mul` ist die Binomialfaltung (Marken auf beide Teile verteilen), `l_exp` die Menge von Blöcken (das Element 1 liegt in einem Block der Größe k: E_n = Σ C(n−1, k−1)·a_k·E_(n−k)), `l_seq` die Folge, `l_cyc` der Zyklus, `l_pow_over_fact` genau k Blöcke (A^k/k!). `blocks` baut die Blöcke (Menge: eine Möglichkeit je Größe, Zyklus: (k−1)! Möglichkeiten) mit Größen in einem Bereich. Familien: Mengenpartitionen, Permutationen (Zyklen) und beschriftete Wurzelbäume (T = z·exp(T)). Die Formeln stehen im 📐-Expander der App.

## Methodik

- **Rechenwege in der App** (Experiment 1): Binomialfaltung (Hauptweg), die gewöhnliche Reihe mit Brüchen (nur bei kleinem Aufwand), Dreieck, Rekursion oder Formel (nur wenn es sie gibt: Bell-Dreieck, Stirling-Dreiecke, Derangement- und Involutionsrekursion, n!/((g!)^(n/g)·(n/g)!)) und Aufzählen (Mengenpartitionen bis n = 9, Permutationen bis n = 7). Bei Wurzelbäumen kommen die Formel von Cayley, Kirchhoffs Determinante (bis n = 40) und das Aufzählen aller Elternfunktionen (bis n = 6) dazu. Bei Abweichung zeigt die App einen Fehler statt einer Zahl.
- **Aufwand** wird als Zahl der Summanden gezählt (exakt, getestet); die Zeit steht nur als Messung auf Klick.
- **Eingabe:** Familie, Zahl der Elemente N (bis 150), Blockgröße von … bis, genau k Blöcke (0 = beliebig). Die Adresszeile spiegelt die Einstellung.

## Befunde (gemessen, keine Behauptungen)

Jede Zahl steht in `tests/test_claims.py`, `tests/test_algorithm.py`, `tests/test_verdicts.py` oder `tests/test_oracle_bes.py`. Zeiten stehen in keinem Test; sie sind gemessen und gekennzeichnet.

| Frage | Befund |
|---|---|
| Handinstanzen | Bell(0) bis Bell(6) = 1, 1, 2, 5, 15, 52, 203; S(4,2) = 7, c(4,2) = 11; Derangements 0 bis 6: 1, 0, 1, 2, 9, 44, 265; Involutionen 0 bis 6: 1, 1, 2, 4, 10, 26, 76; beschriftete Wurzelbäume mit 1 bis 5 Knoten: 1, 2, 9, 64, 625; Zyklentypen von 4: (4) 6, (3,1) 8, (2,2) 3, (2,1,1) 6, (1,1,1,1) 1 |
| Bell- und Stirling-Zahlen | Bell(10) = 115.975, Bell(20) = 51.724.158.235.372, Bell(30) = 846.749.014.511.809.332.450.147 (aus dem Gedächtnis, durch mehrere Wege bestätigt), Bell(200) hat 276 Stellen; Zeile S(10,k) = 1, 511, 9.330, 34.105, 42.525, 22.827, 5.880, 750, 45, 1 (größtes bei k = 5); Zeile c(10,k) = 362.880, 1.026.576, 1.172.700, 723.680, 269.325, 63.273, 9.450, 870, 45, 1 |
| Derangements (Experiment 3) | D₅ = 44, D₁₀ = 1.334.961, D₂₀ = 895.014.631.192.902.121; D_n/n! für n = 1 bis 8: 0, 0,5, 0,33333, 0,375, 0,36667, 0,36806, 0,36786, 0,36788 (1/e = 0,36788); \|D_n/n! − 1/e\|·(n+1)! = 0,8732, 0,9226, 0,9811, 0,9903 bei n = 5, 10, 50, 100 (unter 1); D_n ist für n = 1 bis 300 die Rundung von n!/e |
| Zyklentypen (Experiment 4) | n = 10: **42 Zyklentypen** für 3.628.800 Permutationen, größte Klasse (9,1) mit 403.200, danach (10) mit 362.880, kleinste Klasse 1; Typen für n = 5, 10, 20: 7, 42, 627 gegen n! = 120, 3.628.800, 2.432.902.008.176.640.000; mittlere Zahl der Zyklen = H_n (H₁₀ = 7381/2520 ≈ 2,929) |
| Beschriftete Wurzelbäume (Experiment 1) | n^(n−1) für n = 1 bis 40; Kirchhoff: Spannbäume von K_n = n^(n−2), n = 2 bis 8; Aufzählen aller Elternfunktionen für n = 3, 4, 5, 6: 9, 64, 625, 7.776 |
| Beschriftet gegen unbeschriftet (Experiment 2) | B(n) gegen p(n) für n = 5, 10, 15, 20: 52/7, 115.975/42, 1.382.958.545/176, 51.724.158.235.372/627 (Faktoren 7,4; 2.761,3; 7.857.719; 8,2·10¹⁰); Wurzelbäume n = 5, 10, 20: 625/9, 10⁹/719, 20¹⁹/12.826.228 (Faktoren 69,4; 1.390.820,6; 4,1·10¹⁷); beschriftet / (n!·unbeschriftet) = 0,5787, 0,3833, 0,168, 0,0316, 0,0059 für n = 5, 10, 20, 40, 60 |
| Brücke zu Zuordnung, Clustering, Packen (Spielwiese) | S(10,3) = 9.330; 3!·S(10,3) = 55.980 von 3¹⁰ = 59.049 Zuordnungen lassen keine Maschine leer (94,8 %), gleich der Siebformel und dem Aufzählen; 12 Gegenstände in Gruppen bis 4: 3.305.017, 10 in Gruppen bis 3: 61.136, 12 in Gruppen bis 2: 140.152; 12 in Dreiergruppen: 15.400 = 12!/(3!⁴·4!); 8 Mannschaften in 4 Paare: 105 = 7·5·3·1; 10 Gegenstände in Gruppen bis 4: 99.146, davon genau 3 Gruppen: 3.675 (auch durch Aufzählen der Wachstumsfolgen) |
| Aufwand (Experiment 5) | Summanden des exp-Kalküls und Additionen des Bell-Dreiecks sind gleich: 5.050, 20.100, 125.250, 500.500 für n = 100, 200, 500, 1000; Bell(1000) hat 1.928 Stellen, Bell(2000) 4.350 (über der Grenze von 4.300 Stellen für `str`) |
| Presets | Bell von 10: 115.975; 10 Punkte in 3 Cluster: 9.330; 12 Gegenstände in Gruppen bis 4: 3.305.017; Dreiergruppen: 15.400; 8 Mannschaften in Paare: 105; Derangements von 10: 1.334.961 (36,8 % von 10!); Involutionen von 10: 9.496; Permutationen mit 3 Zyklen: 1.172.700; beschriftete Wurzelbäume mit 10 Knoten: 10⁹ |
| Zeit (nur gemessen, **nicht getestet**) | Auf dem Entwicklungsrechner (Phase 0): exp-Kalkül n = 100, 150, 200, 300: 0,004 s, 0,013 s, 0,036 s, 0,15 s; n = 500: 1,1 s, n = 1000: 13,3 s; Bell-Dreieck n = 1000: 0,30 s, n = 2000: 2,2 s; die App misst n = 200, 300, 500 auf Klick |

## Ehrliche Grenzen

- **Literaturwerte aus dem Gedächtnis:** Bell(30), n!/e, Cayley und H_n wurden nicht an einer Quelle gelesen. Mehrere unabhängige Rechenwege stimmen überein; das ersetzt keine Quelle.
- **Das Verhältnis beschriftet / (n!·unbeschriftet)** ist eine Messung bis n = 60 (der Text sagt „fällt“, nicht „strebt gegen 0“); die Erklärung über 1/|Aut| ist eine Deutung, die Stück 11 belegen muss.
- **Aufzählen als Prüfer ist begrenzt** (Mengenpartitionen n ≤ 9, Permutationen n ≤ 7, Wurzelbäume n ≤ 6); darüber prüfen sich nur Kalkül, Brüche und Dreiecke gegenseitig. Die gewöhnliche Reihe mit Brüchen läuft nur, wenn der Aufwand klein bleibt (k·(n+1)² ≤ 60.000).
- **Schritte sind Summanden**, nicht Zeit: gleich viele Schritte können je nach n und Implementierung sehr verschieden lang dauern (Messung bei n = 1000: 44-mal).
- **Nur Mengen, Zyklen und Wurzelbäume:** beschriftete Graphen, zusammenhängende Graphen und Funktionalgraphen brauchen weitere Bausteine.
- **Blöcke ohne Reihenfolge:** Mit Reihenfolge der Blöcke wären es geordnete Zerlegungen (k!·S(n,k), Surjektionen); verbotene Paare in Zuordnungen zählt die Permanente (Stück 7 und Komplexitätslinie).
- **Wachstum nur als Zahl:** Wie B(n) wächst und wie schnell D_n/n! sich einpendelt, ist hier eine Tabelle, nicht ein Satz (Stück 9).
- **Zielgröße begrenzt** auf 150 Elemente (der Kalkül hat n(n+1)/2 Summanden mit großen Zahlen).
- **Zeiten** sind Python-Messungen dieses Rechners; zwei Läufe unterscheiden sich.
- **Browser:** Seitentext, Zahlen, Diagrammbreiten, Preset-Klick, Spielwiese und die Zeitmessung im Browser geprüft; Handy-Breite nicht.
- Alles gerechnet, keine echten Daten.

## Verifikation

- **Kern:** Handinstanzen (Mengenpartitionen von 3 Elementen, Permutationen von 3 und 4 Elementen, das Produkt „nichtleere Menge mal Zyklus“, beschriftete Bäume mit 2 und 3 Knoten), Aufzählen der Mengenpartitionen über Wachstumsfolgen, Aufzählen der Permutationen mit ihren Zyklen, Dreiecke von Stirling und Bell, Rekursionen, e als Bruch, Kirchhoffs Determinante, die Siebformel, die gewöhnliche Reihe mit Brüchen; Zufallsfamilien (80 für Mengenpartitionen, 40 mit genau k Blöcken, 40 für Permutationen), festgeschriebene Zahlen aus Stück 5.
- **Eigenschaften:** ein enthaltener Größenbereich gibt nie mehr Strukturen; höchstens Bell(n) beziehungsweise n!; die k-Block-Reihen summieren sich zur Reihe ohne k; Binomialfaltung kommutativ und assoziativ; exp(A+B) = exp(A)·exp(B); Menge von Zyklen = Folge von Einzelelementen = n!; Derangements plus Permutationen mit Fixpunkten = n!; Surjektionen höchstens k^n; beschriftet höchstens n!·unbeschriftet; das Verhältnis fällt (ab n = 3 streng, bei n = 1 und n = 2 gleich 1); die Derangement-Wahrscheinlichkeit pendelt sich ein; gleiches Ergebnis in Prozessen mit verschiedenem `PYTHONHASHSEED`.
- **Randfälle:** 0 und 1 Element, Blockgröße 1, Blöcke größer als N, k = 0 und k > n, Zahlen über der 4300-Stellen-Grenze von `str`, falsch herum gestellter Bereich (Hinweis), Wurzelbäume mit Blockeinstellungen (Hinweis), zu teure Brüchereihe übersprungen, jede Familie bei den kleinsten Größen, Grenzen der Spielwiese.
- **Oberfläche:** AppTest-Rauchtest (jeder Button, jeder Regler an Minimum und Maximum), alle Experimente, Permalink mit Müll und Grenzwerten, jede Familie mit k, jedes Preset, Spielwiese, PDF an den Rändern; Footer-Test.
- **Layout:** Schnellstart oben in der Seitenleiste, fester Kopf, aktives Preset hervorgehoben; jede Änderung eines Reglers hebt die Markierung auf (`tests/test_layout.py`).
- **Nicht gemacht:** Mutationstests (seit 2026-10-28 nicht mehr verlangt), Docker-Lauf der Linux-CI (Docker fehlt auf diesem Rechner; die CI nach dem Push entscheidet).

733 Tests (`pytest tests`), zuletzt in etwa einer Minute (58 Sekunden gemessen) auf dem Entwicklungsrechner (Messung, nicht getestet).

## Dateistruktur

| Datei | Zweck |
|---|---|
| `.github/workflows/tests.yml` | CI: Push, Pull Request, wöchentlicher Canary |
| `.gitignore` | venv, Caches, Streamlit-Secrets |
| `.streamlit/config.toml` | Streamlit-Einstellungen (keine Nutzungsstatistik) |
| `app.py` | Streamlit-App: Ergebnis, Kernfrage, fünf Experimente, Spielwiese, Grenzen, Formeln |
| `bes_algorithm.py` | Kern: beschrifteter Baukasten, Dreiecke, Rekursionen, Aufzählen, Wurzelbäume |
| `bes_constants.py` | Regler-Grenzen, Schwellen, Farben, Presets |
| `bes_evaluation.py` | Analyse, Experimente, Verdikte, Formatierung |
| `bes_layout.py` | Fester Kopf (Stylesheet) |
| `bes_pdf_export.py` | PDF der aktuellen Aufgabe (fpdf2) |
| `bes_presets.py` | Permalink (Begrenzen), Presets (Schnellstart in der Seitenleiste, aktives Preset hervorgehoben) |
| `bes_scenario.py` | Eingaben begrenzen und Hinweise melden |
| `bes_visualization.py` | Plotly-Abbildungen (Achsen gesperrt) |
| `requirements-dev.txt` | Laufzeit plus pytest |
| `requirements.txt` | Laufzeit-Bibliotheken (ungepinnt) |
| `tests/` | Handwerte, Orakel, Eigenschaften, Randfälle, Verdikte, Claims, Presets, Layout, AppTest, Footer, Laufzeit-Importe |

## Bewusst nicht umgesetzt

- **Bis auf Symmetrie zählen (Burnside, Pólya):** Stück 11; hier nur das Verhältnis beschriftet / (n!·unbeschriftet).
- **Siebformel, verbotene Paare, Permanente:** Stück 7; die Surjektionen erscheinen nur als Zahlenprobe.
- **Zählen nach Parameter mit Mittel und Streuung (bivariate Reihe):** Stück 8; die Zeilen von S und c werden hier aus A^k/k! gelesen.
- **Asymptotik (Bell, n!/e, Cayley) und gleichverteilt ziehen:** Stück 9 und 10.
- **Dobinski-Formel, Touchard-Kongruenzen, q-Analoga, beschriftete Graphen:** nicht Teil der Linie.
- **Verwandte Demos:** `multimengen-partitionen-demo` (ohne Marken), `cmst-demo` und `constrained-mst-demo` (Zerlegung der Kunden in Bäume), `kruskal-demo` und `random-spanning-tree-demo` (Cayley n^(n−2) als Prüfwert); nur Verweise.

## Lokal ausführen

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

pip install -r requirements.txt
streamlit run app.py
```

Streamlit Cloud: Python-Version nach der Voreinstellung der Plattform (lokal `3.14`, CI `3.12`); der Code nutzt nur Merkmale, die in `3.12` laufen.

## Tests ausführen

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Gebaut mit Streamlit, Plotly und fpdf2.

---

Diese Demo ist Teil des Portfolios von [Sebastian Hanisch](https://sebastianhanisch.net) – Operations Research und Machine Learning ([Über mich](https://sebastianhanisch.net/ueber-mich.html)). Mehr zur Reihe: [Abzählen: von der Rekursion zur Verfahrenswahl](https://sebastianhanisch.net/konzepte-abzaehlen.html).
