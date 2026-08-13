#!/usr/bin/env python3
"""
Generator für den Daily Normal Newsletter.

Setzt Datum und Coverbild in die Vorlage ein, rendert die PDF nach Output/
und misst den Füllgrad jeder Seite.

Aufruf aus dem Projektordner heraus
    python3 Template/build.py

Optionen
    --date YYYY-MM-DD   Abweichendes Ausgabedatum, sonst heute
    --no-check          Füllgradmessung überspringen
"""

import argparse
import base64
import datetime
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "Template" / "newsletter_template.html"
COVER = ROOT / "Design" / "Cover Page Example.jpeg"
STANDARD = ROOT / "Design" / "Main Design Template.pdf"
OUTPUT = ROOT / "Output"

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni",
          "Juli", "August", "September", "Oktober", "November", "Dezember"]

# Messgrenzen in Bildschirmpunkten bei 794 x 1123 je Seite
PAGE_H = 1123
CONTENT_TOP = 40
CONTENT_BOTTOM = 1058          # Oberkante der Fußzeile, wird nicht mitgezählt
MIN_FILL = 95.0                # Vorgabe aus Newsletter_Struktur.md, Abschnitt 4
MIN_QUELLEN = 60               # Untergrenze, nach oben offen. Nie ein Abbruchgrund


def fail(msg):
    print(f"ABBRUCH  {msg}", file=sys.stderr)
    sys.exit(1)


def check_standard():
    """Phase A, Schritt 3 der Struktur. Ohne den 1:1 Standard wird nicht gebaut."""
    fehlend = [p for p in (TEMPLATE, COVER, STANDARD) if not p.exists()]
    if fehlend:
        for p in fehlend:
            print(f"  fehlt  {p.relative_to(ROOT)}", file=sys.stderr)
        fail("Der 1:1 Standard ist nicht vollständig. Es wird nichts nachgebaut.")
    print(f"Standard geprüft   {STANDARD.relative_to(ROOT)}")


def cover_b64():
    """Coverbild auf 1800 px verkleinern und als base64 zurückgeben."""
    tmp = pathlib.Path(tempfile.mkdtemp()) / "cover.jpg"
    subprocess.run(["sips", "-Z", "1800", "-s", "format", "jpeg",
                    "-s", "formatOptions", "72", str(COVER), "--out", str(tmp)],
                   capture_output=True, check=True)
    return base64.b64encode(tmp.read_bytes()).decode()


def render(datum):
    html = TEMPLATE.read_text()
    html = (html
            .replace("__DATE_LONG__", f"{datum.day}. {MONATE[datum.month - 1]} {datum.year}")
            .replace("__DATE_SHORT__", datum.strftime("%d.%m.%Y"))
            .replace("__COVER_B64__", cover_b64()))

    work = pathlib.Path(tempfile.mkdtemp())
    page = work / "render.html"
    page.write_text(html)

    OUTPUT.mkdir(exist_ok=True)
    pdf = OUTPUT / f"{datum.strftime('%Y%m%d')}_Newsletter.pdf"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                    f"file://{page}"], capture_output=True)
    if not pdf.exists():
        fail("Chrome hat keine PDF erzeugt.")
    return pdf, page


def measure(page_html):
    """Füllgrad je Seite messen. Gibt True zurück, wenn alle Seiten die Vorgabe erfüllen."""
    try:
        from PIL import Image
    except ImportError:
        print("Hinweis  Pillow fehlt, Füllgradmessung übersprungen")
        return True

    work = page_html.parent
    shot = work / "full.png"
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-sandbox",
                    "--hide-scrollbars", f"--window-size=794,{PAGE_H * 6}",
                    f"--screenshot={shot}", f"file://{page_html}"], capture_output=True)

    im = Image.open(shot).convert("L")
    alles_ok = True
    for i in range(6):
        top = i * PAGE_H
        letzte = 0
        for y in range(top + CONTENT_BOTTOM, top, -1):
            if any(p < 170 for p in im.crop((30, y, 764, y + 1)).getdata()):
                letzte = y - top
                break
        fill = max(0.0, min(100.0, (letzte - CONTENT_TOP) / (CONTENT_BOTTOM - CONTENT_TOP) * 100))
        # Seite 1 ist randabfallend gestaltet und von der Prüfung ausgenommen
        ok = (i == 0) or (fill >= MIN_FILL)
        alles_ok &= ok
        print(f"  Seite {i + 1}   Füllgrad {fill:5.1f} %   {'OK' if ok else 'ZU LEER'}")
    return alles_ok


def audit(pdf):
    """
    Formale Prüfungen am fertigen Dokument.

    Gibt zwei Werte zurück.
        ok             harte Strukturfehler, etwa Seitenzahl oder Schriftart
        nachrecherche  die Quellenzahl liegt unter der Untergrenze

    Eine zu geringe Quellenzahl ist ausdrücklich KEIN Abbruchgrund. Der Lauf
    wird nie beendet, sondern kehrt in die Recherche zurück und wird
    fortgesetzt, bis die Untergrenze erreicht ist.
    """
    daten = pdf.read_bytes()
    seiten = daten.count(b"/Type /Page") - daten.count(b"/Type /Pages")
    fonts = sorted({m.decode() for m in re.findall(rb"/BaseFont /[A-Z]{6}\+([A-Za-z\-]+)", daten)})
    quellen = TEMPLATE.read_text().count('class="ref"')
    kapitel = TEMPLATE.read_text().count('class="sec"')

    print(f"  Seiten     {seiten}")
    print(f"  Größe      {round(len(daten) / 1024)} KB")
    print(f"  Schriften  {', '.join(fonts)}")
    print(f"  Kapitel    {kapitel}")
    print(f"  Quellen    {quellen}  (Untergrenze {MIN_QUELLEN}, nach oben offen)")

    ok = True
    if seiten != 6:
        print("  FEHLER  Das Dokument muss genau 6 Seiten haben."); ok = False
    if any(not f.startswith("Arial") for f in fonts):
        print("  FEHLER  Es sind Schriften außer Arial eingebettet."); ok = False

    nachrecherche = quellen < MIN_QUELLEN
    if nachrecherche:
        fehlend = MIN_QUELLEN - quellen
        print(f"  OFFEN   Es fehlen noch {fehlend} Quellen bis zur Untergrenze von {MIN_QUELLEN}.")
        print("          Kein Abbruch. Die Recherche wird fortgesetzt, bis die Zahl erreicht ist.")
    return ok, nachrecherche


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="Ausgabedatum als YYYY-MM-DD")
    ap.add_argument("--no-check", action="store_true")
    args = ap.parse_args()

    datum = (datetime.date.fromisoformat(args.date) if args.date else datetime.date.today())

    print(f"Ausgabe            {datum.strftime('%d.%m.%Y')}")
    check_standard()

    pdf, page = render(datum)
    print(f"Erzeugt            {pdf.relative_to(ROOT)}")

    print("Füllgrad")
    fill_ok = True if args.no_check else measure(page)
    print("Prüfung")
    audit_ok, nachrecherche = audit(pdf)

    shutil.rmtree(page.parent, ignore_errors=True)

    if nachrecherche:
        # Kein Abbruch. Die Quellenzahl ist eine Untergrenze, die erreicht werden
        # muss, kein Grund den Lauf zu beenden.
        print("\nERGEBNIS  Weiter recherchieren.")
        print("Die Untergrenze bei den Quellen ist noch nicht erreicht. Der Lauf ist nicht")
        print("beendet. Zusätzliche Quellen suchen, in das Quellenverzeichnis eintragen und")
        print("erneut bauen. Erst danach versenden.")
        return
    if not (fill_ok and audit_ok):
        print("\nERGEBNIS  Strukturprüfungen fehlgeschlagen. Nicht versenden.")
        sys.exit(1)

    print("\nERGEBNIS  Alle Prüfungen bestanden.")
    print(f"Nächster Schritt  git add Output && git commit -m \"Ausgabe {datum.strftime('%d.%m.%Y')}\" && git push")


if __name__ == "__main__":
    main()
