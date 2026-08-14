# Daily Normal Newsletter

Täglicher Newsletter zu Politik und Geopolitik, Wirtschaft und Märkten, Technologie, Wissenschaft, Kultur und Karriere. Sechs Seiten, deutschsprachig, als PDF.

Dieses Repository enthält die vollständige Arbeitsgrundlage. Es ist öffentlich, damit Zapier die fertige Ausgabe für den Mailversand laden kann.

---

## Die drei maßgeblichen Dateien

| Datei | Rolle |
|---|---|
| [Struktur/Newsletter_Struktur.md](Struktur/Newsletter_Struktur.md) | Das vollständige Regelwerk. Inhalt, Sprache, Recherche, Gestaltung, Ablauf |
| [Mail Design/Mail Design.md](Mail%20Design/Mail%20Design.md) | Die Versandvorlage für die tägliche Mail |
| [Design/Main Design Template.pdf](Design/Main%20Design%20Template.pdf) | Der 1:1 Standard für die Gestaltung jeder Ausgabe |

---

## Ordnerstruktur

```
Design/
  Main Design Template.pdf     1:1 Standard, verbindlich
  Cover Page Example.jpeg      Bildmaterial der Cover Page
Template/
  newsletter_template.html     Bauplan mit allen Komponenten und Platzhaltern
  build.py                     Generator, Füllgradmessung und Prüfung
Struktur/
  Newsletter_Struktur.md       Regelwerk
Mail Design/
  Mail Design.md               Versandvorlage
Output/
  YYYYMMDD_Newsletter.pdf      fertige Ausgaben, Quelle für Zapier
```

---

## Eine Ausgabe erzeugen

```bash
python3 Template/build.py
```

Der Generator prüft zuerst, ob der 1:1 Standard vollständig vorliegt. Fehlt eine Datei, bricht er ab und baut nichts nach. Danach setzt er Datum und Coverbild ein, rendert die PDF nach `Output/` und misst den Füllgrad jeder Seite.

Er schlägt fehl, wenn das Dokument nicht genau sechs Seiten hat, wenn eine andere Schrift als Arial eingebettet ist, wenn weniger als 60 Quellen im Verzeichnis stehen oder wenn eine Seite unter 95 Prozent Füllgrad bleibt.

Für ein abweichendes Datum

```bash
python3 Template/build.py --date 2026-08-14
```

---

## Der Pfad für Zapier

Die Ausgabe des Tages liegt immer unter derselben Adresse. Nur das Datum wechselt.

```
https://raw.githubusercontent.com/marchaak77/Daily-Normal-Newsletter/main/Normal%20Newsletter/Output/YYYYMMDD_Newsletter.pdf
```

Der Projektordner liegt im Repository eine Ebene unterhalb der Wurzel, in einem Ordner namens `Normal Newsletter`. Das Leerzeichen darin muss in der Adresse als `%20` geschrieben werden.

Diese Adresse wird in Zapier in das Anhangsfeld der Gmail-Aktion eingetragen. Vor dem Versand muss sie den Statuscode 200 liefern.

```bash
curl -sL -o /dev/null -w "%{http_code}\n" "https://raw.githubusercontent.com/marchaak77/Daily-Normal-Newsletter/main/Normal%20Newsletter/Output/$(date +%Y%m%d)_Newsletter.pdf"
```

---

## Ablauf eines Tages

1. Repository prüfen, Aufbau und Erreichbarkeit der Rohdatei-Adresse
2. Zugriff auf den 1:1 Standard bestätigen
3. Ausgabe des Vortages lesen, um Wiederholungen zu vermeiden
4. Recherche, mindestens 60 unterschiedliche Quellen
5. Faktencheck in vier Stufen
6. Texte schreiben und in die Vorlage einsetzen
7. `python3 Template/build.py`
8. PDF in das Repository laden, nach `Normal Newsletter/Output`
9. Erreichbarkeit prüfen, dann Versand über Zapier auslösen

Die ausführliche Fassung steht in Abschnitt 12 des Regelwerks.
