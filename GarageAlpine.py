#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GARAGE ALPINE — Facturation MADERASATI
Interface Graphique (GUI) — Double-clic pour lancer
"""

import os, sys, subprocess
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# ── CHEMINS ─────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH  = os.path.join(BASE_DIR, "logo_garage_alpine.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── COULEURS APP ────────────────────────────────────────────
BG        = "#1e2330"
BG2       = "#252b3b"
BLUE      = "#185FA5"
GREEN     = "#2ecc71"
WHITE     = "#ffffff"
GRAY      = "#8892a4"
LIGHT     = "#f0f4f8"

# ── PARC ────────────────────────────────────────────────────
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

INTERVENTIONS = [
    "Vidange complète",
    "Système de freinage",
    "Suspension / Direction",
    "Système Embrayage",
    "Réparation moteur",
    "Autre intervention",
]

# ── PDF HELPERS ─────────────────────────────────────────────
PAGE_W, PAGE_H = A4
BLK  = colors.HexColor('#000000')
GBG  = colors.HexColor('#f2f2f2')
GDD  = colors.HexColor('#d9d9d9')
WH   = colors.white

def en_lettres(n):
    n=round(n)
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

def get_items(mk, mo, interv, ht):
    if interv == "Vidange complète":
        if mk=="HYUNDAI" and mo=="COUNTY":
            return [
                {"qte":"8","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"720,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"3194545700","marque":"HYUNDAI","pu":"120,00","pt":"120,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"P3033","marque":"BOSCH","pu":"130,00","pt":"130,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"281305H002","marque":"HYUNDAI","pu":"240,00","pt":"240,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk=="RENAULT":
            return [
                {"qte":"6","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"7701478072","marque":"RENAULT","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"8200768927","marque":"RENAULT","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"8200048662","marque":"RENAULT","pu":"150,00","pt":"150,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk=="CITROEN":
            return [
                {"qte":"6","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"1906.A3","marque":"CITROEN","pu":"95,00","pt":"95,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"1109.AY","marque":"CITROEN","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"1444.VH","marque":"CITROEN","pu":"155,00","pt":"155,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk=="FIAT":
            return [
                {"qte":"6","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"540,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"504179764","marque":"FIAT","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"2995655","marque":"FIAT","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"504049776","marque":"FIAT","pu":"150,00","pt":"150,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk=="IVECO":
            return [
                {"qte":"7","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"630,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"504179864","marque":"IVECO","pu":"95,00","pt":"95,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"2992389","marque":"IVECO","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"2994048","marque":"IVECO","pu":"160,00","pt":"160,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
        elif mk=="FORD":
            return [
                {"qte":"7","desig":"Huile à Moteur","ref":"5W30","marque":"VIPER","pu":"90,00","pt":"630,00"},
                {"qte":"1","desig":"Filtre à gasoil","ref":"BK2Q9176AA","marque":"FORD","pu":"90,00","pt":"90,00"},
                {"qte":"1","desig":"Filtreà Huile","ref":"1806860","marque":"FORD","pu":"85,00","pt":"85,00"},
                {"qte":"1","desig":"Filtre à Air","ref":"1808491","marque":"FORD","pu":"155,00","pt":"155,00"},
                {"qte":"1","desig":"Main D'oeuvre Vidange complete","ref":"-","marque":"-","pu":"200,00","pt":"200,00"},
            ]
    mo_ht=200.0; pieces_ht=round(ht-mo_ht,2)
    return [
        {"qte":"1","desig":interv,"ref":"-","marque":"-","pu":f"{pieces_ht:.2f}","pt":f"{pieces_ht:.2f}"},
        {"qte":"1","desig":"Main D'oeuvre","ref":"-","marque":"-","pu":f"{mo_ht:.2f}","pt":f"{mo_ht:.2f}"},
    ]

def draw_header(c, doc_label, num, date_, client, ice, lot, commande, marque, matricule, km):
    if os.path.exists(LOGO_PATH):
        c.drawImage(LOGO_PATH,10*mm,PAGE_H-38*mm,width=85*mm,height=28*mm,
                    preserveAspectRatio=True,anchor='nw',mask='auto')
    c.setFont('Helvetica',6.5); c.setFillColor(BLK)
    c.drawCentredString(PAGE_W/2,PAGE_H-42*mm,
        'Mécanique Général - Diagnostic par scanner - Electricité Auto - Carrosserie – Pièces de rechange')
    c.setFont('Helvetica-Bold',11)
    c.drawCentredString(PAGE_W/2,PAGE_H-49*mm,'Agrée par SNTL 2115')
    y_sep=PAGE_H-52*mm
    c.setStrokeColor(BLK); c.setLineWidth(0.5)
    c.line(10*mm,y_sep,PAGE_W-10*mm,y_sep)
    y0=y_sep-6*mm; lh=5.5*mm
    left=[('Le :',date_),(f'{doc_label} N° :',num),
          ('N Commande :',commande),('Client :',client),
          ('ICE:',ice+'    Lot : '+lot)]
    right=[('Marque:',marque),('M :',str(matricule)),
           ('KM :',f"{int(km):,}".replace(',',' ')),('',''),('SYZ','')]
    for i,(lb,val) in enumerate(left):
        y=y0-i*lh
        c.setFont('Helvetica-Bold',8.5); c.setFillColor(BLK); c.drawString(10*mm,y,lb)
        c.setFont('Helvetica',8.5); c.drawString(40*mm,y,val)
    for i,(lb,val) in enumerate(right):
        y=y0-i*lh
        if lb:
            c.setFont('Helvetica-Bold',8.5); c.drawString(120*mm,y,lb)
            c.setFont('Helvetica',8.5); c.drawString(138*mm,y,val)
    return y0-len(left)*lh-4*mm

def draw_footer(c,y):
    box_h=22*mm
    c.setFillColor(GBG); c.setStrokeColor(BLK); c.setLineWidth(0.5)
    c.rect(10*mm,y-box_h,PAGE_W-20*mm,box_h,fill=1,stroke=1)
    c.setFillColor(BLK); c.setFont('Helvetica',7.5)
    lines=['Adresse : Lot Oued Eddahab : N°71 Rue Settat –TEMARA – GSM : /0669555344',
           'Fax :0537644498 R.C N°87718 – Patente N°:27935719- Banque B.M.C.E– Cpt(N°011810000004210000848008)',
           '/ICE:001860625000007  _']
    yy=y-6*mm
    for l in lines: c.drawCentredString(PAGE_W/2,yy,l); yy-=5*mm

def draw_table(c,y,col_w,headers,items,with_prices=True):
    x0=10*mm; row_h=6.5*mm; hdr_h=7.5*mm
    c.setFillColor(WH); c.setStrokeColor(BLK); c.setLineWidth(0.6)
    c.rect(x0,y-hdr_h,sum(col_w),hdr_h,fill=1,stroke=1)
    c.setFillColor(BLK); c.setFont('Helvetica-Bold',8)
    xx=x0
    for h,w in zip(headers,col_w):
        c.drawCentredString(xx+w/2,y-hdr_h+2.5*mm,h); xx+=w
    y-=hdr_h; keys=list(items[0].keys()) if items else []
    total_rows=max(len(items),20)
    for idx in range(total_rows):
        bg=GBG if idx%2==1 else WH
        c.setFillColor(bg); c.setStrokeColor(BLK); c.setLineWidth(0.3)
        c.rect(x0,y-row_h,sum(col_w),row_h,fill=1,stroke=1)
        if idx<len(items):
            row=items[idx]; c.setFillColor(BLK); c.setFont('Helvetica',8)
            xx=x0
            for i,(k,w) in enumerate(zip(keys,col_w)):
                v=str(row.get(k,''))
                if i==0 or (with_prices and i>=4): c.drawCentredString(xx+w/2,y-row_h+2*mm,v)
                else: c.drawString(xx+2*mm,y-row_h+2*mm,v)
                xx+=w
        elif with_prices:
            c.setFillColor(BLK); c.setFont('Helvetica',8)
            c.drawCentredString(x0+sum(col_w)-col_w[-1]/2,y-row_h+2*mm,'-')
        y-=row_h
    c.setStrokeColor(BLK); c.setLineWidth(0.8)
    c.rect(x0,y,sum(col_w),hdr_h+total_rows*row_h,fill=0,stroke=1)
    return y

def generer_facture(data,items,out):
    c=canvas.Canvas(out,pagesize=A4)
    y=draw_header(c,'Facture',data['num'],data['date'],data['client'],data['ice'],
                  data['lot'],data['commande'],data['marque'],data['matricule'],data['km'])
    col_w=[18*mm,68*mm,28*mm,24*mm,24*mm,26*mm]
    hdrs=['Quantité','Désignation','Ref','Marque','Prix Unitaire','Prix Total']
    y=draw_table(c,y,col_w,hdrs,items,with_prices=True)
    ht=data['ht']; tva=round(ht*0.2,2); ttc=round(ht+tva,2)
    y-=2*mm
    for i,(lb,val,bold) in enumerate([
        ('Total HT',f'{ht:,.2f}'.replace(',',''),False),
        ('TVA 20%',f'{tva:,.2f}'.replace(',',''),False),
        ('Total TTC',f'{ttc:,.2f}'.replace(',',''),True)]):
        c.setFillColor(GDD if bold else GBG)
        c.setStrokeColor(BLK); c.setLineWidth(0.5)
        c.rect(125*mm,y-7*mm,75*mm,7*mm,fill=1,stroke=1)
        c.setFillColor(BLK); c.setFont('Helvetica-Bold'if bold else'Helvetica',8.5)
        c.drawString(127*mm,y-5.5*mm,lb)
        c.drawRightString(PAGE_W-12*mm,y-5.5*mm,val)
        y-=7*mm
    y-=4*mm
    c.setFont('Helvetica-Bold',8); c.setFillColor(BLK)
    c.drawString(10*mm,y,'La présent facture est arrêtée à la somme de  '+en_lettres(ttc).capitalize()+' dirhams.')
    draw_footer(c,y-12*mm); c.save()

def generer_bl(data,items,out):
    c=canvas.Canvas(out,pagesize=A4)
    y=draw_header(c,'BL',data['num'],data['date'],data['client'],data['ice'],
                  data['lot'],data['commande'],data['marque'],data['matricule'],data['km'])
    col_w=[18*mm,88*mm,36*mm,38*mm]
    hdrs=['Quantité','Désignation','Ref','Marque']
    bl_items=[{k:v for k,v in zip(('qte','desig','ref','marque'),
               [r['qte'],r['desig'],r['ref'],r['marque']])} for r in items]
    y=draw_table(c,y,col_w,hdrs,bl_items,with_prices=False)
    draw_footer(c,y-10*mm); c.save()

# ── GUI ─────────────────────────────────────────────────────
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Garage Alpine — Facturation MADERASATI")
        self.geometry("520x620")
        self.resizable(False,False)
        self.configure(bg=BG)
        self._build()

    def _lbl(self,parent,text,fg=GRAY,size=10,bold=False):
        weight = "bold" if bold else "normal"
        return tk.Label(parent,text=text,bg=BG2,fg=fg,
                        font=("Segoe UI",size,weight))

    def _entry(self,parent,textvariable=None,width=30):
        return tk.Entry(parent,textvariable=textvariable,width=width,
                        bg="#2e3650",fg=WHITE,insertbackground=WHITE,
                        relief="flat",font=("Segoe UI",11),bd=6)

    def _build(self):
        # ── HEADER ──
        hdr=tk.Frame(self,bg=BLUE,pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr,text="🔧 GARAGE ALPINE",bg=BLUE,fg=WHITE,
                 font=("Segoe UI",15,"bold")).pack()
        tk.Label(hdr,text="Facturation MADERASATI — AO/05/2025",bg=BLUE,fg="#cce0ff",
                 font=("Segoe UI",10)).pack()

        # ── FORM ──
        frm=tk.Frame(self,bg=BG2,padx=28,pady=20)
        frm.pack(fill="both",expand=True,padx=16,pady=12)

        # N° Facture
        self._lbl(frm,"N° Facture",WHITE,10,True).grid(row=0,column=0,sticky="w",pady=(0,2))
        self.v_num=tk.StringVar()
        self._entry(frm,self.v_num).grid(row=1,column=0,columnspan=2,sticky="ew",pady=(0,12))

        # Matricule
        self._lbl(frm,"Matricule",WHITE,10,True).grid(row=2,column=0,sticky="w",pady=(0,2))
        mat_frm=tk.Frame(frm,bg=BG2)
        mat_frm.grid(row=3,column=0,columnspan=2,sticky="ew",pady=(0,4))
        self.v_mat=tk.StringVar()
        e=self._entry(mat_frm,self.v_mat,15)
        e.pack(side="left")
        e.bind("<FocusOut>",lambda e:self._auto_fill())
        e.bind("<Return>",lambda e:self._auto_fill())
        tk.Button(mat_frm,text="🔍 Chercher",command=self._auto_fill,
                  bg=BLUE,fg=WHITE,relief="flat",font=("Segoe UI",10),
                  padx=10,cursor="hand2").pack(side="left",padx=(8,0))

        # Info auto
        self.info_var=tk.StringVar(value="")
        self.info_lbl=tk.Label(frm,textvariable=self.info_var,bg=BG2,
                               fg=GREEN,font=("Segoe UI",10),justify="left")
        self.info_lbl.grid(row=4,column=0,columnspan=2,sticky="w",pady=(0,10))

        # KM
        self._lbl(frm,"KM actuel",WHITE,10,True).grid(row=5,column=0,sticky="w",pady=(0,2))
        self.v_km=tk.StringVar()
        self._entry(frm,self.v_km,15).grid(row=6,column=0,sticky="w",pady=(0,12))

        # Montant HT
        self._lbl(frm,"Total HT (DH)",WHITE,10,True).grid(row=5,column=1,sticky="w",pady=(0,2),padx=(20,0))
        self.v_ht=tk.StringVar()
        ht_e=self._entry(frm,self.v_ht,15)
        ht_e.grid(row=6,column=1,sticky="w",pady=(0,12),padx=(20,0))
        self.v_ht.trace_add("write",self._calc_ttc)

        # TTC auto
        self.v_ttc=tk.StringVar(value="TTC : —")
        tk.Label(frm,textvariable=self.v_ttc,bg=BG2,fg="#f0c040",
                 font=("Segoe UI",11,"bold")).grid(row=7,column=1,sticky="w",padx=(20,0))

        # Intervention
        self._lbl(frm,"Type d'intervention",WHITE,10,True).grid(row=7,column=0,sticky="w",pady=(0,2))
        self.v_interv=tk.StringVar(value=INTERVENTIONS[0])
        cb=ttk.Combobox(frm,textvariable=self.v_interv,values=INTERVENTIONS,
                        state="readonly",font=("Segoe UI",10),width=28)
        cb.grid(row=8,column=0,columnspan=2,sticky="ew",pady=(4,16))

        # Impression
        self.v_print=tk.BooleanVar(value=True)
        tk.Checkbutton(frm,text="🖨️  Imprimer automatiquement après génération",
                       variable=self.v_print,bg=BG2,fg=WHITE,
                       selectcolor=BG2,activebackground=BG2,
                       font=("Segoe UI",10)).grid(row=9,column=0,columnspan=2,sticky="w",pady=(0,16))

        # Boutons
        btn_frm=tk.Frame(frm,bg=BG2)
        btn_frm.grid(row=10,column=0,columnspan=2,sticky="ew")

        tk.Button(btn_frm,text="📄  Facture + BL",command=lambda:self._generer("both"),
                  bg=BLUE,fg=WHITE,relief="flat",font=("Segoe UI",11,"bold"),
                  pady=10,cursor="hand2",width=16).pack(side="left",padx=(0,8))
        tk.Button(btn_frm,text="📋  BL seul",command=lambda:self._generer("bl"),
                  bg="#2d6a4f",fg=WHITE,relief="flat",font=("Segoe UI",11,"bold"),
                  pady=10,cursor="hand2",width=12).pack(side="left",padx=(0,8))
        tk.Button(btn_frm,text="📄  Facture seule",command=lambda:self._generer("facture"),
                  bg="#6d4c41",fg=WHITE,relief="flat",font=("Segoe UI",11,"bold"),
                  pady=10,cursor="hand2",width=14).pack(side="left")

        # Status
        self.status=tk.StringVar(value="")
        tk.Label(self,textvariable=self.status,bg=BG,fg=GREEN,
                 font=("Segoe UI",10),wraplength=480).pack(pady=8)

        # Footer
        tk.Label(self,text="Agrée par SNTL 2115  |  Lot Oued Eddahab N°71 – TEMARA",
                 bg=BG,fg=GRAY,font=("Segoe UI",8)).pack(side="bottom",pady=6)

        frm.columnconfigure(0,weight=1)
        frm.columnconfigure(1,weight=1)

    def _auto_fill(self):
        mat=self.v_mat.get().strip()
        if mat in PARC:
            v=PARC[mat]
            self.info_var.set(f"✅  {v['mk']} {v['mo']}  |  Parc : {v['pa']}  |  Lot {v['lot']}")
            self.info_lbl.config(fg=GREEN)
            # Auto HT Vidange
            if v['mk']=="HYUNDAI" and v['mo']=="COUNTY":
                self.v_ht.set("1410")
            elif v['mk'] in ("RENAULT","CITROEN","FIAT"):
                self.v_ht.set("1060")
            elif v['mk'] in ("IVECO","FORD"):
                self.v_ht.set("1175")
        else:
            self.info_var.set("⚠️  Matricule non trouvé dans le parc")
            self.info_lbl.config(fg="#e74c3c")

    def _calc_ttc(self,*a):
        try:
            ht=float(self.v_ht.get().replace(',','.'))
            ttc=round(ht*1.2,2)
            self.v_ttc.set(f"TTC : {ttc:,.2f} DH".replace(',',''))
        except: self.v_ttc.set("TTC : —")

    def _generer(self, mode):
        num   = self.v_num.get().strip()
        mat   = self.v_mat.get().strip()
        km    = self.v_km.get().strip()
        ht_s  = self.v_ht.get().strip().replace(',','.')
        interv= self.v_interv.get()

        if not all([num,mat,km,ht_s]):
            messagebox.showerror("Champs manquants","Veuillez remplir tous les champs !")
            return
        if mat not in PARC:
            messagebox.showerror("Matricule","Matricule non trouvé dans le parc !")
            return
        try: ht=float(ht_s)
        except: messagebox.showerror("Montant","Montant HT invalide !"); return

        v=PARC[mat]; mk=v['mk']; mo=v['mo']
        data={
            "num":num,"date":date.today().strftime('%d/%m/%y'),
            "client":"Maderasati","ice":"003343121000053",
            "lot":v['lot'],"commande":"AO/05/2025",
            "marque":f"{mk}-{mo}","matricule":mat,"km":km,"ht":ht,
        }
        items=get_items(mk,mo,interv,ht)
        safe=num.replace("/","_").replace(" ","-")
        f_f=os.path.join(OUTPUT_DIR,f"Facture_{safe}.pdf")
        f_b=os.path.join(OUTPUT_DIR,f"BL_{safe}.pdf")

        try:
            if mode in ("both","facture"): generer_facture(data,items,f_f)
            if mode in ("both","bl"):      generer_bl(data,items,f_b)

            msg="✅  Documents générés !\n"
            if mode in ("both","facture"): msg+=f"📄 {os.path.basename(f_f)}\n"
            if mode in ("both","bl"):      msg+=f"📋 {os.path.basename(f_b)}"
            self.status.set(msg)

            # Impression auto
            if self.v_print.get():
                if mode in ("both","facture"): os.startfile(f_f,"print")
                if mode in ("both","bl"):      os.startfile(f_b,"print")

            # Ouvrir dossier output
            os.startfile(OUTPUT_DIR)

        except Exception as e:
            messagebox.showerror("Erreur",str(e))

if __name__=="__main__":
    App().mainloop()
