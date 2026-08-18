#!/usr/bin/env python3.11
"""Generate mock invoice PDFs for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
import os

W, H = A4
COMPANY = "ChemCorp Industries S.A."
ADDR = "14 Rue des Réactifs, 69100 Villeurbanne, France"
VAT = "FR 42 387 542 891"
IBAN = "FR76 3000 6000 0112 3456 7890 189"

CUSTOMERS = [
    {"name": "Plastex GmbH", "addr": "Industriestraße 44\n80339 München, Germany", "vat": "DE 123 456 789"},
    {"name": "Solvalor S.A.S.", "addr": "Zone Industrielle Nord, Bât. C\n76700 Harfleur, France", "vat": "FR 91 423 187 002"},
    {"name": "Nordic Resins AB", "addr": "Fabriksvägen 12\n151 36 Södertälje, Sweden", "vat": "SE556012345601"},
    {"name": "Iberchem S.L.", "addr": "Polígono Industrial El Granadal\n41006 Sevilla, Spain", "vat": "ES B41234567"},
    {"name": "Deltasolv NV", "addr": "Havenstraat 78\n2000 Antwerpen, Belgium", "vat": "BE 0897 654 321"},
]

PRODUCTS = [
    ("Technical acetone 99.5%", "AK-995", "L", 0.89),
    ("Distilled toluene", "TL-DIS", "L", 1.42),
    ("Denatured ethanol 96%", "ET-96D", "L", 0.67),
    ("Hydrochloric acid 33%", "HCL-33", "kg", 0.54),
    ("Sodium hydroxide pearls", "NaOH-P", "kg", 0.72),
    ("Pure methanol", "ME-PUR", "L", 1.15),
    ("Isopropanol 99%", "IPA-99", "L", 1.38),
    ("Sulfuric acid 96%", "H2SO4-96", "kg", 0.61),
    ("Dichloromethane", "DCM-TEC", "L", 2.14),
    ("Ethyl acetate 99%", "EA-99", "L", 1.76),
    ("Food-grade sodium chloride", "NaCl-A", "kg", 0.28),
    ("Hydrogen peroxide 30%", "H2O2-30", "kg", 1.92),
    ("Ammonia solution 25%", "NH3-25", "L", 0.83),
    ("Glycerol 99.5% USP", "GLY-USP", "kg", 2.35),
    ("Nitric acid 65%", "HNO3-65", "kg", 0.98),
    ("Mixed xylenes", "XYL-MIX", "L", 1.54),
    ("Propylene glycol USP", "PG-USP", "kg", 1.87),
    ("Triethylamine 99%", "TEA-99", "kg", 4.22),
]

INVOICES = [
    {"num": "FC-2024-00187", "date": "2024-01-15", "due": "2024-02-14", "customer": 0,
     "lines": [(0,500,"L"),(1,200,"L"),(4,300,"kg"),(6,150,"L")], "transport": 145.00, "note": "Carriage paid delivery. Storage temperature: below 25°C. Products classified ADR class 3."},
    {"num": "FC-2024-00241", "date": "2024-02-03", "due": "2024-03-05", "customer": 1,
     "lines": [(2,800,"L"),(5,400,"L"),(9,250,"L"),(11,100,"kg")], "transport": 220.00, "note": "Shipped by an approved dangerous goods carrier. Safety data sheets supplied."},
    {"num": "FC-2024-00318", "date": "2024-02-28", "due": "2024-03-29", "customer": 2,
     "lines": [(3,600,"kg"),(7,400,"kg"),(14,200,"kg"),(15,350,"L")], "transport": 310.00, "note": "EXW Villeurbanne, Incoterms 2020. Payment within 30 days of invoice date."},
    {"num": "FC-2024-00402", "date": "2024-03-18", "due": "2024-04-17", "customer": 3,
     "lines": [(0,1000,"L"),(1,500,"L"),(4,200,"kg"),(10,800,"kg"),(12,300,"L")], "transport": 185.00, "note": "3% volume discount applied. Certificates of analysis enclosed with the shipment."},
    {"num": "FC-2024-00489", "date": "2024-04-05", "due": "2024-05-05", "customer": 4,
     "lines": [(5,300,"L"),(8,150,"L"),(16,500,"kg"),(17,80,"kg")], "transport": 275.00, "note": "Products stored under nitrogen. Shelf life 12 months from the date of manufacture."},
    {"num": "FC-2024-00563", "date": "2024-04-22", "due": "2024-05-22", "customer": 0,
     "lines": [(2,600,"L"),(6,400,"L"),(9,300,"L"),(11,200,"kg"),(13,150,"kg")], "transport": 195.00, "note": "Credit note FC-2023-00891 for €230 deducted. 1000 L IBC packaging. Packaging deposit: €85 per IBC."},
    {"num": "FC-2024-00641", "date": "2024-05-10", "due": "2024-06-09", "customer": 1,
     "lines": [(0,250,"L"),(3,400,"kg"),(7,300,"kg"),(15,200,"L")], "transport": 165.00, "note": "Refrigerated container transport. Temperature maintained between 5°C and 15°C throughout transit."},
    {"num": "FC-2024-00728", "date": "2024-06-01", "due": "2024-07-01", "customer": 2,
     "lines": [(1,700,"L"),(4,500,"kg"),(8,200,"L"),(16,400,"kg"),(17,120,"kg")], "transport": 340.00, "note": "Framework contract 2024 — call-off No. 7/12. Prices fixed until 2024-12-31. Review in January 2025."},
]

def styles():
    s = getSampleStyleSheet()
    title = ParagraphStyle('title', fontSize=20, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a3a5c'), spaceAfter=4)
    h2 = ParagraphStyle('h2', fontSize=11, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a3a5c'), spaceBefore=12, spaceAfter=4)
    normal = ParagraphStyle('normal', fontSize=9, fontName='Helvetica', leading=13)
    small = ParagraphStyle('small', fontSize=8, fontName='Helvetica', textColor=colors.grey, leading=11)
    right = ParagraphStyle('right', fontSize=9, fontName='Helvetica', alignment=TA_RIGHT)
    return title, h2, normal, small, right

def header_table(inv, cust):
    title, h2, normal, small, right = styles()
    left = [
        Paragraph(COMPANY, ParagraphStyle('co', fontSize=13, fontName='Helvetica-Bold', textColor=colors.HexColor('#1a3a5c'))),
        Paragraph(ADDR, small),
        Paragraph(f"VAT: {VAT}", small),
        Spacer(1, 0.3*cm),
        Paragraph(f"<b>INVOICE No. {inv['num']}</b>", ParagraphStyle('inv', fontSize=11, fontName='Helvetica-Bold')),
        Paragraph(f"Date: {inv['date']}", normal),
        Paragraph(f"Due date: {inv['due']}", normal),
    ]
    right_col = [
        Paragraph("<b>Bill to:</b>", h2),
        Paragraph(f"<b>{cust['name']}</b>", ParagraphStyle('cn', fontSize=10, fontName='Helvetica-Bold')),
        Paragraph(cust['addr'].replace('\n','<br/>'), normal),
        Paragraph(f"EU VAT number: {cust['vat']}", small),
    ]
    t = Table([[left, right_col]], colWidths=[9*cm, 9*cm])
    t.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'TOP'), ('LEFTPADDING', (0,0), (-1,-1), 0), ('RIGHTPADDING', (0,0), (-1,-1), 0)]))
    return t

def lines_table(inv):
    header = ['Ref.', 'Description', 'Qty', 'Unit', 'Unit price excl. VAT (€)', 'Amount excl. VAT (€)']
    rows = [header]
    subtotal = 0
    for (pi, qty, _unit) in inv['lines']:
        p = PRODUCTS[pi]
        ref, name, unit, pu = p[1], p[0], p[2], p[3]
        total = round(qty * pu, 2)
        subtotal += total
        rows.append([ref, name, f"{qty:,}", unit, f"{pu:,.2f}", f"{total:,.2f}"])
    # transport
    rows.append(['', 'Freight and handling charges', '', '', '', f"{inv['transport']:,.2f}"])
    subtotal += inv['transport']
    tva = round(subtotal * 0.20, 2)
    ttc = round(subtotal + tva, 2)
    rows.append(['', '', '', '', 'Subtotal excl. VAT', f"{subtotal:,.2f}"])
    rows.append(['', '', '', '', 'VAT 20%', f"{tva:,.2f}"])
    rows.append(['', '', '', '', '<b>TOTAL incl. VAT</b>', f"<b>{ttc:,.2f}</b>"])

    col_w = [2*cm, 6.1*cm, 1.4*cm, 1.5*cm, 3*cm, 3*cm]
    # wrap header and totals in Paragraphs so long English labels wrap
    rows[0] = [Paragraph(f"<b>{c}</b>", ParagraphStyle('hc', fontSize=8.5, fontName='Helvetica-Bold', textColor=colors.white, alignment=TA_RIGHT if i >= 2 else TA_LEFT, leading=10)) for i, c in enumerate(header)]
    for i in range(len(rows)-3, len(rows)):
        rows[i][4] = Paragraph(rows[i][4], ParagraphStyle('rc', fontSize=9, alignment=TA_RIGHT))
        rows[i][5] = Paragraph(rows[i][5], ParagraphStyle('rc', fontSize=9, alignment=TA_RIGHT))

    t = Table(rows, colWidths=col_w, repeatRows=1)
    n = len(rows)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a3a5c')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1, n-4), 0.4, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1, n-4), [colors.white, colors.HexColor('#f5f8fb')]),
        ('LINEABOVE', (4, n-3), (-1, n-3), 0.8, colors.HexColor('#1a3a5c')),
        ('FONTNAME', (4, n-1), (-1, n-1), 'Helvetica-Bold'),
        ('BACKGROUND', (4, n-1), (-1, n-1), colors.HexColor('#e8f0f8')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    return t, ttc

def payment_table(ttc, iban):
    _, h2, normal, small, _ = styles()
    rows = [
        ['Payment method:', 'SEPA bank transfer'],
        ['IBAN:', iban],
        ['BIC:', 'BNPAFRPPXXX'],
        ['Payment reference:', f"FC-{ttc:.0f}-REF"],
        ['Amount due:', f"€{ttc:,.2f}"],
    ]
    t = Table(rows, colWidths=[4.5*cm, 13*cm])
    t.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f5f8fb')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.lightgrey),
    ]))
    return t

def legal_page(styles_fn):
    title, h2, normal, small, right = styles_fn()
    story = []
    story.append(Paragraph("General Terms and Conditions of Sale — Extract", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 0.3*cm))
    cgv = [
        ("Art. 1 — Purpose", "These general terms and conditions of sale apply to all sales of chemical products made by ChemCorp Industries S.A. (hereinafter \"the Seller\") to its business customers. Placing an order implies full and unreserved acceptance of these terms. The customer's own purchasing conditions may not prevail over these terms except with the Seller's express written agreement."),
        ("Art. 2 — Prices", "Prices are stated in euros excluding VAT, according to the tariff in force on the day the order is placed. They may be revised without notice. Freight, packaging and insurance costs are invoiced in addition unless otherwise stipulated. The applicable VAT rate is the one in force at the invoice date."),
        ("Art. 3 — Payment", "Unless specific terms have been granted in writing, payment falls due 30 days from the invoice date. Any late payment automatically incurs late-payment interest at three times the statutory rate, together with a fixed recovery indemnity of €40. The Seller reserves the right to suspend deliveries in progress if the credit limit is exceeded."),
        ("Art. 4 — Delivery", "Delivery lead times are given for guidance only. No delay may give rise to a penalty, damages or cancellation of the order. Risk passes to the buyer as soon as the goods are handed over to the carrier (Incoterms 2020 — EXW unless otherwise agreed). It is the consignee's responsibility to check the condition of the goods on receipt and to raise any reservation within 3 working days."),
        ("Art. 5 — Conformity and claims", "Delivered products conform to the specifications stated in the purchase order and the product data sheets. Any claim regarding conformity must be submitted in writing within 8 days of receipt. After that period no claim will be admissible. The Seller's liability is limited to the amount of the invoice concerned."),
        ("Art. 6 — Dangerous goods regulations", "Chemical products are classified, packaged and labelled in accordance with the CLP Regulation (EC) No 1272/2008. Safety data sheets (SDS) compliant with the REACH Regulation are available on request or from the customer portal. The buyer is responsible for using the products in compliance with the local regulations in force, in particular those covering safety, hygiene and the environment."),
        ("Art. 7 — Retention of title", "The Seller retains ownership of the delivered goods until the price has been paid in full, including principal and incidental charges. In the event of non-payment, the Seller may demand the return of the goods. This clause does not prevent risk from passing on delivery in accordance with Article 4."),
        ("Art. 8 — Returns", "No goods will be accepted for return without the Seller's prior written agreement. Returned products must be in their original unopened packaging and accompanied by the return note. Custom-made or specially manufactured products may not be returned. Return costs are borne by the customer unless the return results from an error by the Seller."),
        ("Art. 9 — Governing law and jurisdiction", "These terms are governed by French law. Any dispute concerning their interpretation or performance falls within the exclusive jurisdiction of the Lyon Commercial Court, even in the event of a warranty claim or multiple defendants."),
    ]
    for title_t, body in cgv:
        story.append(Paragraph(f"<b>{title_t}</b>", ParagraphStyle('cgvt', fontSize=9, fontName='Helvetica-Bold', spaceBefore=8)))
        story.append(Paragraph(body, ParagraphStyle('cgvb', fontSize=8.5, fontName='Helvetica', leading=12, textColor=colors.HexColor('#333333'))))
    return story

def build_invoice(inv, out_dir):
    title, h2, normal, small, right = styles()
    cust = CUSTOMERS[inv['customer']]
    path = os.path.join(out_dir, f"{inv['num']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # Page 1 — header
    story.append(header_table(inv, cust))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 0.4*cm))

    # Lines
    story.append(Paragraph("Order details", h2))
    lt, ttc = lines_table(inv)
    story.append(lt)
    story.append(Spacer(1, 0.6*cm))

    # Note
    story.append(Paragraph(f"<i>Note: {inv['note']}</i>", small))
    story.append(Spacer(1, 0.5*cm))

    # Payment
    story.append(Paragraph("Payment information", h2))
    story.append(payment_table(ttc, IBAN))
    story.append(Spacer(1, 0.5*cm))

    # Certif
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("Certifications &amp; Quality", h2))
    story.append(Paragraph("ChemCorp Industries is certified to ISO 9001:2015 and ISO 14001:2015. Our products undergo systematic quality control. Certificates of analysis are available on request (ref. COA). REACH, RoHS and CLP compliance guaranteed.", small))
    story.append(Spacer(1, 0.5*cm))

    # Traceability table
    story.append(Paragraph("Delivered batch traceability", h2))
    trace_rows = [['Product ref.', 'Batch No.', 'Mfg date', 'Exp. date', 'QC check', 'Analyst']]
    lots = ['LOT-241001', 'LOT-241078', 'LOT-241132', 'LOT-241200', 'LOT-241289']
    dates_fab = ['2024-10-01', '2024-10-12', '2024-10-22', '2024-11-03', '2024-11-15']
    dates_exp = ['2025-10-01', '2025-10-12', '2025-10-22', '2025-11-03', '2025-11-15']
    analysts = ['J. Dupont', 'S. Leroy', 'J. Dupont', 'A. Martin', 'S. Leroy']
    for i, (pi, qty, _) in enumerate(inv['lines']):
        p = PRODUCTS[pi]
        trace_rows.append([p[1], lots[i % len(lots)], dates_fab[i % len(dates_fab)], dates_exp[i % len(dates_exp)], 'PASS', analysts[i % len(analysts)]])
    tt = Table(trace_rows, colWidths=[2.5*cm, 2.5*cm, 2*cm, 2*cm, 2.5*cm, 2.5*cm], repeatRows=1)
    tt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d6a9f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#eef4fa')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tt)

    # Page 2 — terms
    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    story.append(Paragraph(f"Invoice No. {inv['num']} — Regulatory annex and terms", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 0.3*cm))

    # ADR table
    story.append(Paragraph("Dangerous goods transport classification (ADR 2023)", h2))
    adr_rows = [['Product', 'UN No.', 'ADR class', 'Packing group', 'Tunnel code', 'Max qty per package']]
    adr_data = [
        ('Acetone', 'UN 1090', '3', 'II', 'D/E', '450 L'),
        ('Toluene', 'UN 1294', '3', 'II', 'D/E', '450 L'),
        ('Methanol', 'UN 1230', '3+6.1', 'II', 'D/E', '450 L'),
        ('Hydrochloric acid', 'UN 1789', '8', 'II', 'E', '30 L'),
        ('Sulfuric acid', 'UN 1830', '8', 'II', 'E', '30 L'),
    ]
    adr_rows += adr_data
    tadr = Table(adr_rows, colWidths=[3.5*cm, 2*cm, 2*cm, 2.5*cm, 2*cm, 3*cm], repeatRows=1)
    tadr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#fdf2f2')]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(tadr)
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("⚠ Transport entrusted to an ADR-approved carrier. The loader is responsible for the loading declaration. ADR documents available on request.", ParagraphStyle('warn', fontSize=8, textColor=colors.HexColor('#c0392b'))))
    story.append(Spacer(1, 0.5*cm))

    story += legal_page(styles)

    # Page 3 — detailed specs
    from reportlab.platypus import PageBreak
    story.append(PageBreak())
    story.append(Paragraph("Technical specifications of delivered products", h2))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#1a3a5c')))
    story.append(Spacer(1, 0.3*cm))

    specs = [
        ('Technical acetone 99.5%', [
            ('Purity (GC)', '≥ 99.5%', '99.72%'),
            ('Water (KF)', '≤ 0.2%', '0.08%'),
            ('Acidity (as acetic acid)', '≤ 0.002%', '< 0.001%'),
            ('Evaporation residue', '≤ 0.001%', '< 0.001%'),
            ('Density at 20°C', '0.789–0.792 g/mL', '0.790 g/mL'),
            ('Refractive index', '1.356–1.360', '1.3588'),
        ]),
        ('Distilled toluene', [
            ('Purity (GC)', '≥ 99.5%', '99.68%'),
            ('Benzene', '≤ 1 ppm', '< 0.5 ppm'),
            ('Water', '≤ 0.02%', '0.009%'),
            ('Density at 20°C', '0.864–0.867 g/mL', '0.865 g/mL'),
        ]),
        ('Sodium hydroxide pearls', [
            ('Purity (NaOH)', '≥ 99.0%', '99.4%'),
            ('Na₂CO₃', '≤ 0.5%', '0.2%'),
            ('NaCl', '≤ 0.02%', '< 0.01%'),
            ('Fe', '≤ 5 ppm', '2 ppm'),
        ]),
    ]

    for prod_name, spec_rows in specs:
        story.append(Paragraph(f"<b>{prod_name}</b>", ParagraphStyle('specn', fontSize=10, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4, textColor=colors.HexColor('#1a3a5c'))))
        spec_table_rows = [['Parameter', 'Specification', 'COA result']] + spec_rows
        ts = Table(spec_table_rows, colWidths=[6*cm, 5*cm, 6*cm])
        ts.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d6a9f')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
            ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#eef4fa')]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(ts)
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("Declaration of conformity", h2))
    story.append(Paragraph(
        f"ChemCorp Industries S.A. declares that the products delivered under invoice {inv['num']} "
        "conform to the specifications above, to the REACH Regulation (EC No 1907/2006), "
        "the CLP Regulation (EC No 1272/2008), and to the ISO 9001:2015 quality requirements. "
        "Analytical results are issued by our in-house laboratory, COFRAC-accredited under No. 1-5421.",
        ParagraphStyle('decl', fontSize=9, fontName='Helvetica', leading=13, textColor=colors.HexColor('#333333'))
    ))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'data', 'invoices')
    os.makedirs(out, exist_ok=True)
    for inv in INVOICES:
        build_invoice(inv, out)
    print(f"Done — {len(INVOICES)} invoices generated.")
