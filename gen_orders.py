#!/usr/bin/env python3
"""Generate mock purchase orders for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
import os

COMPANY = "ChemCorp Industries S.A."
COMPANY_ADDR = "14 Rue des Réactifs, 69100 Villeurbanne, France"
BLUE = '#1a3a5c'; LBLUE = '#2d6a9f'; PALE = '#eef4fa'

def p(text, size=9, bold=False, color='#000000', align='LEFT', leading=13, sb=0, sa=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}.get(align, TA_LEFT)
    return Paragraph(text, ParagraphStyle('x', fontSize=size, fontName='Helvetica-Bold' if bold else 'Helvetica',
                                          textColor=colors.HexColor(color), alignment=al, leading=leading,
                                          spaceBefore=sb*cm, spaceAfter=sa*cm))

SUPPLIERS = [
    {"name": "BASF SE", "addr": "Carl-Bosch-Str. 38\n67056 Ludwigshafen, Germany", "contact": "Dr. Klaus Weber — k.weber@basf.com", "lead": "10 working days"},
    {"name": "Solvay S.A.", "addr": "Rue de Ransbeek 310\n1120 Brussels, Belgium", "contact": "Ms Isabelle Fontaine — i.fontaine@solvay.com", "lead": "15 working days"},
    {"name": "Arkema France S.A.S.", "addr": "420 rue d'Estienne d'Orves\n92700 Colombes, France", "contact": "Mr Laurent Brard — l.brard@arkema.com", "lead": "8 working days"},
    {"name": "Brenntag SAS", "addr": "11 allée des Érables\n69760 Limonest, France", "contact": "Ms Sophie Charrier — s.charrier@brenntag.fr", "lead": "5 working days"},
    {"name": "TotalEnergies Fluids", "addr": "2 Place Jean Millier\n92078 Paris La Défense, France", "contact": "Mr Renaud Pelloux — r.pelloux@totalenergies.com", "lead": "12 working days"},
]

ITEMS_CATALOG = [
    ("Ethylene glycol 99.9% polymer grade", "EG-999P", "tonne", 780.00),
    ("Propylene oxide 99%", "PO-99", "tonne", 1450.00),
    ("Maleic anhydride pastilles", "MAH-PAS", "tonne", 920.00),
    ("Technical methanol 99.9%", "MeOH-T", "tonne", 420.00),
    ("Glacial acrylic acid 99%", "AA-GLA", "tonne", 1680.00),
    ("Butyl acrylate", "nBA-99", "tonne", 1540.00),
    ("Inhibited styrene monomer", "STY-INH", "tonne", 1120.00),
    ("Glacial acetic acid 99.8%", "AcOH-G", "tonne", 560.00),
    ("Diethylene glycol (DEG)", "DEG-99", "tonne", 690.00),
    ("Methyl ethyl ketone (MEK)", "MEK-99", "tonne", 980.00),
    ("Stabilised chloroform", "CHCl3-S", "tonne", 2100.00),
    ("Acetic anhydride 99%", "AcO-99", "tonne", 1350.00),
    ("Technical cyclohexane", "CyHex-T", "tonne", 760.00),
    ("Dimethylformamide (DMF)", "DMF-99", "tonne", 1180.00),
    ("Ethyl acetate 99.5%", "EtOAc-T", "tonne", 870.00),
]

ORDERS = [
    {"num": "BC-2024-0142", "date": "2024-01-22", "delivery": "2024-02-05", "supplier": 0,
     "dest": "Villeurbanne site — Warehouse B, dock 3", "buyer": "Mr Alain Rousset, Purchasing Manager",
     "validator": "Ms Hélène Marchand, Operations Director",
     "items": [(0, 5.0), (3, 10.0), (8, 3.0)],
     "inco": "DDP Villeurbanne", "payment": "60 days end of month",
     "notes": "Delivery required between 07:00 and 16:00. Book a slot on 04 72 XX XX XX. Bolted tanker mandatory for MEG and DEG. ADR documents in French are mandatory."},
    {"num": "BC-2024-0218", "date": "2024-02-14", "delivery": "2024-03-01", "supplier": 1,
     "dest": "Roussillon site — Zone A, building 12", "buyer": "Ms Carole Petit, Senior Buyer",
     "validator": "Mr Bertrand Vidal, Production Manager",
     "items": [(1, 2.5), (4, 1.5), (5, 4.0)],
     "inco": "FCA Brussels Incoterms 2020", "payment": "45 days from invoice date",
     "notes": "Products must be delivered before the Q1 campaign start (2024-03-01). Certificates of analysis compliant with ChemCorp spec. QUAL-2024-003 are required. No import via a third-party forwarder without prior agreement."},
    {"num": "BC-2024-0331", "date": "2024-03-07", "delivery": "2024-03-18", "supplier": 2,
     "dest": "Villeurbanne site — Warehouse A", "buyer": "Mr Alain Rousset, Purchasing Manager",
     "validator": "Mr Frédéric Dumont, Technical Director",
     "items": [(6, 8.0), (7, 6.0), (14, 3.5)],
     "inco": "EXW Colombes", "payment": "30 days end of month",
     "notes": "Styrene: compliant TBC inhibitor, content 10-15 ppm verified on the COA. Cold storage required (below 15°C) during transport. Supplier to notify 72h in advance if the lead time cannot be met."},
    {"num": "BC-2024-0445", "date": "2024-04-02", "delivery": "2024-04-15", "supplier": 3,
     "dest": "Villeurbanne site — Warehouse C (solvent products)", "buyer": "Ms Carole Petit, Senior Buyer",
     "validator": "Ms Hélène Marchand, Operations Director",
     "items": [(9, 2.0), (12, 5.0), (13, 1.0), (10, 0.5)],
     "inco": "DDP Villeurbanne", "payment": "60 days end of month",
     "notes": "Automatic replenishment order — framework contract BC-CADRE-2024-003. DMF is classified reprotoxic cat. 1B; restricted access, storage in a ventilated cabinet is mandatory. Delivery by ventilated tanker truck."},
    {"num": "BC-2024-0589", "date": "2024-05-06", "delivery": "2024-05-20", "supplier": 4,
     "dest": "Lyon-Est site — Chemical terminal, bay 7", "buyer": "Mr Alain Rousset, Purchasing Manager",
     "validator": "Mr Bertrand Vidal, Production Manager",
     "items": [(0, 8.0), (3, 15.0), (8, 5.0), (11, 2.0)],
     "inco": "DDP Lyon Incoterms 2020", "payment": "45 days end of month",
     "notes": "Multi-product delivery by compartmented tanker is permitted provided ADR segregation is observed. Transfer pump supplied by ChemCorp. Allow 4h for unloading. Site contact: Mr Renaud Oger, +33 4 XX XX XX XX."},
    {"num": "BC-2024-0672", "date": "2024-06-10", "delivery": "2024-06-24", "supplier": 0,
     "dest": "Villeurbanne site — Warehouse B", "buyer": "Ms Carole Petit, Senior Buyer",
     "validator": "Mr Frédéric Dumont, Technical Director",
     "items": [(1, 3.0), (4, 2.0), (6, 6.0), (9, 3.0)],
     "inco": "CIF Lyon Incoterms 2020", "payment": "60 days from invoice date",
     "notes": "Urgent order following an unexpected stock-out. Firm, non-negotiable lead time. If partial delivery is impossible, contact Ms Petit immediately (07 XX XX XX XX). Late penalty: 0.1% of the order value per day."},
]

def build_order(order, out_dir):
    sup = SUPPLIERS[order['supplier']]
    path = os.path.join(out_dir, f"{order['num']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm)
    story = []

    # Header
    hdr = Table([[
        [p(COMPANY, 14, bold=True, color='#ffffff'), p(COMPANY_ADDR, 8, color='#ccddee')],
        [p(f"PURCHASE ORDER", 14, bold=True, color='#ffffff', align='RIGHT'),
         p(f"No. {order['num']}", 11, bold=True, color='#aaccee', align='RIGHT'),
         p(f"Date: {order['date']}", 9, color='#ccddee', align='RIGHT')]
    ]], colWidths=[10*cm, 7*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (0,-1), 12), ('RIGHTPADDING', (1,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.5*cm))

    # Supplier & Delivery
    sup_block = [
        p("SUPPLIER", 8, bold=True, color=LBLUE),
        p(sup['name'], 11, bold=True),
        p(sup['addr'].replace('\n','<br/>'), 9, color='#333333'),
        Spacer(1, 0.1*cm),
        p(f"Contact: {sup['contact']}", 8.5),
        p(f"Standard lead time: {sup['lead']}", 8.5),
    ]
    del_block = [
        p("REQUESTED DELIVERY", 8, bold=True, color=LBLUE),
        p(f"Requested date: <b>{order['delivery']}</b>", 9),
        Spacer(1, 0.1*cm),
        p("Delivery address:", 8, bold=True),
        p(order['dest'], 9),
        Spacer(1, 0.2*cm),
        p("TERMS", 8, bold=True, color=LBLUE),
        p(f"Incoterms: <b>{order['inco']}</b>", 9),
        p(f"Payment: {order['payment']}", 9),
    ]
    info = Table([[sup_block, del_block]], colWidths=[8.5*cm, 8.5*cm])
    info.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (0,-1), 0.5, colors.lightgrey),
        ('BOX', (1,0), (-1,-1), 0.5, colors.lightgrey),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (1,0), (-1,-1), colors.HexColor(PALE)),
    ]))
    story.append(info)
    story.append(Spacer(1, 0.5*cm))

    # Order lines
    story.append(p("ORDER DETAILS", 10, bold=True, color=BLUE, sb=0.1))
    rows = [['Ref.', 'Description', 'Quantity', 'Unit', 'Unit price (€)', 'Amount excl. VAT (€)']]
    total = 0.0
    for (ci, qty) in order['items']:
        item = ITEMS_CATALOG[ci]
        ref, name, unit, pu = item[1], item[0], item[2], item[3]
        amt = round(qty * pu, 2)
        total += amt
        rows.append([ref, name, f"{qty:,.1f}", unit, f"{pu:,.2f}", f"{amt:,.2f}"])
    tva = round(total * 0.20, 2)
    ttc = round(total + tva, 2)
    rows.append(['', '', '', '', 'Subtotal excl. VAT', f"{total:,.2f}"])
    rows.append(['', '', '', '', 'VAT 20%', f"{tva:,.2f}"])
    rows.append(['', '', '', '', 'TOTAL incl. VAT', f"{ttc:,.2f}"])

    col_w = [2*cm, 6.6*cm, 2*cm, 1.4*cm, 2.5*cm, 3*cm]
    rows[0] = [Paragraph(f"<b>{c}</b>", ParagraphStyle('hc', fontSize=8.5, fontName='Helvetica-Bold',
               textColor=colors.white, leading=10)) for c in rows[0]]
    ot = Table(rows, colWidths=col_w, repeatRows=1)
    n = len(rows)
    ot.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (2,1), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1, n-4), 0.4, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1, n-4), [colors.white, colors.HexColor(PALE)]),
        ('LINEABOVE', (4, n-3), (-1, n-3), 0.8, colors.HexColor(BLUE)),
        ('FONTNAME', (4, n-1), (-1, n-1), 'Helvetica-Bold'),
        ('BACKGROUND', (4, n-1), (-1, n-1), colors.HexColor('#e8f0f8')),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(ot)
    story.append(Spacer(1, 0.4*cm))

    # Notes
    story.append(p("SPECIAL INSTRUCTIONS AND NOTES", 10, bold=True, color=BLUE, sb=0.1))
    story.append(p(order['notes'], 9, color='#333333'))
    story.append(Spacer(1, 0.5*cm))

    # Signatories
    story.append(p("APPROVAL AND SIGNATURES", 10, bold=True, color=BLUE, sb=0.1))
    sig_rows = [
        ['Prepared by', 'Approved by', 'Received and accepted by the supplier'],
        [order['buyer'], order['validator'], ''],
        ['Signature:\n\n\n', 'Signature:\n\n\n', 'Signature:\n\n\n'],
        ['Date:', 'Date:', 'Date:'],
        ['Stamp:', 'Stamp:', 'Supplier stamp:'],
    ]
    sig_rows[0] = [Paragraph(f"<b>{c}</b>", ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', leading=11)) for c in sig_rows[0]]
    sig_rows[1] = [Paragraph(c, ParagraphStyle('sb', fontSize=9, leading=11)) for c in sig_rows[1]]
    sigt = Table(sig_rows, colWidths=[5.7*cm, 5.7*cm, 5.7*cm])
    sigt.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(PALE)),
        ('BOX', (0,0), (-1,-1), 0.5, colors.grey),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sigt)

    # Page 2 — Conditions & Technical requirements
    story.append(PageBreak())
    story.append(p(f"Purchase Order {order['num']} — General Purchasing Conditions", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    cga_articles = [
        ("Art. 1 — Purpose and scope",
         "These general purchasing conditions (GPC) apply to all orders placed by ChemCorp Industries S.A. with its suppliers. They prevail over any general terms of sale issued by the supplier unless an express written derogation is signed by an authorised representative of ChemCorp Industries. Receipt of this purchase order by the supplier constitutes acceptance of these GPC."),
        ("Art. 2 — Prices and revision",
         "The prices stated are firm and final until the delivery date, unless a specific indexation clause is stated on the purchase order. Any price revision must be the subject of a written amendment approved by the ChemCorp Industries purchasing department before execution. Prices are stated excluding VAT, with duties and taxes included under the Incoterms stated."),
        ("Art. 3 — Delivery and transfer of risk",
         "The delivery lead times stated are binding and constitute an essential element of the order. Any delay not notified 72h in advance engages the supplier's liability. Risk transfers according to the Incoterms 2020 specified. Delivery must be accompanied by a delivery note, the certificates of analysis, the safety data sheets (SDS) and ADR documents where applicable."),
        ("Art. 4 — Quality and inspection on receipt",
         "All products delivered must conform to ChemCorp Industries specifications and to the approved product data sheets. ChemCorp Industries reserves the right to reject any non-conforming batch, with return at the supplier's expense. A certificate of analysis (COA) per batch is mandatory. Counter-analysis samples are taken systematically and retained for 24 months."),
        ("Art. 5 — Penalties and liability",
         "In the event of an unjustified delivery delay, penalties of 0.1% of the value excluding VAT per day of delay will be applied, capped at 10%. In the event of a quality non-conformity, ChemCorp Industries reserves the right to terminate the order and claim compensation for the loss suffered, including attributable production losses. The supplier's liability may not be less than the value of the order concerned."),
        ("Art. 6 — Regulations and compliance",
         "The supplier warrants that the products delivered comply with the REACH Regulation (EC) No 1907/2006, the CLP Regulation No 1272/2008, and all regulations applicable in the countries of origin and destination. Safety data sheets must comply with Regulation (EU) 2020/878. The supplier undertakes to notify immediately any change of composition or regulatory classification."),
        ("Art. 7 — Sustainability and CSR",
         "ChemCorp Industries attaches particular importance to ESG criteria. The supplier undertakes to respect the principles of the United Nations Global Compact, to maintain an environmental management system (ISO 14001 or equivalent), and to respect fundamental rights at work (ILO conventions). A CSR audit may be commissioned with 15 working days' notice."),
        ("Art. 8 — Confidentiality",
         "All information exchanged under this order is strictly confidential. The supplier shall not disclose to any third party the technical characteristics, volumes, prices and negotiated terms without the prior written agreement of ChemCorp Industries. This confidentiality obligation continues for 5 years after the last delivery."),
    ]

    for title_a, body in cga_articles:
        story.append(p(f"<b>{title_a}</b>", 9.5, bold=False, sb=0.15))
        story.append(p(body, 9, color='#333333'))

    # Page 3 — Technical requirements
    story.append(PageBreak())
    story.append(p(f"Purchase Order {order['num']} — Technical Specification", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    story.append(p("ChemCorp Industries quality requirements — chemical product suppliers", 10, bold=True, color=LBLUE))
    story.append(Spacer(1, 0.2*cm))

    req_sections = [
        ("Mandatory documentation per delivery", [
            "Certificate of Analysis (COA) — one per batch number, with the reference analytical methods",
            "Safety Data Sheet (SDS) no more than 3 years old, compliant with Regulation (EU) 2020/878",
            "ADR transport documents (transport document, instructions in writing, loader's declaration) where applicable",
            "Delivery note showing the ChemCorp order number, batch number, date of manufacture and best-before date",
            "Certificate of origin where required by customs conditions",
        ]),
        ("Packaging and labelling requirements", [
            "ADR-approved packaging per the 2024 approved packaging list (ref. ADR-2024-Q2)",
            "CLP-compliant labelling: pictograms, H and P statements visible and indelible",
            "Clear identification: batch number, date of manufacture, best-before date, net mass/volume",
            "Clean packaging, free of external residue, with leak-tight caps and valves",
            "Returnable packaging: IBCs to be returned within 60 days, drums within 90 days",
        ]),
        ("Minimum analytical requirements (key parameters)", [
            "Purity: GC or titrimetric method per the applicable EN or ASTM standard (to be specified)",
            "Water content: Karl Fischer (ISO 760 or ASTM E1064)",
            "Colour: APHA/Hazen (ASTM D1209) or Pt-Co",
            "Heavy metals: ICP-OES (EN ISO 11885) — Pb, As, Hg, Cd where applicable",
            "pH: per EN ISO 10523 for aqueous solutions",
            "Density: pycnometer or oscillating densitometer (ASTM D4052)",
        ]),
        ("Traceability and non-conformity management", [
            "Retention samples kept for a minimum of 24 months per batch",
            "Traceability system allowing a batch recall in under 4 hours",
            "Immediate notification to ChemCorp Industries of any specification deviation identified after the fact",
            "Root cause analysis report (8D) within 10 working days for any quality return",
            "On-site audit access granted with 15 days' notice; an annual quality audit is planned",
        ]),
    ]

    for sec_title, items in req_sections:
        story.append(p(f"<b>{sec_title}</b>", 10, bold=False, color=LBLUE, sb=0.2))
        for item in items:
            story.append(p(f"  • {item}", 9, color='#333333'))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.4, color=colors.lightgrey))
    story.append(Spacer(1, 0.2*cm))
    story.append(p(f"Generated by the ChemCorp ERP system | PO {order['num']} | {order['date']} | Buyer: {order['buyer']}", 7.5, color='#666666'))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'website', 'docs', 'orders')
    os.makedirs(out, exist_ok=True)
    for o in ORDERS:
        build_order(o, out)
    print(f"Done — {len(ORDERS)} orders generated.")
