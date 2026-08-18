#!/usr/bin/env python3
"""Generate mock business goals / strategic plans for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
import os

BLUE = '#1a3a5c'; LBLUE = '#2d6a9f'; PALE = '#eef4fa'; GREEN = '#1a5c2d'; ORANGE = '#b35c00'
COMPANY = "ChemCorp Industries S.A."

def p(text, size=9, bold=False, color='#000000', align='LEFT', leading=14, sb=0, sa=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}.get(align, TA_LEFT)
    return Paragraph(text, ParagraphStyle('x', fontSize=size,
                                          fontName='Helvetica-Bold' if bold else 'Helvetica',
                                          textColor=colors.HexColor(color), alignment=al,
                                          leading=leading, spaceBefore=sb*cm, spaceAfter=sa*cm))

DOCS = [
    {
        "ref": "OBJ-STRAT-2024",
        "title": "Strategic Objectives &amp; Performance Plan 2024",
        "subtitle": "Reference document — Restricted circulation, Executive Committee",
        "date": "2024-01-10",
        "version": "v1.2",
        "sections": [
            ("VISION AND AMBITION 2027",
             "ChemCorp Industries aims to become the leading supplier of bio-based, low environmental impact chemical specialities in Southern and Western Europe, with an 8% market share in the green industrial solvents segment by 2027.",
             [
                 ("2027 revenue target", "€62M (+32% vs 2023)", "Based on organic growth of 8% per year and international expansion"),
                 ("2027 EBITDA margin target", "22%", "Improved product mix towards specialities (margin above 30%)"),
                 ("Bio-based share of revenue", "25% by 2027", "Against below 1% in 2023 — driven by the BioSolv and EcoSolv ranges"),
                 ("CO2 footprint reduction", "-35% in intensity per tonne by 2027", "2021 baseline, SBTi commitments under validation"),
                 ("New markets", "Active presence in Benelux + Maghreb + Poland", "Distribution agreements signed or in progress"),
             ]),
            ("COMMERCIAL OBJECTIVES 2024",
             "A year of transition and consolidation: strengthening the existing customer base, commercial launch of the first bio-based ranges, and development of 3 new geographic markets.",
             [
                 ("2024 revenue", "€50M (+6%)", "Growth driven by specialities (+15%) and international sales (+20%)"),
                 ("New customers signed", "8 new accounts", "Priority: Poland, Morocco, Benelux — 3 qualified prospects in the pipeline"),
                 ("Export revenue", "28% of revenue (vs 24% in 2023)", "Recruitment of a Business Development Manager for Eastern Europe"),
                 ("BioSolv-3 launch", "Q3 2024 — 3 pilot customers", "Plastex, Solvalor and Nordic Resins confirmed as beta testers"),
                 ("Contract renewal rate", "Above 95%", "Priority on the 8 accounts worth more than €1M per year"),
                 ("Customer satisfaction (NPS)", "Score above 50 (vs 38 in 2023)", "Quarterly survey, corrective actions within 30 days"),
             ]),
            ("INDUSTRIAL AND R&amp;D OBJECTIVES 2024",
             "Modernisation of production assets, improvement of OEE, and acceleration of the priority R&amp;D programmes (BioSolv, GreenCat, solvent regeneration).",
             [
                 ("Overall OEE", "80% (vs 72% in 2023)", "Reinforced preventive maintenance plan + MES digitalisation"),
                 ("First pass yield (FPY)", "97% (vs 94.1% in 2023)", "Operator training + SPC (statistical process control) in 3 workshops"),
                 ("Production waste reduction", "-20% by mass per tonne produced", "Lean Manufacturing plan launched in January 2024"),
                 ("Patent filings", "2 patents filed", "BioSolv-3 (PCT) + GreenCat (French national)"),
                 ("GreenCat progress", "50 L pilot demonstrator validated", "ANR funding secured provided the application is filed in March 2024"),
                 ("Production cost", "3% reduction at constant volume", "Raw material negotiation + energy optimisation + automation"),
             ]),
            ("CSR &amp; COMPLIANCE OBJECTIVES 2024",
             "ChemCorp is strengthening its ESG commitment with measurable objectives, reported annually under the GRI framework and the ESRS standard (CSRD applicable from 2026).",
             [
                 ("CDP score", "Reach level B (vs C+ in 2023)", "Improvement on scopes 1 &amp; 2 + start of scope 3 reporting"),
                 ("Energy consumption", "-8% in intensity (kWh per tonne)", "ADEME audit completed in Q1 2024, targeted investments"),
                 ("Workplace accidents (LTIFR)", "0", "STOP programme + systematic near-miss reporting"),
                 ("REACH SVHC compliance", "100% of products up to date", "SDS updated before June 2024 (new EU regulation)"),
                 ("Employee training", "40h per year per employee on average", "ChemCorp Academy: 12 modules available as e-learning"),
                 ("GRI sustainability report", "Published June 2024", "Deloitte engaged for external review"),
             ]),
            ("FINANCIAL OBJECTIVES 2024",
             "Control of operating costs in a context of margin pressure (energy, raw materials), while preserving investment capacity for the 2025-2027 capex plan.",
             [
                 ("2024 EBITDA", "€9.2M (margin 18.4%)", "Improvement on 2023 (17.8%) thanks to mix and cost optimisation"),
                 ("2024 net income", "€4.5M", "Excluding exceptional charges linked to the transformation plan"),
                 ("2024 capex", "€1.4M", "Maintenance and safety take priority; expansion capex deferred to 2025"),
                 ("Working capital (days)", "Reduction from 55 to 50 days", "Optimisation of customer receivables (DSO) and raw material stock management"),
                 ("Debt/EBITDA ratio", "Below 1.2×", "Preserving the capacity to raise €6-8M in 2025"),
                 ("Net cash at end 2024", "Above €7M", "Buffer for M&amp;A opportunities or technology acquisition"),
             ]),
        ],
        "risks": [
            ("Raw material price volatility", "High", "High", "6-month fixed-price contracts, 90-day strategic stock on 5 raw materials"),
            ("Delay to the BioSolv-3 programme", "Medium", "High", "Monthly milestones, contingency budget of €50k"),
            ("Rising energy costs", "High", "High", "Assessment of a multi-year energy contract with EDF/Engie"),
            ("Non-compliance with the new REACH SVHC list", "Low", "Medium", "Monthly regulatory watch, proactive SDS updates"),
            ("Loss of a major account (above €1M)", "Low", "High", "Tailored retention plans, quarterly NPS surveys"),
            ("Cyber-attack / data loss", "Medium", "High", "IT security audit in Q1 2024, BCP tested annually"),
        ],
        "governance": [
            "Monthly KPI review by the Executive Committee (first Tuesday of each month)",
            "Quarterly review with the Board of Directors (March, June, September, December)",
            "Half-year ESG reporting (June and December) — Deloitte",
            "Annual internal audit (2024 programme: finance, QHSE, IT — Grant Thornton)",
            "OKR progress reviews by department: weekly (operational) and monthly (strategic)",
        ],
    },
    {
        "ref": "OBJ-VERT-2024-2030",
        "title": "ChemCorp Green Chemistry Roadmap 2024-2030",
        "subtitle": "Environmental Transformation &amp; Innovation Programme",
        "date": "2024-02-28",
        "version": "v2.0",
        "sections": [
            ("WHY A GREEN CHEMISTRY ROADMAP",
             "European regulation (Green Deal, REACH, the green taxonomy), pressure from customers (buyer CSR criteria) and changing societal expectations place green chemistry at the heart of ChemCorp Industries' long-term competitiveness strategy.",
             [
                 ("Pillar 1: Bio-based products", "BioSolv range extended to 15 references by 2030", "Replacing petrochemicals with renewable raw materials (agricultural biomass, waste)"),
                 ("Pillar 2: Clean processes", "Energy -40% and water -30% by 2030", "Heterogeneous catalysis (GreenCat), electrochemistry, continuous processes"),
                 ("Pillar 3: Circular economy", "Used solvent regeneration service from 2026", "\"Solvent as a Service\" model: collection, regeneration, redelivery"),
                 ("Pillar 4: Sustainable supply chain", "100% of key suppliers CSR-assessed by 2026", "EcoVadis score or equivalent required for suppliers above €200k per year"),
                 ("Pillar 5: Carbon transparency", "Operational carbon neutrality (scope 1+2) by 2030", "PAS 2060 certification targeted; residual offsetting via VCS"),
             ]),
            ("BIOSOLV PROGRAMME — DETAIL 2024-2026",
             "The BioSolv programme is the flagship of the roadmap. It aims to substitute standard petrochemical solvents with functional equivalents derived from biomass.",
             [
                 ("BioSolv-3 (methyl lactate acetate)", "Commercial launch Q3 2024", "97% bio-based, boiling point 144°C, KB solvency 48, ISCC+ certification Q4 2024"),
                 ("BioSolv-5 (technical limonene)", "Launch Q1 2025", "Derived from citrus peel (partnership with a southern cooperative), boiling point 176°C, \"made in France\" label"),
                 ("BioSolv-7 (bio-based glycol ether)", "Feasibility study 2024, launch 2026", "Co-development with IFPEN; potential 500 t/year in the electronics cleaning segment"),
                 ("BioSolv-10 (degreaser range)", "Launch 2026", "Complete ready-to-use formulations — 4 references (light, standard, concentrated, high temperature)"),
             ]),
            ("GREENCAT PROGRAMME — GREEN CATALYSIS",
             "GreenCat aims to develop reusable heterogeneous catalysts for ChemCorp's main synthesis reactions, reducing the consumption of homogeneous acids and the generation of salt.",
             [
                 ("GreenCat-Est (esterification)", "50 L pilot validated Q4 2024", "Modified H-ZSM-5 zeolite; estimated energy saving -23%; ANR co-funding €180k"),
                 ("GreenCat-Hyd (hydration)", "Laboratory study 2024-2025", "Applied to the hydration of light olefins; partnership with CNRS Lyon"),
                 ("GreenCat-Ox (mild oxidation)", "Exploratory research 2025-2027", "Replacing KMnO4/CrO3 with Au/TiO2 catalysis for primary alcohols"),
             ]),
            ("KEY MILESTONES AND INDICATORS",
             "The roadmap is steered through quarterly milestones and key performance indicators (KPIs) approved by the Executive Committee and the Board of Directors.",
             [
                 ("Bio-based share of revenue", "2024: 2% | 2026: 12% | 2030: 25%", "Monthly monitoring — Executive Committee reporting"),
                 ("CO2 intensity (kgCO2 per tonne of product)", "2024: -10% | 2027: -30% | 2030: -50%", "2021 baseline; scope 1+2; annual Deloitte audit"),
                 ("Energy intensity (kWh per tonne)", "2024: -8% | 2027: -22% | 2030: -40%", "Monitored by workshop; real-time energy dashboards"),
                 ("Waste to landfill", "2024: below 5% | 2030: 0%", "Zero non-recovered waste plan; partnership with Veolia since 2024"),
                 ("Green Chemistry R&amp;D budget", "2024: €380k | 2025: €650k | 2027: €1.2M", "Of which 30% grant-funded (ANR, ADEME, Horizon Europe)"),
             ]),
            ("FUNDING AND GOVERNANCE",
             "The roadmap draws on mixed funding (equity, green debt, grants, research tax credit) and a dedicated governance structure.",
             [
                 ("Total budget 2024-2030", "€14.2M (7 years)", "40% equity, 25% BPI green debt, 20% grants, 15% research tax credit"),
                 ("Green Chemistry Steering Committee", "Quarterly meeting", "CEO + CTO + COO + CFO + Head of CSR + 1 independent director"),
                 ("External partners", "Bureau Veritas (ISCC+) + Deloitte (ESG audit)", "Reports published annually on the ChemCorp website"),
                 ("UN Sustainable Development Goals addressed", "SDG 9, 12, 13, 17", "Industrial innovation, responsible consumption, climate action"),
             ]),
        ],
        "risks": [
            ("Biomass availability / price", "High", "High", "Multi-year supply contracts with cooperatives"),
            ("Delay to ISCC+ certification", "Medium", "Medium", "Weekly follow-up with Bureau Veritas; fallback: RSPO certification"),
            ("Failure to secure ANR GreenCat funding", "Low", "High", "Alternative funding via BPI France ETI Ready planned"),
            ("Fast-moving competition in bio-based products", "Medium", "High", "Accelerated patent filing + exclusivity for pilot customers"),
            ("Bio-based content not recognised by regulation", "Low", "Medium", "Participation in AFNOR and ChemBioEurope working groups"),
        ],
        "governance": [
            "Green Chemistry Steering Committee (quarterly) — CEO + CTO + CFO + CSR",
            "Monthly progress report to the Executive Committee",
            "Public annual report aligned with GRI + SASB (published in March)",
            "Annual external ESG audit (Deloitte) since 2022",
            "Stakeholder dialogue (customers, suppliers, NGOs) — annual ChemCorp Vert forum",
        ],
    },
]

def build_doc(doc_data, out_dir):
    path = os.path.join(out_dir, f"{doc_data['ref']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm)
    story = []

    # Cover-style header
    cover = Table([[
        [p(COMPANY, 14, bold=True, color='#ffffff'),
         p(doc_data['subtitle'], 9, color='#aaccee'),
         Spacer(1, 0.3*cm),
         p(doc_data['title'], 13, bold=True, color='#ffffff')],
        [p(f"Ref: {doc_data['ref']}", 9, color='#aaccee', align='RIGHT'),
         p(f"Version: {doc_data['version']}", 9, color='#aaccee', align='RIGHT'),
         p(f"Date: {doc_data['date']}", 9, color='#aaccee', align='RIGHT'),
         Spacer(1, 0.3*cm),
         p("CONFIDENTIAL — EXECUTIVE COMMITTEE ONLY", 8, color='#ff9999', align='RIGHT')]
    ]], colWidths=[11*cm, 6*cm])
    cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 14), ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LEFTPADDING', (0,0), (0,-1), 14), ('RIGHTPADDING', (1,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(cover)
    story.append(Spacer(1, 0.6*cm))

    # Executive summary / intro paragraph
    story.append(p("EXECUTIVE SUMMARY", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.2*cm))
    story.append(p(
        f"This document sets out the objectives and commitments of ChemCorp Industries for the period covered. "
        f"It is intended for the Executive Committee and the Board of Directors. "
        f"It serves as the reference for operational and strategic steering, KPI monitoring and "
        f"stakeholder communication. Any modification must be approved by the CEO and the CFO. "
        f"Document ref.: {doc_data['ref']} — {doc_data['version']} dated {doc_data['date']}.",
        9, color='#333333'))
    story.append(Spacer(1, 0.5*cm))

    # Sections
    for sec_title, intro, rows in doc_data['sections']:
        story.append(p(sec_title, 11, bold=True, color=BLUE, sb=0.2))
        story.append(HRFlowable(width="100%", thickness=0.4, color=colors.HexColor(LBLUE)))
        story.append(Spacer(1, 0.2*cm))
        story.append(p(intro, 9, color='#444444', leading=13))
        story.append(Spacer(1, 0.3*cm))

        table_rows = [['Objective / Item', 'Target / Value', 'Comment / Detail']]
        for r in rows:
            table_rows.append(list(r))
        table_rows = [[Paragraph(c, ParagraphStyle('bg', fontSize=8.5, leading=10.5,
                       fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                       textColor=colors.white if ri == 0 else colors.black)) for c in row]
                      for ri, row in enumerate(table_rows)]
        t = Table(table_rows, colWidths=[5.5*cm, 3.5*cm, 8*cm], repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
            ('FONTSIZE', (0,0), (-1,-1), 8.5),
            ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
            ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.4*cm))

    # Page 2 — Risks and governance
    story.append(PageBreak())
    story.append(p(f"{doc_data['ref']} — Risk management &amp; governance", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.4*cm))

    story.append(p("PRINCIPAL RISK ANALYSIS", 10, bold=True, color=BLUE))
    risk_rows = [['Identified risk', 'Likelihood', 'Impact', 'Mitigation plan']]
    for r in doc_data['risks']:
        risk_rows.append(list(r))
    risk_rows = [[Paragraph(c, ParagraphStyle('rk', fontSize=8.5, leading=10.5,
                  fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                  textColor=colors.white if ri == 0 else colors.black)) for c in row]
                 for ri, row in enumerate(risk_rows)]
    rt = Table(risk_rows, colWidths=[5*cm, 2*cm, 1.8*cm, 8.2*cm], repeatRows=1)
    rt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8b0000')),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fdf2f2'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(rt)
    story.append(Spacer(1, 0.5*cm))

    story.append(p("GOVERNANCE AND MONITORING ARRANGEMENTS", 10, bold=True, color=BLUE))
    for g in doc_data['governance']:
        story.append(p(f"  » {g}", 9, color='#333333'))
    story.append(Spacer(1, 0.5*cm))

    # Signature block
    story.append(p("APPROVAL AND SIGNATURES", 10, bold=True, color=BLUE))
    sig_rows = [
        ['Prepared by', 'Reviewed by', 'Approved by'],
        ['Dr. Martine Chabrol\nR&amp;D Director', 'Ms Hélène Marchand\nOperations Director', 'Mr François Lemercier\nCEO'],
        ['Signature:\n\n\n', 'Signature:\n\n\n', 'Signature:\n\n\n'],
        ['Date:', 'Date:', 'Date:'],
    ]
    sig_rows[0] = [Paragraph(f"<b>{c}</b>", ParagraphStyle('sh', fontSize=9, fontName='Helvetica-Bold', leading=11)) for c in sig_rows[0]]
    sig_rows[1] = [Paragraph(c.replace('\n', '<br/>'), ParagraphStyle('sb', fontSize=9, leading=11)) for c in sig_rows[1]]
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
    story.append(Spacer(1, 0.4*cm))
    story.append(p(f"© {COMPANY} — Proprietary document. Reproduction prohibited without written authorisation. Ref: {doc_data['ref']} {doc_data['version']}.", 7.5, color='#666666'))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'website', 'docs', 'business-goals')
    os.makedirs(out, exist_ok=True)
    for d in DOCS:
        build_doc(d, out)
    print(f"Done — {len(DOCS)} business goal documents generated.")
