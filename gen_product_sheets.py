#!/usr/bin/env python3
"""Generate mock product data sheets for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import os

COMPANY = "ChemCorp Industries S.A."

def s(name='normal', size=9, bold=False, color='#000000', leading=13, align='LEFT', space_before=0, space_after=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}[align]
    return ParagraphStyle(name, fontSize=size, fontName='Helvetica-Bold' if bold else 'Helvetica',
                          textColor=colors.HexColor(color), leading=leading, alignment=al,
                          spaceBefore=space_before*cm, spaceAfter=space_after*cm)

BLUE = '#1a3a5c'
LBLUE = '#2d6a9f'
PALE = '#eef4fa'
RED = '#c0392b'

PRODUCTS = [
    {
        "ref": "FT-AK995-2024",
        "name": "Technical Acetone 99.5%",
        "cas": "67-64-1",
        "ec": "200-662-2",
        "formula": "C3H6O — (CH3)2CO",
        "mw": "58.08 g/mol",
        "family": "Aliphatic ketone",
        "grade": "Technical",
        "packaging": ["25 L can (HDPE)", "200 L drum (stainless steel)", "1000 L IBC"],
        "physical": [
            ("Physical state", "Colourless liquid"),
            ("Odour", "Characteristic, fruity"),
            ("Boiling point", "56.0 °C (1013 hPa)"),
            ("Flash point", "-18 °C (closed cup)"),
            ("Density at 20°C", "0.790 g/mL"),
            ("Vapour pressure at 20°C", "233 hPa"),
            ("Viscosity at 20°C", "0.32 mPa·s"),
            ("Solubility in water", "Miscible in all proportions"),
            ("Refractive index nD20", "1.3588"),
            ("Auto-ignition temperature", "465 °C"),
            ("Explosive limits (LEL/UEL)", "2.5% / 13.0% vol."),
        ],
        "specs": [
            ("Purity (GC)", ">= 99.5%"),
            ("Water (Karl Fischer)", "<= 0.20%"),
            ("Acidity (as acetic acid)", "<= 0.002%"),
            ("Evaporation residue", "<= 0.001%"),
            ("Colour (Hazen/APHA)", "<= 10"),
            ("Methanol", "<= 0.05%"),
            ("Isopropanol", "<= 0.05%"),
        ],
        "uses": [
            "Solvent for organic synthesis (esterification, aldol condensation)",
            "Degreasing and cleaning of metal and plastic surfaces",
            "Thinner for resins, paints and varnishes",
            "Liquid-liquid extraction in pharmaceutical and food chemistry",
            "Polymer manufacture (PMMA, polycarbonate)",
            "Degreasing in electronics (printed circuit board cleaning)",
        ],
        "hazards": [
            ("H225", "Highly flammable liquid and vapour"),
            ("H319", "Causes serious eye irritation"),
            ("H336", "May cause drowsiness or dizziness"),
        ],
        "precautions": [
            ("P210", "Keep away from heat, sparks and open flames"),
            ("P233", "Keep container tightly closed"),
            ("P261", "Avoid breathing vapours"),
            ("P305+P351+P338", "IF IN EYES: rinse cautiously with water"),
            ("P370+P378", "In case of fire: use CO2 or all-purpose foam"),
        ],
        "storage": "Store in a cool, well-ventilated area away from sources of ignition. Recommended storage temperature: 5–25°C. Keep away from strong oxidisers, acids and concentrated bases. Shelf life: 36 months in the unopened original packaging.",
        "transport": "UN 1090 | ADR class 3 | Packing group II | Tunnel code D/E",
        "certif": "ISO 9001:2015 | Analysed by COFRAC No. 1-5421 | REACH SVHC: not concerned",
    },
    {
        "ref": "FT-NaOHP-2024",
        "name": "Sodium Hydroxide Pearls 99%",
        "cas": "1310-73-2",
        "ec": "215-185-5",
        "formula": "NaOH",
        "mw": "40.00 g/mol",
        "family": "Strong inorganic base",
        "grade": "Technical / Industrial",
        "packaging": ["25 kg bag (PE)", "500 kg big bag", "1000 kg big bag"],
        "physical": [
            ("Physical state", "Solid (white pearls)"),
            ("Odour", "Odourless"),
            ("Melting point", "318 °C"),
            ("Boiling point", "1388 °C"),
            ("Bulk density", "0.88–1.00 g/cm³"),
            ("True density at 20°C", "2.13 g/cm³"),
            ("Solubility in water at 20°C", "111 g/100 mL (exothermic solution)"),
            ("pH (1% solution)", "13.0"),
            ("Hygroscopicity", "Very hygroscopic"),
            ("Flash point", "Not applicable (solid)"),
        ],
        "specs": [
            ("Purity (NaOH)", ">= 99.0%"),
            ("Na2CO3", "<= 0.50%"),
            ("NaCl", "<= 0.02%"),
            ("Na2SO4", "<= 0.01%"),
            ("Iron (Fe)", "<= 5 ppm"),
            ("Aluminium (Al)", "<= 10 ppm"),
            ("Silicon (Si)", "<= 10 ppm"),
            ("Water-insoluble matter", "<= 0.02%"),
        ],
        "uses": [
            "Neutralisation of acidic effluent in water treatment",
            "Manufacture of soaps and detergents (saponification)",
            "Metal surface treatment (pickling, alkaline degreasing)",
            "Paper industry (Kraft process, bleaching)",
            "Chemical synthesis (hydrolysis, epoxidation reactions)",
            "pH regulation in food processes (food grades on request)",
        ],
        "hazards": [
            ("H290", "May be corrosive to metals"),
            ("H314", "Causes severe skin burns and eye damage"),
        ],
        "precautions": [
            ("P234", "Keep only in the original packaging"),
            ("P260", "Do not breathe dust"),
            ("P280", "Wear protective gloves/clothing/eye protection/face protection"),
            ("P301+P330+P331", "IF SWALLOWED: rinse mouth — do NOT induce vomiting"),
            ("P305+P351+P338", "IF IN EYES: rinse with water for 15 minutes"),
            ("P405", "Store locked up"),
        ],
        "storage": "Store in tightly closed containers in a dry place. Protect from moisture and atmospheric CO2. Keep away from acids and metals (aluminium, zinc, tin). Shelf life: 24 months in closed packaging.",
        "transport": "UN 1823 | ADR class 8 | Packing group II | Tunnel code E",
        "certif": "ISO 9001:2015 | ISO 14001:2015 | Tested per EN ISO 8655",
    },
    {
        "ref": "FT-H2SO496-2024",
        "name": "Sulfuric Acid 96% — Technical Grade",
        "cas": "7664-93-9",
        "ec": "231-639-5",
        "formula": "H2SO4",
        "mw": "98.08 g/mol",
        "family": "Strong mineral acid",
        "grade": "Technical",
        "packaging": ["25 L jerrican (HDPE)", "200 L drum (HDPE)", "1000 L tank (HDPE IBC)"],
        "physical": [
            ("Physical state", "Oily liquid, colourless to slightly yellowish"),
            ("Odour", "Slightly acrid at high concentration"),
            ("Boiling point", "330 °C (with decomposition)"),
            ("Freezing point", "3 °C (H2SO4 96%)"),
            ("Density at 20°C", "1.835 g/mL"),
            ("Viscosity at 20°C", "21.4 mPa·s"),
            ("pH (1% dilute solution)", "< 1"),
            ("Miscibility with water", "Miscible (strongly exothermic)"),
            ("Vapour pressure at 20°C", "< 0.1 hPa"),
            ("Flash point", "Not applicable"),
        ],
        "specs": [
            ("H2SO4 content", "95.0–97.0%"),
            ("Ignition residue", "<= 0.005%"),
            ("Iron (Fe)", "<= 5 ppm"),
            ("Chlorides (Cl-)", "<= 2 ppm"),
            ("Arsenic (As)", "<= 0.05 ppm"),
            ("Lead (Pb)", "<= 0.1 ppm"),
            ("Nitrates (NO3-)", "<= 5 ppm"),
            ("Reducing agents (SO2)", "<= 5 ppm"),
        ],
        "uses": [
            "Pickling and surface treatment of metals (steel, copper, aluminium)",
            "Electrolyte in lead-acid batteries",
            "Synthesis of metal sulfates and alums",
            "Water treatment (pH correction)",
            "Textile industry (acid bath for dyeing)",
            "Regeneration of ion-exchange resins",
        ],
        "hazards": [
            ("H290", "May be corrosive to metals"),
            ("H314", "Causes severe skin burns and eye damage"),
            ("H335", "May cause respiratory irritation"),
        ],
        "precautions": [
            ("P234", "Keep only in the original HDPE or glass packaging"),
            ("P260", "Do not breathe vapours or aerosols"),
            ("P280", "Wear full personal protective equipment"),
            ("P301+P330+P331", "IF SWALLOWED: rinse mouth. Do NOT induce vomiting"),
            ("P303+P361+P353", "IF ON SKIN: rinse immediately with plenty of water"),
            ("P405+P501", "Store locked up. Dispose of in accordance with local regulations"),
        ],
        "storage": "Store in a ventilated, acid-resistant area away from organic matter, combustibles, bases and oxidisers. Never add water to sulfuric acid (risk of violent splashing). Storage temperature: 5–35°C. Unlimited shelf life in closed packaging.",
        "transport": "UN 1830 | ADR class 8 | Packing group II | Tunnel code E",
        "certif": "ISO 9001:2015 | Compliant with Directive 2008/98/EC",
    },
    {
        "ref": "FT-PG-USP-2024",
        "name": "Propylene Glycol — USP/Food Grade",
        "cas": "57-55-6",
        "ec": "200-338-0",
        "formula": "C3H8O2 — CH3CH(OH)CH2OH",
        "mw": "76.09 g/mol",
        "family": "Aliphatic diol",
        "grade": "USP / Food grade E1520",
        "packaging": ["25 L can (HDPE)", "200 L drum (HDPE)", "1000 L IBC (HDPE)"],
        "physical": [
            ("Physical state", "Colourless viscous liquid"),
            ("Odour", "Practically odourless, slightly sweet"),
            ("Boiling point", "188.2 °C"),
            ("Flash point", "99 °C (closed cup)"),
            ("Freezing point", "-59 °C"),
            ("Density at 20°C", "1.036 g/mL"),
            ("Viscosity at 20°C", "56 mPa·s"),
            ("Solubility in water", "Miscible in all proportions"),
            ("Hygroscopicity", "Hygroscopic"),
            ("Refractive index nD20", "1.4326"),
        ],
        "specs": [
            ("Purity (GC)", ">= 99.5%"),
            ("Water", "<= 0.20%"),
            ("Density at 20°C", "1.035–1.037 g/mL"),
            ("Refractive index", "1.4320–1.4330"),
            ("Acidity (as lactic acid)", "<= 0.007%"),
            ("Arsenic (As)", "<= 1.5 ppm"),
            ("Lead (Pb)", "<= 5 ppm"),
            ("Chlorides (Cl-)", "<= 10 ppm"),
            ("Ethylene glycol", "<= 0.06%"),
            ("Diethylene glycol", "<= 0.10%"),
        ],
        "uses": [
            "Pharmaceutical solvent (excipient in syrups and injectables)",
            "Humectant in cosmetics and personal care",
            "Food additive (humectant E1520 — bread, cakes, colourings)",
            "Non-toxic heat transfer fluid (food-industry chillers)",
            "Carrier for flavours and fragrances in e-liquids",
            "Non-corrosive antifreeze in food-grade HVAC systems",
        ],
        "hazards": [],
        "precautions": [
            ("P260", "Avoid breathing vapours at high temperature"),
            ("P273", "Avoid release to the environment"),
        ],
        "storage": "Store under ambient conditions (5–30°C), away from direct light and moisture. Keep in tightly closed containers. Compatible with most materials. Shelf life: 24 months. Check regularly for the absence of microbial contamination.",
        "transport": "Not subject to ADR regulations in packages of 1000 L or less",
        "certif": "USP/NF, BP/EP, FCC, E1520 | Halal &amp; Kosher on request | ISO 22000 | FSSC 22000",
    },
    {
        "ref": "FT-HCL33-2024",
        "name": "Hydrochloric Acid 33% — Aqueous Solution",
        "cas": "7647-01-0",
        "ec": "231-595-7",
        "formula": "HCl (aq.) — 33% w/w",
        "mw": "36.46 g/mol (pure HCl)",
        "family": "Strong mineral acid",
        "grade": "Technical",
        "packaging": ["25 L jerrican (HDPE)", "200 L drum (HDPE)", "1000 L IBC (HDPE)"],
        "physical": [
            ("Physical state", "Colourless to pale yellow liquid"),
            ("Odour", "Pungent, acrid (HCl fumes)"),
            ("Boiling point (azeotrope)", "108.6 °C at 20.2% HCl"),
            ("Freezing point", "-36 °C (HCl 33%)"),
            ("Density at 20°C", "1.155–1.165 g/mL"),
            ("Viscosity at 20°C", "1.9 mPa·s"),
            ("HCl vapour pressure at 20°C", "~16 hPa"),
            ("pH (undiluted)", "< 0"),
            ("Electrical conductivity", "High (strong electrolyte)"),
        ],
        "specs": [
            ("HCl content", "32.0–34.0%"),
            ("Density at 20°C", "1.155–1.165 g/mL"),
            ("Evaporation residue", "<= 0.01%"),
            ("Sulfates (SO4²-)", "<= 5 ppm"),
            ("Iron (Fe)", "<= 3 ppm"),
            ("Arsenic (As)", "<= 0.1 ppm"),
            ("Heavy metals (Pb)", "<= 1 ppm"),
            ("Colour (APHA)", "<= 20"),
        ],
        "uses": [
            "Acid pickling of steel before galvanising or welding",
            "Regeneration of cationic ion-exchange resins",
            "Synthesis of metal chlorides (FeCl2, ZnCl2, AlCl3)",
            "pH adjustment in water treatment",
            "Gelatine extraction and protein hydrolysis",
            "Cleaning of tanks and pipework in the food industry",
        ],
        "hazards": [
            ("H290", "May be corrosive to metals"),
            ("H314", "Causes severe skin burns and eye damage"),
            ("H335", "May cause respiratory irritation"),
        ],
        "precautions": [
            ("P260", "Do not breathe vapours"),
            ("P271", "Use only outdoors or in a well-ventilated area"),
            ("P280", "Acid-resistant gloves, eye and face protection"),
            ("P301+P330+P331", "IF SWALLOWED: rinse mouth. Do NOT induce vomiting"),
            ("P304+P340", "IF INHALED: move the person to fresh air"),
        ],
        "storage": "Store in acid-resistant HDPE or glass containers in a ventilated area away from bases, oxidisers and metals. Storage temperature: 0–30°C. Shelf life: 24 months (risk of off-gassing at elevated temperature).",
        "transport": "UN 1789 | ADR class 8 | Packing group II | Tunnel code E",
        "certif": "ISO 9001:2015 | Compliant with IED Directive 2010/75/EU",
    },
]

def build_sheet(prod, out_dir):
    path = os.path.join(out_dir, f"{prod['ref']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm)
    story = []

    # Title block
    title_t = Table([[
        Paragraph(f"<b>{prod['name']}</b>", s('pt', 16, bold=True, color='#ffffff', leading=19)),
        Paragraph(f"<b>PRODUCT DATA SHEET</b><br/>{prod['ref']}", s('pr', 10, bold=True, color='#ffffff', align='RIGHT', leading=13)),
    ]], colWidths=[12*cm, 5*cm])
    title_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (0,-1), 12), ('RIGHTPADDING', (1,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(title_t)
    story.append(Spacer(1, 0.4*cm))

    # Identity
    id_rows = [
        ['CAS No.', prod['cas'], 'EC No.', prod['ec']],
        ['Formula', prod['formula'], 'Molar mass', prod['mw']],
        ['Chemical family', prod['family'], 'Grade', prod['grade']],
    ]
    id_t = Table(id_rows, colWidths=[3.5*cm, 5*cm, 3.5*cm, 5*cm])
    id_t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'), ('FONTNAME', (2,0), (2,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PALE)), ('BACKGROUND', (2,0), (2,-1), colors.HexColor(PALE)),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(Paragraph("1. PRODUCT IDENTIFICATION", s('h', 10, bold=True, color=BLUE, space_before=0.1)))
    story.append(id_t)
    story.append(Spacer(1, 0.2*cm))

    # Packaging
    pkg_str = " | ".join(prod['packaging'])
    story.append(Paragraph(f"<b>Available pack sizes:</b> {pkg_str}", s('pkg', 9)))
    story.append(Spacer(1, 0.4*cm))

    # Physical properties
    story.append(Paragraph("2. PHYSICO-CHEMICAL PROPERTIES", s('h2', 10, bold=True, color=BLUE)))
    phys_rows = [['Property', 'Value']] + list(prod['physical'])
    pt = Table(phys_rows, colWidths=[7*cm, 10*cm], repeatRows=1)
    pt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(pt)
    story.append(Spacer(1, 0.4*cm))

    # Specifications
    story.append(Paragraph("3. ANALYTICAL SPECIFICATIONS", s('h3', 10, bold=True, color=BLUE)))
    spec_rows = [['Parameter', 'Specification']] + list(prod['specs'])
    st = Table(spec_rows, colWidths=[8*cm, 9*cm], repeatRows=1)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(st)

    # Page 2
    story.append(PageBreak())
    story.append(Paragraph(f"{prod['name']} — Page 2/3", s('pg', 8, color='#666666', align='RIGHT')))
    story.append(Spacer(1, 0.2*cm))

    # Uses
    story.append(Paragraph("4. APPLICATIONS AND USES", s('h4', 10, bold=True, color=BLUE)))
    for use in prod['uses']:
        story.append(Paragraph(f"• {use}", s('u', 9, leading=14, space_before=0)))
    story.append(Spacer(1, 0.4*cm))

    # Hazards
    if prod['hazards']:
        story.append(Paragraph("5. HAZARD INFORMATION (CLP/GHS)", s('h5', 10, bold=True, color=BLUE)))
        hz_rows = [['Code', 'Hazard statement']] + [[h, m] for h, m in prod['hazards']]
        ht = Table(hz_rows, colWidths=[2.5*cm, 14.5*cm])
        ht.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(RED)),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fdf2f2'), colors.white]),
            ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(ht)
        story.append(Spacer(1, 0.3*cm))
    else:
        story.append(Paragraph("5. HAZARD INFORMATION", s('h5', 10, bold=True, color=BLUE)))
        story.append(Paragraph("This product is not classified as hazardous under the CLP Regulation (EC) No 1272/2008.", s('nd', 9, color='#2e7d32')))
        story.append(Spacer(1, 0.3*cm))

    # Precautions
    story.append(Paragraph("6. PRECAUTIONARY STATEMENTS", s('h6', 10, bold=True, color=BLUE)))
    pc_rows = [['Code', 'Precautionary statement']] + [[p, m] for p, m in prod['precautions']]
    pct = Table(pc_rows, colWidths=[3.5*cm, 13.5*cm])
    pct.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e67e22')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fef9f0'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(pct)
    story.append(Spacer(1, 0.4*cm))

    # Storage
    story.append(Paragraph("7. STORAGE AND SHELF LIFE", s('h7', 10, bold=True, color=BLUE)))
    story.append(Paragraph(prod['storage'], s('stor', 9, leading=13)))
    story.append(Spacer(1, 0.4*cm))

    # Transport
    story.append(Paragraph("8. TRANSPORT AND REGULATIONS", s('h8', 10, bold=True, color=BLUE)))
    story.append(Paragraph(prod['transport'], s('trans', 9, leading=13)))
    story.append(Spacer(1, 0.4*cm))

    # Page 3 — extended application notes
    story.append(PageBreak())
    story.append(Paragraph(f"{prod['name']} — Page 3/3", s('pg3', 8, color='#666666', align='RIGHT')))
    story.append(Spacer(1, 0.2*cm))
    story.append(Paragraph("9. DETAILED APPLICATION NOTES", s('h9', 10, bold=True, color=BLUE)))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    # Generic extended content for all products
    app_notes = [
        ("Material compatibility",
         "Before use at scale, check compatibility with seals, pipework and containers. "
         "Give preference to materials tested and validated by ChemCorp Industries. Refer to the chemical "
         "compatibility tables available on our technical portal (portail.chemcorp.fr/compat). If in doubt, contact "
         "our Technical Application service on +33 4 72 XX XX XX."),
        ("Quality control on receipt",
         "On receipt, check the integrity of the packaging and that the batch numbers match the accompanying "
         "certificate of analysis. Carry out a density and pH check where available. In the event of an anomaly, keep "
         "the original packaging and contact our quality department within 48 hours. Procedure ref.: QC-RECEP-003."),
        ("Waste management",
         "Waste from this product must be managed in accordance with local hazardous waste regulations "
         "(Directive 2008/98/EC). Contact an approved contractor for disposal. European Waste Code (EWC): 06 01 04* for "
         "acid solutions, 07 01 01* for halogenated solvents, 07 01 04* for other organic solvents. "
         "Never discharge into drains or watercourses."),
        ("First aid (operational summary)",
         "INHALATION: Move the person to fresh air, in a semi-seated position. If breathing is difficult, "
         "administer O2 and call the emergency services (15 in France). SKIN CONTACT: Remove contaminated clothing. "
         "Rinse with plenty of water for at least 15 minutes. EYE CONTACT: Rinse with water for at least 15 minutes, "
         "holding the eyelids open. Consult an ophthalmologist. INGESTION: Do not induce vomiting. Rinse the mouth. "
         "Call the Poison Control Centre (European number: 0800 59 59 59)."),
        ("Environmental data (in-house results)",
         "BOD5 (5 days): tested per ISO 5815. COD: tested per ISO 15705. "
         "Log Kow (n-octanol/water partition coefficient): measured per OECD 117. "
         "Aerobic biodegradability: tested per OECD 301B. "
         "Aquatic toxicity (Daphnia magna): EC50 per OECD 202. "
         "For the complete numerical values, refer to section 12 of the Safety Data Sheet."),
        ("Additional regulatory information",
         f"This product is registered under REACH: registration number available on request. "
         "It is / is not on the SVHC candidate list (last ECHA update: Jan 2025). "
         "IED Directive: applicable to installations using this product in quantities above 200 t/year. "
         "French ICPE: check the classification under the ICPE nomenclature (heading 1175, 4110 or 4XXX depending on the product). "
         f"Certifications: {prod['certif']}."),
    ]

    for title_t, body in app_notes:
        story.append(Paragraph(f"<b>{title_t}</b>", s('ant', 10, bold=True, color=LBLUE, space_before=0.2)))
        story.append(Paragraph(body, s('anb', 9, leading=13)))
        story.append(Spacer(1, 0.2*cm))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    footer_text = (f"Document: {prod['ref']} | Version 3.2 | Issued 2024-09-01 | Revised: 2025-01-15\n"
                   f"{COMPANY} — 14 Rue des Réactifs, 69100 Villeurbanne — contact@chemcorp.fr\n"
                   "The information in this document is provided for guidance only. The user is solely responsible for the appropriate use of the product.")
    story.append(Paragraph(footer_text.replace('\n','<br/>'), s('ft', 7.5, color='#666666', leading=11)))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'website', 'docs', 'product-sheets')
    os.makedirs(out, exist_ok=True)
    for p in PRODUCTS:
        build_sheet(p, out)
    print(f"Done — {len(PRODUCTS)} product sheets generated.")
