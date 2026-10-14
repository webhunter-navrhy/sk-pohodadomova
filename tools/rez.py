#!/usr/bin/env python3
"""Vygeneruje src/_rez.html – technický rez domom so systémami TZB (signature úvodnej stránky)."""
import os
E = "https://www.pohodadomova.sk"
C = dict(teplo="#d82430", voda="#0090d8", vzduch="#3a9a3a", plyn="#e9a800", odpad="#181818")

def rura(d, farba, w=3.2, cls=""):
    return (f'<path class="rura {cls}" d="{d}" stroke="{farba}" stroke-width="{w}"/>'
            f'<path class="tok" d="{d}" stroke-width="{max(w-1.6,1.4)}"/>')

def body(x0, x1, y, krok, farba, r=3.6):
    out = []
    for i, x in enumerate(range(x0, x1 + 1, krok)):
        out.append(f'<circle class="bod" style="--i:{i}" cx="{x}" cy="{y}" r="{r}" fill="{farba}"/>')
    return "".join(out)

def stitok(x, y, text, href, farba, kotva="start", sirka=None):
    w = sirka or (len(text) * 8.6 + 34)
    rx = x if kotva == "start" else x - w
    return (f'<a class="stitok" href="{E}{href}" target="_blank" rel="noopener">'
            f'<rect x="{rx}" y="{y-15}" width="{w:.0f}" height="30" rx="15"/>'
            f'<circle cx="{rx+15}" cy="{y}" r="5" fill="{farba}"/>'
            f'<text x="{rx+27}" y="{y+5}">{text}</text></a>')

def main():
    s = []
    s.append('<svg class="rez-svg" viewBox="0 0 800 640" role="img" aria-labelledby="rez-t rez-d" xmlns="http://www.w3.org/2000/svg">')
    s.append('<title id="rez-t">Rez rodinným domom</title><desc id="rez-d">Kde v dome je tepelné čerpadlo, podlahové kúrenie, rekuperácia, fotovoltika, kúpeľňa, voda, plyn a kanalizácia. Štítky vedú do kategórií e-shopu.</desc>')
    s.append('<defs><pattern id="zem" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="12" stroke="#cfc9bb" stroke-width="1.2"/></pattern></defs>')
    # zem
    s.append('<rect class="zem" x="0" y="500" width="800" height="140" fill="url(#zem)"/><line x1="0" y1="500" x2="800" y2="500" class="ciara-zem"/>')
    # dom: steny, stropy, strecha
    s.append('<g class="dom">'
             '<path class="obrys" d="M170 500 V230 M630 230 V500"/>'
             '<path class="doska" d="M164 492 H636 V504 H164 Z"/>'
             '<path class="doska" d="M170 352 H630 V362 H170 Z"/>'
             '<path class="doska" d="M170 226 H630 V234 H170 Z"/>'
             '<path class="strecha" d="M140 236 L400 88 L660 236"/>'
             '<path class="obrys tenka" d="M470 362 V492 M400 234 V352"/>'
             # okná
             '<path class="okno" d="M210 270 h70 v56 h-70 z M245 270 v56"/>'
             '<path class="okno" d="M210 395 h110 v70 h-110 z M265 395 v70"/>'
             # dvere
             '<path class="okno" d="M400 402 h40 v90 h-40 z"/>'
             '</g>')
    # --- TEPLO: tepelné čerpadlo vonku, kotol, rozdeľovač, podlahovka, stropné chladenie
    t = ['<g class="sys" data-sys="teplo">']
    t.append('<rect class="pristroj" x="672" y="432" width="96" height="62" rx="4"/>'
             '<circle class="pristroj-v" cx="704" cy="463" r="21"/><path class="pristroj-v" d="M704 442 v42 M683 463 h42"/>'
             '<path class="obrys tenka" d="M680 494 v6 M760 494 v6"/>')
    t.append(rura("M672 452 H636 M636 452 H560 V420", C["teplo"]))
    t.append(rura("M672 474 H636 M636 474 H574 V420", C["voda"], 2.4, "spiatocka"))
    # vnútorná jednotka + zásobník
    t.append('<rect class="pristroj" x="540" y="372" width="48" height="48" rx="3"/><rect class="pristroj" x="596" y="380" width="26" height="106" rx="13"/>')
    # rozdeľovač
    t.append('<path class="pristroj-v" d="M488 430 h40 M492 424 v12 M502 424 v12 M512 424 v12 M522 424 v12"/>')
    t.append(rura("M540 410 H528 M488 430 H482 V482 H470", C["teplo"]))
    t.append(body(186, 462, 486, 12, C["teplo"]))
    # radiátor hore + stropné chladenie
    t.append(rura("M564 372 V340 H600 V300", C["teplo"], 2.4))
    t.append('<path class="pristroj" d="M592 262 h16 v36 h-16 z M596 262 v36 M600 262 v36 M604 262 v36"/>')
    t.append(body(186, 390, 242, 13, C["voda"], 3.2))
    t.append('</g>')
    s += t
    # --- VZDUCH: rekuperácia v podkroví, fotovoltika na streche
    v = ['<g class="sys" data-sys="vzduch">']
    v.append('<rect class="pristroj" x="330" y="180" width="86" height="38" rx="4"/><path class="pristroj-v" d="M346 199 h20 M380 199 h20"/>')
    v.append(rura("M330 196 H250 V236", C["vzduch"], 4.2))
    v.append(rura("M330 210 H200 V352 M200 362 V372", C["vzduch"], 4.2))
    v.append(rura("M416 196 H500 V236", C["vzduch"], 4.2))
    v.append(rura("M372 180 V120 H372 V104", C["vzduch"], 4.2))
    # fotovoltika: panely na pravej strane strechy
    import math
    ang = math.degrees(math.atan2(148, 260))
    v.append(f'<g transform="translate(432 106) rotate({ang:.2f})">' + "".join(
        f'<rect class="panel" x="{i*44}" y="-14" width="40" height="10" rx="1"/>' for i in range(4)) + '</g>')
    v.append('</g>')
    s += v
    # --- VODA: prípojka, úprava vody, kúpeľňa
    w = ['<g class="sys" data-sys="voda">']
    w.append(rura("M800 566 H648 V512 H612 V486", C["voda"], 3.2))
    w.append('<rect class="pristroj" x="640" y="548" width="16" height="36" rx="2"/>')
    w.append(rura("M622 420 H630 V340 H612 V318", C["voda"], 2.4))
    # kúpeľňa: vaňa, WC, umývadlo
    w.append('<path class="pristroj" d="M412 318 h104 v26 q0 8 -8 8 h-88 q-8 0 -8 -8 z"/>'
             '<path class="pristroj" d="M534 310 h8 v18 h22 q4 0 4 6 q0 18 -18 18 h-16 z M534 290 h10 v20 h-10 z"/>'
             '<path class="pristroj" d="M588 314 h34 q0 16 -17 16 q-17 0 -17 -16 z M605 330 v22"/>'
             '<path class="pristroj-v" d="M612 314 v-10 h-8"/>')
    w.append('</g>')
    s += w
    # --- PLYN
    g = ['<g class="sys" data-sys="plyn">']
    g.append(rura("M0 540 H120 V448", C["plyn"], 3.2))
    g.append('<rect class="pristroj" x="104" y="412" width="34" height="40" rx="2"/><path class="pristroj-v" d="M112 424 h18 M112 432 h18"/>')
    g.append(rura("M138 432 H164 M176 378 H540 M170 378 H176", C["plyn"], 2.6))
    g.append(rura("M152 432 V378 H170", C["plyn"], 2.6))
    g.append('</g>')
    s += g
    # --- ODPAD
    o = ['<g class="sys" data-sys="odpad">']
    o.append(rura("M550 352 V362 M550 362 V530 H90", C["odpad"], 5))
    o.append(rura("M470 352 H550", C["odpad"], 4))
    o.append(rura("M550 230 V288 M550 220 V200 M550 200 V150", C["odpad"], 3.4))
    o.append('<path class="pristroj" d="M44 520 h46 v92 h-46 z M38 520 h58"/>')
    o.append('</g>')
    s += o
    # --- štítky (desktop)
    L = [
        (676, 412, "Tepelné čerpadlo", "/tepelnecerpadlo/", "teplo"),
        (186, 470, "Podlahové kúrenie", "/podlahove-kurenie-rehau-uponor-herz/", "teplo"),
        (186, 260, "Stropné chladenie", "/stropne-chladenie-rehau-uponor/", "voda"),
        (478, 392, "Kotol a ohrev", "/kurenie-chladenie/", "teplo"),
        (216, 160, "Rekuperácia", "/rekuperacia-vzduchu/", "vzduch"),
        (560, 128, "Fotovoltika", "/fotovoltaika/", "vzduch"),
        (414, 270, "Kúpeľňa", "/kupelna/", "voda"),
        (650, 604, "Voda", "/vodoinstalacny-material/", "voda"),
        (20, 396, "Plyn", "/plyn/", "plyn"),
        (104, 600, "Kanalizácia", "/kanalizacia/", "odpad"),
    ]
    s.append('<g class="stitky">')
    for x, y, txt, href, sys_ in L:
        s.append(f'<g data-sys="{sys_}">' + stitok(x, y, txt, href, C[sys_]) + '</g>')
    s.append('</g></svg>')
    cesta = os.path.join(os.path.dirname(__file__), "..", "src", "_rez.html")
    open(cesta, "w").write("\n".join(s) + "\n")
    print("ok", cesta)

main()
