#!/usr/bin/env python3.11
"""Generate mock chemical data sheets / analytical datasets for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
import os, random

random.seed(42)
BLUE = '#1a3a5c'; LBLUE = '#2d6a9f'; PALE = '#eef4fa'; DGREEN = '#1a5c2d'
COMPANY = "ChemCorp Industries S.A."

def p(text, size=9, bold=False, color='#000000', align='LEFT', leading=13, sb=0, sa=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}.get(align, TA_LEFT)
    return Paragraph(text, ParagraphStyle('x', fontSize=size,
                                          fontName='Helvetica-Bold' if bold else 'Helvetica',
                                          textColor=colors.HexColor(color), alignment=al,
                                          leading=leading, spaceBefore=sb*cm, spaceAfter=sa*cm))

# --- Dataset 1: Solvent purity monitoring (12 months, 3 products)
SOLVENTS = ['Acetone 99.5%', 'Methanol 99.9%', 'Isopropanol 99%']
MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def make_purity_data():
    rows = [['Month', 'Product', 'Batch', 'GC purity (%)', 'Water KF (%)', 'Colour APHA', 'Acidity (%)', 'Evap. residue (%)', 'Status']]
    lot_n = 241001
    for mi, mo in enumerate(MONTHS):
        for si, solv in enumerate(SOLVENTS):
            purity = round(random.gauss(99.65, 0.08), 2)
            water = round(random.gauss(0.09, 0.03), 3)
            apha = random.randint(2, 14)
            acid = round(random.gauss(0.0008, 0.0003), 4)
            residu = round(random.gauss(0.0005, 0.0002), 4)
            status = 'PASS' if (purity >= 99.5 and water <= 0.20 and apha <= 10) else 'FAIL'
            rows.append([mo, solv, f'LOT-{lot_n}', f'{purity:.2f}', f'{water:.3f}', str(apha), f'{acid:.4f}', f'{residu:.4f}', status])
            lot_n += 1
    return rows

# --- Dataset 2: Production batch records
PRODUCTS_BATCH = [
    ('AK-995', 'Acetone 99.5%', 'R-101', 87.5),
    ('ME-PUR', 'Pure methanol', 'R-102', 91.2),
    ('IPA-99', 'Isopropanol 99%', 'R-103', 88.8),
    ('ET-96D', 'Ethanol 96%', 'R-104', 85.4),
    ('GLY-USP', 'Glycerol USP', 'R-105', 92.1),
]

def make_batch_data():
    rows = [['Batch No.', 'Product', 'Reactor', 'Prod. date', 'Quantity (kg)', 'Yield (%)', 'Avg T °C', 'Avg P bar', 'Duration (h)', 'Operator', 'QC status']]
    dates = [f'2024-{m:02d}-{d:02d}' for m in range(1,13) for d in [3,8,14,20,26]]
    operators = ['Mr Dubois', 'Ms Laurent', 'Mr Petit', 'Ms Garcia', 'Mr Bernard']
    for i in range(45):
        pi = i % len(PRODUCTS_BATCH)
        prod = PRODUCTS_BATCH[pi]
        lot_n = f'B24{i+1001:04d}'
        date = dates[i % len(dates)]
        qty = round(random.gauss(1850, 200), 1)
        rend = round(random.gauss(prod[3], 2.5), 1)
        temp = round(random.gauss(82, 3), 1)
        pres = round(random.gauss(3.8, 0.3), 2)
        duree = round(random.gauss(6.5, 0.8), 1)
        op = operators[i % len(operators)]
        qc = 'OK' if rend >= 83 else 'REVIEW'
        rows.append([lot_n, prod[1], prod[2], date, f'{qty:,.1f}', f'{rend:.1f}', f'{temp:.1f}', f'{pres:.2f}', f'{duree:.1f}', op, qc])
    return rows

# --- Dataset 3: Energy consumption by unit
UNITS = ['Solvents workshop', 'Acids workshop', 'Bases workshop', 'Specialities workshop', 'Utilities / HVAC', 'Lighting / Misc.']
def make_energy_data():
    rows = [['Month', 'Unit', 'Elec. (MWh)', 'Gas (MWh NCV)', 'Steam (t)', 'Water (m³)', 'Waste (t)', 'CO₂ (t eq.)']]
    base_e = [145, 98, 67, 112, 88, 22]
    base_g = [32, 56, 78, 18, 44, 5]
    base_s = [12, 28, 45, 8, 65, 2]
    base_w = [38, 55, 42, 29, 120, 15]
    base_d = [2.1, 3.4, 1.8, 4.2, 0.5, 0.3]
    for mi, mo in enumerate(MONTHS):
        for ui, unit in enumerate(UNITS):
            factor = 1.0 + 0.08*abs(mi - 6)/6 + random.gauss(0, 0.04)
            e = round(base_e[ui] * factor, 1)
            g = round(base_g[ui] * factor, 1)
            s = round(base_s[ui] * factor, 1)
            w = round(base_w[ui] * factor, 1)
            d = round(base_d[ui] * factor, 2)
            co2 = round(e * 0.0567 + g * 0.185 + s * 0.070, 2)
            rows.append([mo, unit, f'{e:,}', f'{g:,}', f'{s:,}', f'{w:,}', f'{d:,}', f'{co2:,}'])
    return rows

DATASETS = [
    {
        "ref": "DS-QC-SOL-2024",
        "title": "Quality Control Data — Solvents 2024 (monthly monitoring)",
        "description": "This dataset compiles the monthly analytical results of the quality control checks carried out on the 3 main solvents produced by ChemCorp Industries in 2024. The analyses are performed by the in-house laboratory (COFRAC-accredited under No. 1-5421) on representative samples from each batch.",
        "method_notes": [
            ("GC purity", "Gas chromatography (GC-FID), Agilent DB-624 column, external calibration, in-house method QC-GC-001 based on ISO 11013"),
            ("Water (Karl Fischer)", "Volumetric KF titration, Metrohm 870 KF Titrino plus instrument, method ISO 760 / ASTM E1064"),
            ("Colour APHA/Hazen", "Hach DR 6000 spectrophotometer, method ASTM D1209 (Pt-Co scale)"),
            ("Acidity", "Potentiometric titration as acetic acid, in-house method QC-ACID-003"),
            ("Evaporation residue", "Evaporation for 2h at 105°C, weighed on a Mettler Toledo XPE205 microbalance, method ASTM D1353"),
        ],
        "spec_table": [
            ['Parameter', 'Acetone 99.5%', 'Methanol 99.9%', 'Isopropanol 99%', 'Method'],
            ['Purity (%)', '≥ 99.5', '≥ 99.9', '≥ 99.0', 'GC-FID'],
            ['Water (%)', '≤ 0.20', '≤ 0.05', '≤ 0.20', 'Karl Fischer'],
            ['Colour APHA', '≤ 10', '≤ 10', '≤ 10', 'ASTM D1209'],
            ['Acidity (%)', '≤ 0.002', '≤ 0.001', '≤ 0.002', 'Potentiometry'],
            ['Evap. residue (%)', '≤ 0.001', '≤ 0.001', '≤ 0.001', 'ASTM D1353'],
        ],
        "data_fn": make_purity_data,
        "col_widths": [1*cm, 3.8*cm, 2.5*cm, 2*cm, 1.8*cm, 1.5*cm, 1.8*cm, 2*cm, 2.6*cm],
        "statistics": [
            ('Acetone 99.5%', 'GC purity', '99.52–99.82%', '99.65%', '0.08%', '99.5% — 100%'),
            ('Methanol 99.9%', 'GC purity', '99.55–99.91%', '99.74%', '0.07%', '99.9% — 100%'),
            ('Isopropanol 99%', 'GC purity', '99.08–99.78%', '99.48%', '0.12%', '99.0% — 100%'),
            ('All solvents', 'Water KF (%)', '0.03–0.18%', '0.09%', '0.03%', '≤ 0.20%'),
            ('All solvents', 'Colour APHA', '2–14', '6', '3', '≤ 10'),
        ],
    },
    {
        "ref": "DS-PROD-BATCH-2024",
        "title": "Production Data — 2024 Manufacturing Batch History",
        "description": "This dataset lists the 45 manufacturing batches produced across the 5 production workshops of ChemCorp Industries during the first half of 2024. It includes the process parameters (temperature, pressure, duration) and the post-production quality control results.",
        "method_notes": [
            ("Yield", "Calculated as the mass of conforming finished product divided by the maximum theoretical mass. Losses included (purge, cleaning, QC sampling)."),
            ("Temperature", "Mean value of the temperature profile recorded by the Siemens PCS7 DCS — 1 min resolution."),
            ("Pressure", "Mean value recorded by Endress+Hauser PMP55 sensors — 1 min resolution."),
            ("Duration", "From the introduction of the reagents to release of the finished product by QC."),
            ("QC status", "OK: conforms to all specifications. REVIEW: at least one parameter out of specification — batch placed in quarantine."),
        ],
        "spec_table": [
            ['Process parameter', 'R-101', 'R-102', 'R-103', 'R-104', 'R-105'],
            ['T setpoint (°C)', '80±5', '75±3', '85±5', '78±4', '90±5'],
            ['P setpoint (bar)', '3.5–4.5', '2.5–3.5', '3.8–4.8', '3.0–4.0', '4.0–5.0'],
            ['Typical duration (h)', '5.5–7.5', '4.0–6.0', '5.5–8.0', '5.0–7.0', '6.0–8.0'],
            ['Target yield (%)', '>85', '>88', '>85', '>82', '>90'],
            ['Nominal capacity (kg/batch)', '2,000', '1,800', '2,200', '1,600', '2,400'],
        ],
        "data_fn": make_batch_data,
        "col_widths": [1.6*cm, 2.8*cm, 1.5*cm, 1.8*cm, 1.8*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.7*cm, 1.9*cm, 1.4*cm],
        "statistics": [
            ('R-101 (acetone)', 'Yield', '82.4–93.1%', '87.6%', '2.4%', '>85%'),
            ('R-102 (methanol)', 'Yield', '85.2–95.6%', '91.0%', '2.1%', '>88%'),
            ('R-103 (IPA)', 'Yield', '81.8–93.7%', '88.4%', '2.8%', '>85%'),
            ('All reactors', 'Mean temperature', '72.3–88.9°C', '82.1°C', '2.9°C', 'Process dependent'),
            ('All reactors', 'Mean duration', '4.2–9.1 h', '6.5 h', '0.8 h', 'Process dependent'),
        ],
    },
    {
        "ref": "DS-ENERGIE-2024",
        "title": "Energy and Environmental Consumption Data 2024",
        "description": "This dataset presents the monthly consumption of energy (electricity, natural gas, steam), water and waste generation per production unit at the Villeurbanne site for the year 2024. These data feed the annual ESG report and the carbon reporting (scopes 1 and 2).",
        "method_notes": [
            ("Electricity", "Schneider PowerLogic PM8000 sub-meters per unit — daily readings, aggregated monthly. Emission factor: 0.0567 kgCO₂/kWh (ADEME 2024 — French grid)."),
            ("Natural gas", "Elster BK-G16 meters — monthly readings. Emission factor: 0.185 kgCO₂/kWh NCV (ADEME 2024)."),
            ("Steam", "Yokogawa ADMAG mass meters on the distribution line. Steam emission factor: 0.070 kgCO₂/kg (in-house gas boiler production)."),
            ("Water", "Endress+Hauser Prosonic Flow ultrasonic meters on the demineralised water and process water networks."),
            ("Waste", "Waste tracking forms (BSD) CERFA No. 12571. Hazardous waste accounted for separately."),
            ("CO₂ equivalent", "Calculated using the formula: CO₂ = Elec×0.0567 + Gas×0.185 + Steam×0.070 (in tonnes). Scope: scopes 1 and 2 only."),
        ],
        "spec_table": [
            ['Indicator', '2022', '2023', '2024 target', '2027 target'],
            ['Total electricity (MWh)', '8,420', '8,102', '7,454 (-8%)', '6,320 (-22%)'],
            ['Total natural gas (MWh NCV)', '2,845', '2,710', '2,493 (-8%)', '2,140 (-21%)'],
            ['Total process water (m³)', '48,200', '45,600', '43,300 (-5%)', '36,500 (-20%)'],
            ['Total waste (t)', '812', '745', '690 (-7%)', '520 (-30%)'],
            ['Total CO₂ (t eq.)', '1,247', '1,198', '1,102 (-8%)', '868 (-28%)'],
            ['CO₂ intensity (kgCO₂/t product)', '1.39', '1.31', '1.20 (-8%)', '0.97 (-26%)'],
        ],
        "data_fn": make_energy_data,
        "col_widths": [1.2*cm, 3.5*cm, 1.8*cm, 2.2*cm, 1.5*cm, 1.5*cm, 1.6*cm, 2.2*cm],
        "statistics": [
            ('Solvents workshop', 'Elec. (MWh/month)', '132–165', '148', '10', 'OEE >80%'),
            ('Acids workshop', 'Gas (MWh/month)', '48–68', '57', '7', 'Boiler efficiency'),
            ('Site total', 'CO₂ per month (t)', '82–128', '99', '13', 'Annual target 1,102 t'),
            ('Bases workshop', 'Water (m³/month)', '35–55', '43', '6', 'Target -5%/year'),
            ('Site total', 'Waste (t/month)', '55–72', '62', '5', 'Target -7% in 2024'),
        ],
    },
]

def build_dataset(ds, out_dir):
    path = os.path.join(out_dir, f"{ds['ref']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=2*cm, bottomMargin=2*cm)
    story = []

    # Header
    hdr = Table([[
        [p(COMPANY, 12, bold=True, color='#ffffff'),
         p("ANALYTICAL DATASETS", 8, color='#aaccee')],
        [p(ds['title'], 10, bold=True, color='#ffffff'),
         p(f"Ref: {ds['ref']}", 8, color='#aaccee', align='RIGHT')]
    ]], colWidths=[10.5*cm, 7*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (0,-1), 12), ('RIGHTPADDING', (1,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.4*cm))

    # Description
    story.append(p("DESCRIPTION", 10, bold=True, color=BLUE))
    story.append(p(ds['description'], 9, color='#333333', leading=13))
    story.append(Spacer(1, 0.4*cm))

    # Methods
    story.append(p("ANALYTICAL METHODS AND ASSUMPTIONS", 10, bold=True, color=BLUE))
    for method, detail in ds['method_notes']:
        story.append(p(f"<b>{method}:</b> {detail}", 8.5, color='#333333', leading=12))
        story.append(Spacer(1, 0.05*cm))
    story.append(Spacer(1, 0.4*cm))

    # Spec / reference table
    story.append(p("SPECIFICATIONS / REFERENCE VALUES", 10, bold=True, color=BLUE))
    ncols = len(ds['spec_table'][0])
    avail = 17.5*cm
    cw = [avail/ncols]*ncols
    spt = Table(ds['spec_table'], colWidths=cw, repeatRows=1)
    spt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)), ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(spt)

    # Raw data table
    story.append(PageBreak())
    story.append(p(f"{ds['ref']} — Raw data", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    data_rows = ds['data_fn']()
    dt = Table(data_rows, colWidths=ds['col_widths'], repeatRows=1)
    n = len(data_rows)
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(DGREEN if 'ENERGIE' not in ds['ref'] else LBLUE)),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('GRID', (0,0), (-1,-1), 0.2, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 2), ('RIGHTPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(dt)

    # Statistics summary page
    story.append(PageBreak())
    story.append(p(f"{ds['ref']} — Statistical summary", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.4*cm))

    story.append(p("DESCRIPTIVE STATISTICS", 10, bold=True, color=BLUE))
    stat_rows = [['Subset', 'Parameter', 'Observed range', 'Mean', 'Std dev.', 'Specification']]
    for s in ds['statistics']:
        stat_rows.append(list(s))
    stat_t = Table(stat_rows, colWidths=[3.5*cm, 3*cm, 3*cm, 2*cm, 2*cm, 3.5*cm], repeatRows=1)
    stat_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)), ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'), ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(stat_t)
    story.append(Spacer(1, 0.5*cm))

    story.append(p("OBSERVATIONS AND CONCLUSIONS", 10, bold=True, color=BLUE))
    observations = [
        "Taken together, the results confirm that the production process remained in statistical control over the period considered.",
        "The Cpk indices calculated on the critical parameters (purity, water KF, colour) are above 1.33 for all 3 products, indicating satisfactory process capability.",
        "The slight drift observed on the APHA colour parameter during the summer months (July-August) correlates with higher storage temperatures — corrective action: the depot temperature setpoint was lowered to 18°C in summer.",
        "No definitively non-conforming batch was released to a customer. The 3 batches placed under review were successfully reprocessed.",
        "The data are archived in the ChemCorp LIMS (QC-TRACK v4.2 module) and available for COFRAC audit.",
    ]
    for obs in observations:
        story.append(p(f"  • {obs}", 9, color='#333333', leading=13))
        story.append(Spacer(1, 0.05*cm))

    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=colors.lightgrey))
    story.append(p(f"Data generated by ChemCorp LIMS v4.2 — {ds['ref']} — Confidentiality: internal. Contact: qualite@chemcorp.fr", 7.5, color='#666666'))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'data', 'datasets')
    os.makedirs(out, exist_ok=True)
    for d in DATASETS:
        build_dataset(d, out)
    print(f"Done — {len(DATASETS)} dataset PDFs generated.")
