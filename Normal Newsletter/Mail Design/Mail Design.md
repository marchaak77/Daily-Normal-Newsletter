# Mail Design — Versandvorlage für den Normal Newsletter

Diese Datei ist die verbindliche Vorlage für die tägliche Versandmail, mit der die Newsletter-PDF ausgeliefert wird.
Sie ergänzt die Datei `Struktur/Newsletter_Struktur.md`, welche den Newsletter selbst regelt.

---

## 1. Rolle

Du agierst als Redakteur und Versandverantwortlicher.
Deine Aufgabe ist es, die fertige Newsletter-PDF des Tages per Mail auszuliefern und im Mailtext die sechs wichtigsten Meldungen der Ausgabe so zusammenzufassen, dass sie sofort verständlich sind.

Die Mail ist kein zweiter Newsletter. Sie ist ein kurzer, professioneller Überblick mit Anhang.

---

## 2. Versandparameter

| Merkmal | Festlegung |
|---|---|
| Versandweg | Automatisiert über Zapier |
| Mailkonto | Google Mail, Konto laut Zapier-Verbindung, siehe Abschnitt 2.1 |
| Empfänger | Zara Mainz, Adresse laut Zapier-Konfiguration, siehe Abschnitt 2.1 |
| Versandart | Direkter Versand, kein Entwurf |
| Frequenz | Täglich |
| Auslöser | Routinen-Einstellung innerhalb von Claude |
| Datumsbezug | Immer das aktuelle Datum des Ausführungstages laut Routinen-Einstellung |
| Anhang | `YYYYMMDD_Newsletter.pdf`, von Zapier über die öffentliche Rohdatei-Adresse geladen |
| Absendername | Marc Haak |

### 2.1 Wo Absender und Empfänger hinterlegt sind

Dieses Repository ist öffentlich. Mailadressen stehen deshalb **nicht** in den Dateien, sondern ausschließlich in der Zapier-Konfiguration.

| Angabe | Fundort |
|---|---|
| Absenderkonto | Die verbundene Gmail-Verbindung in Zapier. Es gibt genau eine, sie wird immer verwendet |
| Empfänger | Das Feld `To` in der Zapier-Aktion für den täglichen Versand |

Vor dem Versand wird geprüft, dass die Gmail-Verbindung das erwartete Konto ist und dass genau eine Empfängeradresse eingetragen ist. Wird eine Adresse geändert, geschieht das in Zapier und nicht in dieser Datei.

### Woher Zapier die PDF nimmt

Zapier kann nicht auf die Festplatte zugreifen. Die PDF wird deshalb vor dem Versand in das öffentliche GitHub-Repository gepusht und von dort als Anhang geladen.

| Merkmal | Festlegung |
|---|---|
| Repository | `Daily-Normal-Newsletter` |
| Adresse | `https://github.com/marchaak77/Daily-Normal-Newsletter.git` |
| Zweig | `main` |
| Pfad im Repository | `Normal Newsletter/Output` |

Der Projektordner liegt im Repository nicht in der Wurzel, sondern eine Ebene tiefer in einem Ordner mit dem Namen `Normal Newsletter`. Dieser Ordnername enthält ein Leerzeichen. In einer Adresse muss ein Leerzeichen als `%20` geschrieben werden.

**Die Adresse für das Anhangsfeld in Zapier**

```
https://raw.githubusercontent.com/marchaak77/Daily-Normal-Newsletter/main/Normal%20Newsletter/Output/YYYYMMDD_Newsletter.pdf
```

Nur das Datum im Dateinamen wechselt täglich. In Zapier wird dieser Wert dynamisch aus dem Ausführungsdatum im Format `YYYYMMDD` gebildet.

**Beispiel für den 12.08.2026**

```
https://raw.githubusercontent.com/marchaak77/Daily-Normal-Newsletter/main/Normal%20Newsletter/Output/20260812_Newsletter.pdf
```

**Häufige Fehler, die zu einem 404 führen**

| Falsch | Warum |
|---|---|
| `.../main/Output/...` | Der Ordner `Normal Newsletter` fehlt |
| `.../main/Normal Newsletter/Output/...` | Unkodiertes Leerzeichen |
| `.../main/Normal+Newsletter/Output/...` | Ein Plus ersetzt kein Leerzeichen in einem Pfad, nur in einer Abfrage |
| `github.com/...` statt `raw.githubusercontent.com/...` | Liefert die Weboberfläche, keine Datei |

**Pflichtprüfung vor dem Versand.** Die Adresse wird aufgerufen und muss den Statuscode 200 liefern. Erst danach wird gesendet. Liefert sie 404, ist die Datei noch nicht im Repository. Dann wird nicht gesendet, sondern erst hochgeladen.

```bash
curl -sL -o /dev/null -w "%{http_code}\n" "https://raw.githubusercontent.com/marchaak77/Daily-Normal-Newsletter/main/Normal%20Newsletter/Output/$(date +%Y%m%d)_Newsletter.pdf"
```

---

## 3. Betreff

```
Newsletter - Ausgabe des DD.MM.YYYY
```

Das Datum wird bei jeder Ausführung automatisch durch das aktuelle Tagesdatum ersetzt.

Beispiel für den 12.08.2026
```
Newsletter - Ausgabe des 12.08.2026
```

---

## 4. Aufbau der Mail

Die Mail folgt immer derselben Reihenfolge.

1. Anrede
2. Einleitung mit Hinweis auf den Anhang
3. Überblick über die sechs wichtigsten Meldungen des Tages
4. Schlusssatz
5. Grußformel

---

## 5. Textvorlage

### 5.1 Anrede

```
Hallo zusammen
```

Diese Zeile steht unverändert am Anfang jeder Mail.

### 5.2 Einleitung

Ein kurzer, professioneller Absatz, der mitteilt, dass die heutige Ausgabe des Newsletters im Anhang beiliegt und dass die wichtigsten Meldungen darunter zusammengefasst sind.

Beispielformulierung
```
die heutige Ausgabe des Newsletters vom 12.08.2026 liegt dieser Mail als PDF im Anhang bei.
Nachfolgend finden Sie die sechs wichtigsten Meldungen des Tages in kurzer Form.
```

Der Wortlaut darf tagesabhängig leicht variieren, bleibt aber sachlich und professionell.

### 5.3 Die sechs wichtigsten Meldungen

Grundlage sind ausschließlich die Inhalte der Newsletter-PDF des jeweiligen Tages. Es werden keine Meldungen ergänzt, die nicht im PDF stehen.

Pro Meldung gilt dieser Aufbau.

1. Zeile eins ist die Überschrift der Rubrik, aus der die Meldung stammt
2. Darunter folgt die Ausführung des Topics in verständlicher Sprache

Die sechs Rubriken sind
* Politik & Geopolitik
* Wirtschaft & Märkte
* Technologie & Innovation
* Wissenschaft & Forschung
* Kultur & Gesellschaft
* Karriere & Trends

Beispielstruktur
```
Politik & Geopolitik
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]

Wirtschaft & Märkte
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]

Technologie & Innovation
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]

Wissenschaft & Forschung
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]

Kultur & Gesellschaft
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]

Karriere & Trends
[Verständliche Ausführung des wichtigsten Topics aus dieser Rubrik]
```

### 5.4 Schlusssatz

```
Ich wünsche einen erfolgreichen Start in den Tag
```

Diese Zeile steht unverändert am Ende jeder Mail.

### 5.5 Grußformel

```
Viele Grüße
Marc Haak
```

---

## 6. Sprachregeln für den Mailtext

Es gelten dieselben Regeln wie für den Newsletter.

1. Verständlich auf Grundschulniveau, jeder Satz ohne Vorwissen nachvollziehbar
2. Fachbegriffe werden erklärt oder vermieden
3. Menschlich verfasst, kein Kauderwelsch, kein AI Slop
4. Keine Doppelpunkte im Satzbau, also kein Doppelpunkt zur Ankündigung von Aufzählungen oder Nachsätzen
5. Keine Gedankenstriche im Satzbau, Einschübe werden mit Komma gelöst
6. Bindestriche in zusammengesetzten Wörtern sind erlaubt und werden nach den Regeln der deutschen Rechtschreibung gesetzt, etwa KI-Modell oder US-Bundesstaat
7. Abkürzungen werden bei der ersten Nennung in Klammern ausgeschrieben und kurz erklärt, etwa PKK (Partiya Karkerên Kurdistanê, die Arbeiterpartei Kurdistans, eine verbotene kurdische Untergrundorganisation). Ausgenommen sind allgemein bekannte Länderkürzel wie USA und EU
8. MECE, jede Information erscheint nur einmal
9. Keine Wiederholung derselben Formulierung zwischen den sechs Meldungen
10. Keine Aussage, die nicht durch die PDF gedeckt ist
11. Die sechs Meldungen unterscheiden sich inhaltlich von denen des Vortages, siehe Abschnitt 9 der Datei `Struktur/Newsletter_Struktur.md`

Hinweis
Der Betreff ist von den Regeln 4 und 5 ausgenommen, da seine Schreibweise fest vorgegeben ist.

---

## 7. Gestaltung der Mail

* Reiner, ruhiger Textaufbau ohne überladene Grafik
* Schriftart Arial
* Farbwelt wie im Newsletter, also Weiß als Grundfläche, Grau für Text, Beige/Sand als einziger Akzent
* Rubriküberschriften optisch abgesetzt, zum Beispiel fett
* Ein Leerraum zwischen den sechs Meldungen, damit die Struktur sofort erkennbar ist
* Keine Bilder im Mailtext, das PDF trägt die Gestaltung

---

## 8. Vollständiges Beispiel

**Betreff**
```
Newsletter - Ausgabe des 12.08.2026
```

**Text**
```
Hallo zusammen

die heutige Ausgabe des Newsletters vom 12.08.2026 liegt dieser Mail als PDF im Anhang bei.
Nachfolgend finden Sie die sechs wichtigsten Meldungen des Tages in kurzer Form.

Politik & Geopolitik
[Inhalt]

Wirtschaft & Märkte
[Inhalt]

Technologie & Innovation
[Inhalt]

Wissenschaft & Forschung
[Inhalt]

Kultur & Gesellschaft
[Inhalt]

Karriere & Trends
[Inhalt]

Ich wünsche einen erfolgreichen Start in den Tag

Viele Grüße
Marc Haak
```

**Anhang**
```
20260812_Newsletter.pdf
```

---

## 9. Ablauf je Versandtag

1. Routine in Claude löst zum festgelegten Zeitpunkt aus
2. Aktuelles Datum aus der Routinen-Einstellung übernehmen
3. Prüfen, dass die PDF des Tages im Repository liegt und die Rohdatei-Adresse den Statuscode 200 liefert
4. Newsletter-PDF des Tages lesen
5. Die sechs wichtigsten Meldungen aus der PDF ableiten, je eine pro Rubrik
6. Mailtext nach Abschnitt 5 aufbauen
7. Betreff nach Abschnitt 3 setzen
8. Zapier-Aktion für Google Mail ausführen mit dem in Zapier hinterlegten Absender und Empfänger
9. Im Anhangsfeld die Rohdatei-Adresse mit dem heutigen Datum eintragen
10. Direkt versenden, keinen Entwurf anlegen
11. Endkontrolle nach Abschnitt 10 vor dem Versand

---

## 10. Endkontrolle vor dem Versand

| Prüfpunkt | Erfüllt |
|---|---|
| Betreff lautet `Newsletter - Ausgabe des DD.MM.YYYY` mit heutigem Datum | ☐ |
| Mail startet mit `Hallo zusammen` | ☐ |
| Hinweis auf den Anhang vorhanden | ☐ |
| Genau sechs Meldungen, je eine pro Rubrik | ☐ |
| Jede Meldung trägt die Rubriküberschrift | ☐ |
| Inhalte stammen ausschließlich aus der PDF des Tages | ☐ |
| Grundschulverständliche Sprache | ☐ |
| Keine Doppelpunkte und keine Gedankenstriche im Satzbau | ☐ |
| Bindestriche in zusammengesetzten Wörtern korrekt gesetzt | ☐ |
| Abkürzungen bei Erstnennung in Klammern erklärt | ☐ |
| Meldungen unterscheiden sich von der Vortagsmail | ☐ |
| Keine Wiederholungen, MECE erfüllt | ☐ |
| Schlusssatz `Ich wünsche einen erfolgreichen Start in den Tag` vorhanden | ☐ |
| Grußformel `Viele Grüße Marc Haak` vorhanden | ☐ |
| Rohdatei-Adresse liefert Statuscode 200 und eine PDF | ☐ |
| Datum in der Anhangsadresse entspricht dem heutigen Tag | ☐ |
| PDF `YYYYMMDD_Newsletter.pdf` korrekt angehängt | ☐ |
| Absender entspricht dem hinterlegten Gmail-Konto | ☐ |
| Empfänger entspricht der hinterlegten Adresse | ☐ |
| Direktversand, kein Entwurf | ☐ |

---

## 11. Ordnerbezug

```
Normal Newsletter/
├── Design/
├── Mail Design/
│   └── Mail Design.md              diese Datei
├── Output/                         Quelle für den PDF-Anhang
└── Struktur/
    └── Newsletter_Struktur.md      Regelwerk für den Newsletter selbst
```
