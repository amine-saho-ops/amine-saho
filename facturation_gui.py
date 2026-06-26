#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================
  GARAGE ALPINE — Facturation MADERASATI
  AO/05/2025 — Lot 1 & Lot 2 | Agrée SNTL 2115
================================================
  Saisie minimale : N° Facture + Matricule + KM + Montant HT
  Sélection       : Type d'intervention
  Le reste        : 100% automatique
================================================
"""

import os
from datetime import date
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# ── CONFIG ──────────────────────────────────────────────────
LOGO_PATH  = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo_garage_alpine.png")
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGE_W, PAGE_H = A4
BLACK   = colors.HexColor('#000000')
GRAY_BG = colors.HexColor('#f2f2f2')
GRAY_D  = colors.HexColor('#d9d9d9')
WHITE   = colors.white

# ── PARC COMPLET ────────────────────────────────────────────
PARC = {
    "160841":{"mk":"HYUNDAI","mo":"COUNTY","pa":"SKHIRAT",         "lot":"2"},
    "160842":{"mk":"HYUNDAI","mo":"COUNTY","pa":"SYZ",             "lot":"2"},
    "160843":{"mk":"HYUNDAI","mo":"COUNTY","pa":"SYZ",             "lot":"2"},
    "197542":{"mk":"IVECO",  "mo":"DAILY", "pa":"SKHIRAT",         "lot":"2"},
    "197543":{"mk":"IVECO",  "mo":"DAILY", "pa":"SYZ",             "lot":"2"},
    "206087":{"mk":"RENAULT","mo":"MASTER","pa":"SKHIRAT",         "lot":"2"},
    "206088":{"mk":"RENAULT","mo":"MASTER","pa":"SYZ",             "lot":"2"},
    "207899":{"mk":"CITROEN","mo":"JUMPER","pa":"SYZ",             "lot":"2"},
    "207901":{"mk":"CITROEN","mo":"JUMPER","pa":"SYZ",             "lot":"2"},
    "207903":{"mk":"CITROEN","mo":"JUMPER","pa":"SKHIRAT",         "lot":"2"},
    "220708":{"mk":"HYUNDAI","mo":"H350",  "pa":"SKHIRAT",         "lot":"2"},
    "220715":{"mk":"HYUNDAI","mo":"H350",  "pa":"SKHIRAT",         "lot":"2"},
    "236374":{"mk":"CITROEN","mo":"JUMPER","pa":"SYZ",             "lot":"2"},
    "237757":{"mk":"HYUNDAI","mo":"H350",  "pa":"SKHIRAT",         "lot":"2"},
    "248364":{"mk":"FIAT",   "mo":"DUCATO","pa":"SYZ",             "lot":"2"},
    "248365":{"mk":"FIAT",   "mo":"DUCATO","pa":"SYZ",             "lot":"2"},
    "255348":{"mk":"RENAULT","mo":"MASTER","pa":"SKHIRAT",         "lot":"2"},
    "255349":{"mk":"RENAULT","mo":"MASTER","pa":"SKHIRAT",         "lot":"2"},
    "259882":{"mk":"RENAULT","mo":"MASTER","pa":"SYZ",             "lot":"2"},
    "262178":{"mk":"IVECO",  "mo":"DAILY", "pa":"SKHIRAT",         "lot":"2"},
    "262179":{"mk":"IVECO",  "mo":"DAILY", "pa":"SKHIRAT",         "lot":"2"},
    "262180":{"mk":"IVECO",  "mo":"DAILY", "pa":"SYZ",             "lot":"2"},
    "217723":{"mk":"FORD",   "mo":"TRANSIT","pa":"AMEUR-BOUKNADEL","lot":"1"},
    "217724":{"mk":"FORD",   "mo":"TRANSIT","pa":"AMEUR-BOUKNADEL","lot":"1"},
    "222355":{"mk":"RENAULT","mo":"MASTER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "222356":{"mk":"RENAULT","mo":"MASTER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "236869":{"mk":"CITROEN","mo":"JUMPER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "236870":{"mk":"CITROEN","mo":"JUMPER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "236976":{"mk":"CITROEN","mo":"JUMPER","pa":"EL ARJAT-SEHOUL", "lot":"1"},
    "238403":{"mk":"FORD",   "mo":"TRANSIT","pa":"AMEUR-BOUKNADEL","lot":"1"},
    "253448":{"mk":"CITROEN","mo":"JUMPER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "254656":{"mk":"FIAT",   "mo":"DUCATO","pa":"EL ARJAT-SEHOUL", "lot":"1"},
    "254657":{"mk":"FIAT",   "mo":"DUCATO","pa":"EL ARJAT-SEHOUL", "lot":"1"},
    "254675":{"mk":"RENAULT","mo":"MASTER","pa":"EL ARJAT-SEHOUL", "lot":"1"},
    "254686":{"mk":"RENAULT","mo":"MASTER","pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "259876":{"mk":"RENAULT","mo":"MASTER","pa":"EL ARJAT-SEHOUL", "lot":"1"},
    "262173":{"mk":"IVECO",  "mo":"DAILY", "pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "262174":{"mk":"IVECO",  "mo":"DAILY", "pa":"AMEUR-BOUKNADEL", "lot":"1"},
    "262175":{"mk":"IVECO",  "mo":"DAILY", "pa":"EL ARJAT-SEHOUL", "lot":"1"},
}

# ── ARTICLES PAR INTERVENTION ───────────────────────────────
INTERVENTIONS = {
    "1": "Vidange complète",
    "2": "Système de freinage",
    "3": "Suspension / Direction",
    "4": "Système Embrayage",
    "5": "Réparation moteur",
    "6": "Autre intervention",
}

def get_items(mk, mo, code_interv, ht):
    """Génère les lignes articles selon intervention et marque/modèle."""
    if code_interv == "1":
        # Vidange — articles détaillés selon marque
        if mk == "HYUNDAI" and mo == "COUNTY":
            return [
                {"qte":"8","desig":"Huile à Moteur",               "ref":"5W30",       "marque":"VIPER",   "pu":"90,00", "pt":"720,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"3194545700", "marque":"HYUNDAI", "pu":"120,00","pt":"120,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"P3033",      "marque":"BOSCH",   "pu":"130,00","pt":"130,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"281305H002", "marque":"HYUNDAI", "pu":"240,00","pt":"240,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",          "marque":"-",       "pu":"200,00","pt":"200,00"},
            ]
        elif mk == "HYUNDAI" and mo == "H350":
            return [
                {"qte":"7","desig":"Huile à Moteur",               "ref":"5W30",       "marque":"VIPER",   "pu":"90,00","pt":"630,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"31922-2E900","marque":"HYUNDAI", "pu":"95,00","pt":"95,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"26300-35504","marque":"HYUNDAI", "pu":"110,00","pt":"110,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"28113-4H000","marque":"HYUNDAI", "pu":"180,00","pt":"180,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",          "marque":"-",       "pu":"200,00","pt":"200,00"},
            ]
        elif mk == "RENAULT" and mo == "MASTER":
            return [
                {"qte":"6","desig":"Huile à Moteur",               "ref":"5W30",    "marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"7701478072","marque":"RENAULT","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"8200768927","marque":"RENAULT","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"8200048662","marque":"RENAULT","pu":"150,00","pt":"150,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",       "marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk == "CITROEN" and mo == "JUMPER":
            return [
                {"qte":"6","desig":"Huile à Moteur",               "ref":"5W30",    "marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"1906.A3", "marque":"CITROEN","pu":"95,00","pt":"95,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"1109.AY", "marque":"CITROEN","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"1444.VH", "marque":"CITROEN","pu":"155,00","pt":"155,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",       "marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk == "FIAT" and mo == "DUCATO":
            return [
                {"qte":"6","desig":"Huile à Moteur",               "ref":"5W30",       "marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"504179764",  "marque":"FIAT","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"2995655",    "marque":"FIAT","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"504049776",  "marque":"FIAT","pu":"150,00","pt":"150,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",          "marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk == "IVECO" and mo == "DAILY":
            return [
                {"qte":"7","desig":"Huile à Moteur",               "ref":"5W30",      "marque":"VIPER","pu":"90,00","pt":"630,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"504179864", "marque":"IVECO","pu":"95,00","pt":"95,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"2992389",   "marque":"IVECO","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"2994048",   "marque":"IVECO","pu":"160,00","pt":"160,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",         "marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk == "FORD" and mo == "TRANSIT":
            return [
                {"qte":"7","desig":"Huile à Moteur",               "ref":"5W30",    "marque":"VIPER","pu":"90,00","pt":"630,00"},
                {"qte":"1","desig":"Filtre à gasoil",               "ref":"BK2Q9176AA","marque":"FORD","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile",                 "ref":"1806860",   "marque":"FORD","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air",                  "ref":"1808491",   "marque":"FORD","pu":"155,00","pt":"155,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-",         "marque":"-","pu":"200,00","pt":"200,00"},
            ]
        else:
            return [{"qte":"1","desig":"Vidange complète","ref":"-","marque":"-",
                     "pu":f"{ht:.2f}","pt":f"{ht:.2f}"}]
    # Autres interventions — 1 ligne + MO
    label = INTERVENTIONS.get(code_interv, "Prestation")
    mo_ht = 200.0
    pieces_ht = round(ht - mo_ht, 2)
    return [
        {"qte":"1","desig":label,                          "ref":"-","marque":"-",
         "pu":f"{pieces_ht:.2f}","pt":f"{pieces_ht:.2f}"},
        {"qte":"1","desig":"Main D'oeuvre",                "ref":"-","marque":"-",
         "pu":f"{mo_ht:.2f}","pt":f"{mo_ht:.2f}"},
    ]

# ── MONTANT EN LETTRES ──────────────────────────────────────
def en_lettres(n):
    n = round(n)
    u=['','un','deux','trois','quatre','cinq','six','sept','huit','neuf','dix',
       'onze','douze','treize','quatorze','quinze','seize','dix-sept','dix-huit','dix-neuf']
    d=['','','vingt','trente','quarante','cinquante','soixante','soixante','quatre-vingt','quatre-vingt']
    def b100(x):
        if x<20: return u[x]
        t,r=divmod(x,10)
        if t in(7,9): return d[t]+('-et-'if r==1 and t==7 else'-')+u[10+r]
        return d[t]+('-et-'if r==1 and t!=8 else('-'+u[r]if r else''))
    def b1000(x):
        if x<100: return b100(x)
        h,r=divmod(x,100)
        return('cent'if h==1 else u[h]+' cent')+(' '+b100(r)if r else'')
    if n==0: return 'zéro'
    if n<1000: return b1000(n)
    k,r=divmod(n,1000)
    return('mille'if k==1 else b1000(k)+' mille')+(' '+b1000(r)if r else'')

# ── EN-TÊTE COMMUN ──────────────────────────────────────────
def draw_header(c, doc_label, num, date_, client, ice, lot, commande, marque, matricule, km):
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH, 10*mm, PAGE_H-38*mm, width=85*mm, height=28*mm,
                    preserveAspectRatio=True, anchor='nw', mask='auto')
    c.setFont('Helvetica',6.5); c.setFillColor(BLACK)
    c.drawCentredString(PAGE_W/2, PAGE_H-42*mm,
        'Mécanique Général - Diagnostic par scanner - Electricité Auto - Carrosserie – Pièces de rechange')
    c.setFont('Helvetica-Bold',11)
    c.drawCentredString(PAGE_W/2, PAGE_H-49*mm, 'Agrée par SNTL 2115')
    y_sep = PAGE_H-52*mm
    c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.line(10*mm, y_sep, PAGE_W-10*mm, y_sep)
    y0=y_sep-6*mm; lh=5.5*mm
    left=[('Le :',date_),(f'{doc_label} N° :',num),
          ('N Commande :',commande),('Client :',client),
          ('ICE:',ice+'    Lot : '+lot)]
    right=[('Marque:',marque),('M :',str(matricule)),
           ('KM :',f"{int(km):,}".replace(',',' ')),('',''),('SYZ','')]
    for i,(lb,val) in enumerate(left):
        y=y0-i*lh
        c.setFont('Helvetica-Bold',8.5); c.setFillColor(BLACK); c.drawString(10*mm,y,lb)
        c.setFont('Helvetica',8.5); c.drawString(40*mm,y,val)
    for i,(lb,val) in enumerate(right):
        y=y0-i*lh
        if lb:
            c.setFont('Helvetica-Bold',8.5); c.drawString(120*mm,y,lb)
            c.setFont('Helvetica',8.5); c.drawString(138*mm,y,val)
    return y0-len(left)*lh-4*mm

def draw_footer(c, y):
    box_h=22*mm
    c.setFillColor(GRAY_BG); c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.rect(10*mm,y-box_h,PAGE_W-20*mm,box_h,fill=1,stroke=1)
    c.setFillColor(BLACK); c.setFont('Helvetica',7.5)
    lines=['Adresse : Lot Oued Eddahab : N°71 Rue Settat –TEMARA – GSM : /0669555344',
           'Fax :0537644498 R.C N°87718 – Patente N°:27935719- Banque B.M.C.E– Cpt(N°011810000004210000848008)',
           '/ICE:001860625000007  _']
    yy=y-6*mm
    for l in lines: c.drawCentredString(PAGE_W/2,yy,l); yy-=5*mm

def draw_table(c, y, col_w, headers, items, with_prices=True, min_rows=20):
    x0=10*mm; row_h=6.5*mm; hdr_h=7.5*mm
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.6)
    c.rect(x0,y-hdr_h,sum(col_w),hdr_h,fill=1,stroke=1)
    c.setFillColor(BLACK); c.setFont('Helvetica-Bold',8)
    xx=x0
    for h,w in zip(headers,col_w):
        c.drawCentredString(xx+w/2,y-hdr_h+2.5*mm,h); xx+=w
    y-=hdr_h
    total_rows=max(len(items),min_rows)
    keys_f=['qte','desig','ref','marque','pu','pt']
    keys_b=['qte','desig','ref','marque']
    keys=keys_f if with_prices else keys_b
    for idx in range(total_rows):
        bg=GRAY_BG if idx%2==1 else WHITE
        c.setFillColor(bg); c.setStrokeColor(BLACK); c.setLineWidth(0.3)
        c.rect(x0,y-row_h,sum(col_w),row_h,fill=1,stroke=1)
        if idx<len(items):
            row=items[idx]
            c.setFillColor(BLACK); c.setFont('Helvetica',8)
            xx=x0
            for i,(k,w) in enumerate(zip(keys,col_w)):
                v=str(row.get(k,''))
                if i==0 or (with_prices and i>=4): c.drawCentredString(xx+w/2,y-row_h+2*mm,v)
                else: c.drawString(xx+2*mm,y-row_h+2*mm,v)
                xx+=w
        elif with_prices:
            c.setFillColor(BLACK); c.setFont('Helvetica',8)
            c.drawCentredString(x0+sum(col_w)-col_w[-1]/2,y-row_h+2*mm,'-')
        y-=row_h
    c.setStrokeColor(BLACK); c.setLineWidth(0.8)
    c.rect(x0,y,sum(col_w),hdr_h+total_rows*row_h,fill=0,stroke=1)
    return y

# ── GÉNÉRATION PDF ──────────────────────────────────────────
def generer_facture(data, items, out):
    c=canvas.Canvas(out,pagesize=A4)
    y=draw_header(c,'Facture',data['num'],data['date'],data['client'],data['ice'],
                  data['lot'],data['commande'],data['marque'],data['matricule'],data['km'])
    col_w=[18*mm,68*mm,28*mm,24*mm,24*mm,26*mm]
    hdrs=['Quantité','Désignation','Ref','Marque','Prix Unitaire','Prix Total']
    y=draw_table(c,y,col_w,hdrs,items,with_prices=True)
    ht=data['ht']; tva=round(ht*0.2,2); ttc=round(ht+tva,2)
    y-=2*mm
    for i,(lb,val,bold) in enumerate([
        ('Total HT', f'{ht:,.2f}'.replace(',',''), False),
        ('TVA 20%',  f'{tva:,.2f}'.replace(',',''), False),
        ('Total TTC',f'{ttc:,.2f}'.replace(',',''), True)]):
        c.setFillColor(GRAY_D if bold else GRAY_BG)
        c.setStrokeColor(BLACK); c.setLineWidth(0.5)
        c.rect(125*mm,y-7*mm,75*mm,7*mm,fill=1,stroke=1)
        c.setFillColor(BLACK); c.setFont('Helvetica-Bold'if bold else'Helvetica',8.5)
        c.drawString(127*mm,y-5.5*mm,lb)
        c.drawRightString(PAGE_W-12*mm,y-5.5*mm,val)
        y-=7*mm
    y-=4*mm
    c.setFont('Helvetica-Bold',8); c.setFillColor(BLACK)
    c.drawString(10*mm,y,'La présent facture est arrêtée à la somme de  '
                 +en_lettres(ttc).capitalize()+' dirhams.')
    draw_footer(c,y-12*mm)
    c.save()

def generer_bl(data, items, out):
    c=canvas.Canvas(out,pagesize=A4)
    y=draw_header(c,'BL',data['num'],data['date'],data['client'],data['ice'],
                  data['lot'],data['commande'],data['marque'],data['matricule'],data['km'])
    col_w=[18*mm,88*mm,36*mm,38*mm]
    hdrs=['Quantité','Désignation','Ref','Marque']
    y=draw_table(c,y,col_w,hdrs,items,with_prices=False)
    draw_footer(c,y-10*mm)
    c.save()

# ── INTERFACE ───────────────────────────────────────────────
def ligne(n=52): print("─"*n)

def saisir_num():
    print("\n  ┌─ N° Facture ───────────────────────────────┐")
    print("  │  Format : AO/05/2025-L1-XXX ou L2-XXX      │")
    print("  └─────────────────────────────────────────────┘")
    return input("  N° Facture : ").strip()

def saisir_matricule():
    while True:
        mat = input("  Matricule : ").strip()
        if mat in PARC:
            v = PARC[mat]
            print(f"\n  ✅ Trouvé automatiquement :")
            print(f"     Marque   : {v['mk']} {v['mo']}")
            print(f"     Parc     : {v['pa']}")
            print(f"     Lot      : {v['lot']}")
            return mat, v
        else:
            print(f"  ⚠️  Matricule '{mat}' non trouvé. Réessayez.")

def choisir_intervention():
    print("\n  ┌─ Type d'intervention ───────────────────────┐")
    for k,v in INTERVENTIONS.items():
        print(f"  │  {k}. {v:<41}│")
    print("  └─────────────────────────────────────────────┘")
    while True:
        c = input("  Choix (1-6) : ").strip()
        if c in INTERVENTIONS: return c
        print("  ⚠️  Choix invalide, entrez 1 à 6.")

def main():
    while True:
        print()
        ligne()
        print("   GARAGE ALPINE — Facturation MADERASATI")
        print("   AO/05/2025  |  Agrée SNTL 2115")
        ligne()
        print("\n  1. Générer  Facture + BL")
        print("  2. Générer  BL uniquement")
        print("  3. Générer  Facture uniquement")
        print("  0. Quitter")
        choix = input("\n  Votre choix : ").strip()
        if choix == "0":
            print("\n  Au revoir! بسلامة 👋\n"); break
        if choix not in ("1","2","3"):
            print("  Choix invalide."); continue

        ligne()
        print("  SAISIE — 4 champs seulement")
        ligne()

        # 1. N° Facture
        num = saisir_num()

        # 2. Matricule → tout automatique
        print()
        mat, v = saisir_matricule()
        mk  = v['mk']; mo = v['mo']; pa = v['pa']; lot = v['lot']
        marque_full = f"{mk}-{mo}"

        # 3. KM
        while True:
            km_str = input("\n  KM actuel : ").strip()
            if km_str.isdigit(): km = int(km_str); break
            print("  ⚠️  Entrez un nombre valide.")

        # 4. Montant HT
        while True:
            try:
                ht = float(input("  Total HT (DH) : ").strip().replace(',','.'))
                break
            except: print("  ⚠️  Montant invalide.")

        # 5. Intervention
        code_interv = choisir_intervention()

        # Date auto
        today = date.today().strftime('%d/%m/%y')

        # Articles auto
        items = get_items(mk, mo, code_interv, ht)

        data = {
            "num"      : num,
            "date"     : today,
            "client"   : "Maderasati",
            "ice"      : "003343121000053",
            "lot"      : lot,
            "commande" : "AO/05/2025",
            "marque"   : marque_full,
            "matricule": mat,
            "km"       : km,
            "ht"       : ht,
        }

        safe = num.replace("/","_").replace(" ","-")
        f_f  = os.path.join(OUTPUT_DIR, f"Facture_{safe}.pdf")
        f_b  = os.path.join(OUTPUT_DIR, f"BL_{safe}.pdf")

        ligne()
        print("  Génération en cours...")
        if choix in ("1","3"): generer_facture(data, items, f_f)
        if choix in ("1","2"): generer_bl(data, items, f_b)

        print("\n  ✅ Documents prêts dans le dossier output/")
        if choix in ("1","3"): print(f"     📄 {os.path.basename(f_f)}")
        if choix in ("1","2"): print(f"     📋 {os.path.basename(f_b)}")
        ligne()

        # ── IMPRESSION AUTOMATIQUE ──────────────────
        imp = input("\n  Imprimer Facture + BL maintenant ? (o/n) : ").strip().lower()
        if imp == 'o':
            import subprocess, sys
            print("\n  Impression en cours...")
            try:
                if sys.platform == "win32":
                    # Windows — ouvre Adobe Reader ou Edge pour imprimer
                    if choix in ("1","3"):
                        subprocess.Popen(f'rundll32 mshtml.dll,PrintHTML "{f_f}"', shell=True)
                        subprocess.Popen(f'start /wait "" "{f_f}"', shell=True)
                    if choix in ("1","2"):
                        subprocess.Popen(f'start /wait "" "{f_b}"', shell=True)
                else:
                    if choix in ("1","3"): subprocess.run(['lp', f_f])
                    if choix in ("1","2"): subprocess.run(['lp', f_b])
                print("  OK - Fichiers ouverts pour impression!")
                print(f"  Dossier : {OUTPUT_DIR}")
            except Exception as e:
                print(f"  Erreur : {e}")
                print(f"  Ouvrez manuellement : {OUTPUT_DIR}")
        ligne()

        suite = input("\n  Autre document ? (o/n) : ").strip().lower()
        if suite != 'o':
            print("\n  Au revoir! بسلامة 👋\n"); break

if __name__ == "__main__":
    main()
