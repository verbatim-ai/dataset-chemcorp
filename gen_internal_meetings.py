#!/usr/bin/env python3.11
"""Generate mock internal meeting notes for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
import os

BLUE = '#1a3a5c'; LBLUE = '#2d6a9f'; PALE = '#eef4fa'
COMPANY = "ChemCorp Industries S.A."

def p(text, size=9, bold=False, color='#000000', align='LEFT', leading=14, sb=0, sa=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}.get(align, TA_LEFT)
    return Paragraph(text, ParagraphStyle('x', fontSize=size, fontName='Helvetica-Bold' if bold else 'Helvetica',
                                          textColor=colors.HexColor(color), alignment=al, leading=leading,
                                          spaceBefore=sb*cm, spaceAfter=sa*cm))

MEETINGS = [
    {
        "ref": "CRI-RD-2024-003",
        "title": "R&amp;D Meeting — Bio-based solvent formulation development",
        "date": "2024-01-18", "time": "09:00–12:30", "location": "Innovation Room, Villeurbanne site",
        "chair": "Dr. Martine Chabrol, R&amp;D Director",
        "secretary": "Mr Antoine Ferretti, Project Manager",
        "attendees": [
            ("Dr. Martine Chabrol", "R&amp;D Management", "Present"),
            ("Mr Antoine Ferretti", "R&amp;D — Formulation", "Present"),
            ("Ms Sonia Blanc", "R&amp;D — Synthesis", "Present"),
            ("Mr Kévin Lecomte", "R&amp;D — Analytical", "Present"),
            ("Ms Clara Nguyen", "Product Marketing", "Present"),
            ("Mr Bertrand Vidal", "Production / Processes", "Present"),
            ("Dr. Paul Renaud", "Regulatory / REACH", "Apologies — represented by Mr Ferretti"),
        ],
        "agenda": [
            "Progress update on the BioSolv-3 project (bio-based industrial solvent formulation)",
            "Pilot test results on reactor unit R-103",
            "Competitive analysis — new entrants in the green solvents market",
            "Validation schedule and Q2 2024 patent filing",
            "Any other business",
        ],
        "sections": [
            ("1. BioSolv-3 progress update",
             [
                 "Dr. Chabrol opened the meeting at 09:05 and restated the objectives of the BioSolv-3 project: to develop "
                 "a range of industrial solvents derived more than 70% from renewable raw materials, with performance "
                 "equivalent to conventional solvents for degreasing and paint formulation applications.",
                 "Mr Ferretti presented the current status: formulation F-12C (a blend of isosorbide acetate / "
                 "methyl lactate / limonene) reaches a KB solvency value of 42, below the target of 50. Two optimisation "
                 "routes were identified: (a) increasing the limonene fraction from 15% to 22%, and (b) partially substituting "
                 "the methyl lactate with ethyl lactate to improve miscibility.",
                 "Ms Blanc reported thermal stability problems: formulation F-12C shows a tendency to develop colour "
                 "(APHA above 50) after 48h at 60°C, probably linked to oxidation of the limonene. She proposed "
                 "evaluating the addition of a phenolic antioxidant (BHT at 200 ppm) and working under an inert atmosphere "
                 "during packaging.",
                 "Mr Lecomte (analytical) presented the GC-MS characterisation data: the purity of the pilot batch is "
                 "compliant, but traces of residual lactic acid (180 ppm) were detected, requiring an additional "
                 "purification step. Proposal: passing the material over a basic ion-exchange resin.",
             ]),
            ("2. Pilot test results — Reactor R-103",
             [
                 "Mr Vidal (Production) presented the results of the pilot campaign of 8-12 Jan 2024 on reactor R-103 "
                 "(50 L). Reaction yield: 87.3% (target: above 90%). The pressure observed at the end of the reaction (4.2 bar) "
                 "slightly exceeds the nominal value of 4.0 bar — a check of safety valve SV-103B is "
                 "scheduled for 25 Jan.",
                 "The 85°C temperature setpoint is difficult to maintain: sensors TC-103A and TC-103B show "
                 "a deviation of ±3°C at steady state. Mr Vidal recommended recalibrating the sensors and evaluating "
                 "an adaptive PID controller.",
                 "Mass balance: 3.2 kg of unidentified by-products collected in the sump. Mr Lecomte will analyse "
                 "these fractions by HPLC during the week of 22 Jan. Results are expected for the next weekly update.",
                 "Ms Blanc proposed testing heterogeneous acid catalysis (H-ZSM-5 zeolite) to replace the "
                 "current homogeneous catalyst, to make recovery easier and improve selectivity. To be confirmed with "
                 "the supplier Zeochem before trials begin.",
             ]),
            ("3. Competitive analysis — Green solvents",
             [
                 "Ms Nguyen (Marketing) presented market intelligence gathered over Q4 2023: at least 4 competitors "
                 "launched or announced bio-based solvent ranges between September and December 2023. Key points: "
                 "Greensolv AG (Switzerland) filed patent EP3812450 covering a process for purifying methyl lactate "
                 "by membrane distillation — Mr Ferretti confirmed that our ion-exchange resin approach is "
                 "different and not covered.",
                 "Observed pricing: premium bio-based solvents at 2.5–3.5× the price of petrochemical equivalents "
                 "among competitors. ChemCorp is targeting a position at 1.8–2.2× thanks to the optimised process.",
                 "Discussion: Ms Nguyen proposed prioritising regulated markets (cosmetics, "
                 "pharmaceuticals, food-contact cleaning) where customers accept higher prices in exchange for "
                 "documented bio-based content. Mr Vidal noted the capacity constraints: 200 t/year maximum on the "
                 "pilot unit, which limits how far heavy industrial markets can be addressed.",
             ]),
            ("4. Validation schedule and patent filing",
             [
                 "Schedule approved in the meeting: (1) Finalise the optimised F-12C formulation — 15 March 2024. "
                 "(2) 200 L scale-up pilot campaign — April 2024. (3) Validation dossier (stability, compatibility, "
                 "performance) — May-June 2024. (4) PCT patent filing — 30 June 2024 (firm Lebret &amp; Associés). "
                 "(5) Industrialisation and first commercial launch — Q1 2025.",
                 "Mr Ferretti was appointed project coordinator (project manager). A monthly review point is "
                 "scheduled for the 3rd Thursday of each month, 09:00-10:00, Innovation Room.",
                 "2024 R&amp;D budget for BioSolv-3: €380k allocated, of which €120k for analytical work and external testing, "
                 "€85k for patent costs, and €175k for pilot and raw material costs.",
             ]),
        ],
        "actions": [
            ("Ms Blanc", "Prepare the BHT antioxidant trial plan + packaging under N₂", "2024-02-01"),
            ("Mr Lecomte", "Analyse the R-103 reactor by-product fractions by HPLC", "2024-01-26"),
            ("Mr Ferretti", "Contact the Lebret firm to scope the PCT patent filing", "2024-01-25"),
            ("Mr Vidal", "Schedule recalibration of sensors TC-103A/B and the SV-103B check", "2024-01-25"),
            ("Ms Nguyen", "Finalise the market study and price positioning proposal", "2024-02-15"),
            ("Dr. Chabrol", "Approve the 2024 BioSolv-3 budget with the Finance Director", "2024-01-30"),
        ],
        "next_meeting": "15 February 2024, 09:00, Innovation Room",
    },
    {
        "ref": "CRI-PROD-2024-007",
        "title": "Production Meeting — Monthly performance and safety review (January 2024)",
        "date": "2024-02-01", "time": "14:00–16:30", "location": "Conference room C2, Villeurbanne site",
        "chair": "Mr Bertrand Vidal, Production Manager",
        "secretary": "Ms Laurence Aubert, Industrial Management Assistant",
        "attendees": [
            ("Mr Bertrand Vidal", "Production", "Present"),
            ("Mr Jean-Paul Moreau", "Maintenance", "Present"),
            ("Ms Ingrid Hoffmann", "QHSE", "Present"),
            ("Mr Samuel Osei", "Logistics / Shipping", "Present"),
            ("Ms Carole Petit", "Purchasing", "Present"),
            ("Mr Thierry Bruneau", "Management control", "Present"),
            ("Ms Laurence Aubert", "Secretariat / Admin", "Present"),
        ],
        "agenda": [
            "January 2024 production KPIs — variance analysis",
            "Incidents and near misses for the month",
            "Status of preventive and corrective maintenance",
            "Raw material supply — pressure on MEG",
            "Preparation for the external ISO 9001 audit (March 2024)",
            "Any other business",
        ],
        "sections": [
            ("1. Production KPIs — January 2024",
             [
                 "Mr Vidal presented the production dashboard: overall utilisation rate 78.3% (target 85%), "
                 "down against December 2023 (82.1%). Main factors: the unplanned shutdown of reactor R-201 "
                 "(24-26 January, 2.5 days), and reduced throughput in the solvents workshop linked to the "
                 "MEG supply pressure (item 4).",
                 "Output achieved: 847 tonnes (target 920 t, variance -8.0%). By workshop: solvents 312 t (target 350 t), "
                 "acids 203 t (target 210 t), bases 180 t (target 185 t), specialities 152 t (target 175 t).",
                 "First pass yield (FPY): 94.1% (target 97%). Batches rejected: 3 batches (solvent A-45 batch B241089, "
                 "hydrochloric acid batch B241102, glycerol batch B241134). Causes: out-of-specification purity deviation for "
                 "the first two, trace Al contamination for the glycerol (raw material origin suspected — see action).",
                 "Mr Bruneau (management control): average unit production cost €1.42/kg against a budget of €1.38/kg, "
                 "+2.9%. The variance is mainly linked to energy costs (+8.4% vs budget, a market trend). "
                 "Raw material costs are within budget. Action: assess the opportunity of a fixed-price energy contract for 2025.",
             ]),
            ("2. Incidents and near misses",
             [
                 "Ms Hoffmann (QHSE) presented the safety summary: 0 lost-time accidents in January. 2 near misses "
                 "recorded: (PA-2024-003) minor leak on valve V-218 during a gasket replacement — detected during a "
                 "control round, no spillage, maintenance intervention within 25 min. (PA-2024-004) a fall from height "
                 "was avoided: an operator without a harness on walkway P-07, immediate procedure reminder issued.",
                 "Following PA-2024-003: an audit of all valves in the solvents workshop, prioritising valves "
                 "more than 3 years old. Scheduled by Mr Moreau (maintenance) for March-April 2024. Estimated budget: €22k.",
                 "Following PA-2024-004: a reminder of the working-at-height procedure was posted in all workshops. "
                 "The mandatory harness training for new starters was reviewed — a practical assessment was added on top "
                 "of the existing theory module. Ms Hoffmann is leading this.",
                 "Cumulative YTD safety indicators: LTIFR (lost time) = 0 ; TRIFR (no lost time) = 62.5 ; severity rate = 0.",
             ]),
            ("3. Maintenance",
             [
                 "Mr Moreau presented the maintenance status: 94% of the preventive plan completed in January (46/49 jobs). "
                 "3 deferrals: heat exchanger E-105 (part on order), pump P-312 (specialist intervention scheduled "
                 "10 Feb), agitator A-201 (reactor R-201 shutdown — see below).",
                 "R-201 shutdown (24-26 Jan): failure of the mechanical seal on agitator A-201. A spare part was "
                 "available in stock but the intervention required a full purge of the reactor. Total downtime: "
                 "60h. Recommendation: increase the stock of mechanical seals for critical reactors (2 units "
                 "minimum per reactor). Mr Moreau will propose an update to the critical spare parts plan.",
                 "OEE (Overall Equipment Effectiveness) for January: 71.2% (target 80%). Availability: 84%, Performance: "
                 "88%, Quality: 96%. The main area for improvement is availability (unplanned shutdowns).",
             ]),
            ("4. Supply — Pressure on monoethylene glycol (MEG)",
             [
                 "Ms Petit (Purchasing) reported worldwide pressure on MEG since mid-January: a production cut "
                 "at SABIC (Saudi Arabia) following maintenance on a cracker unit, and strong Asian demand (PET textiles). "
                 "Spot price: +18% in 3 weeks. Current ChemCorp stock: 45 tonnes (12 days of cover).",
                 "Emergency actions: (1) A spot order of 30 t from Brenntag (delivery 8 Feb, spot price + 12%). "
                 "(2) Contact with supplier BASF to bring forward the February contract delivery (+15 t). (3) Rationalisation "
                 "of formulations: a review is under way with R&amp;D on partially substituting DEG for MEG in "
                 "non-critical formulations (5 products identified).",
                 "Mr Vidal proposed launching a study into building a 90-day strategic stock for "
                 "the 5 most critical raw materials. Mr Bruneau will cost the corresponding working capital "
                 "(preliminary estimate: €800k–€1.2M).",
             ]),
        ],
        "actions": [
            ("Mr Moreau", "Audit solvents workshop valves over 3 years old + replacement budget proposal", "2024-03-15"),
            ("Ms Hoffmann", "Revise the working-at-height training module (add practical assessment)", "2024-02-28"),
            ("Ms Petit", "Finalise the 30 t MEG spot order with Brenntag", "2024-02-02"),
            ("Mr Bruneau", "Cost the working capital for a 90-day strategic stock of 5 critical raw materials", "2024-02-15"),
            ("Mr Vidal", "Propose an update to the critical reactor spare parts plan", "2024-02-15"),
            ("Quality Lab (Mr Lecomte)", "Identify the source of Al contamination in glycerol batch B241134", "2024-02-09"),
        ],
        "next_meeting": "7 March 2024, 14:00, Room C2",
    },
    {
        "ref": "CRI-STRAT-2024-002",
        "title": "Strategy Committee — Product portfolio review and 2025-2027 direction",
        "date": "2024-03-14", "time": "09:00–17:00", "location": "Board Room, Lyon Head Office",
        "chair": "Mr François Lemercier, CEO",
        "secretary": "Ms Hélène Marchand, Operations Director",
        "attendees": [
            ("Mr François Lemercier", "Executive Management", "Present"),
            ("Ms Hélène Marchand", "Operations / COO", "Present"),
            ("Dr. Martine Chabrol", "R&amp;D / CTO", "Present"),
            ("Mr Pierre Valentin", "Sales Management", "Present"),
            ("Mr Thierry Bruneau", "Finance / CFO", "Present"),
            ("Ms Ingrid Hoffmann", "QHSE &amp; Regulatory", "Present"),
            ("Mr Jacques Delorme", "Independent Director (guest)", "Present (morning)"),
        ],
        "agenda": [
            "2023 performance review and Q1 2024 outlook",
            "Product portfolio analysis — BCG and ROI by segment",
            "Presentation of the \"Green chemistry\" strategic pillar — BioSolv and GreenCat projects",
            "2025-2027 investment plan — prioritisation",
            "International expansion — Maghreb and Benelux markets",
            "Regulatory risks 2024-2025 (REACH SVHCs, F-gas)",
            "Closing remarks and decisions",
        ],
        "sections": [
            ("1. 2023 performance review",
             [
                 "Mr Bruneau presented the 2023 consolidated accounts (provisional): revenue €47.2M (+6.3% vs 2022), "
                 "EBITDA €8.4M (margin 17.8%, target 18.5%). The margin shortfall is mainly explained by "
                 "the rise in energy costs (+31% vs 2022) only partly passed through in prices (+9% on average), "
                 "and by the BioSolv-3 R&amp;D investment (€380k not originally budgeted).",
                 "Net income: €4.1M (+2.8% vs 2022). Positive net cash: €6.2M. Debt/EBITDA ratio: "
                 "1.4× (target below 2×). The financial position is sound enough to absorb the 2025-2027 investment plan.",
                 "By segment: industrial solvents 38% of revenue (+4%), inorganic acids and bases 28% (+8%), "
                 "chemical specialities 21% (+12%), trading 13% (-2%). Specialities (margins above 30%) are the "
                 "priority growth area.",
             ]),
            ("2. Portfolio analysis — BCG",
             [
                 "Dr. Chabrol presented the BCG analysis of the portfolio (41 active references): "
                 "Stars (growth above 10%, relative share above 1): 6 products (including USP propylene glycol, "
                 "refined glycerol, pilot bio-based formulations). "
                 "Cash cows (growth below 5%, share above 1): 12 products — standard chlorinated solvents and mineral "
                 "acids. Cash generators requiring little investment. "
                 "Question marks (growth above 10%, share below 1): 9 products — new catalysts, pharma specialities. "
                 "Dogs (growth below 5%, share below 1): 14 products, candidates for progressive discontinuation.",
                 "Mr Lemercier decided to launch a valuation analysis of the 14 \"dogs\" with the option of "
                 "divestment or discontinuation. Mr Valentin and Mr Bruneau were mandated to present options in June 2024.",
             ]),
            ("3. Green chemistry strategic pillar",
             [
                 "Dr. Chabrol presented the ChemCorp Green Chemistry roadmap for 2025-2030: "
                 "Pillar 1 — Bio-based: extension of the BioSolv range (target of 8 references by 2026), "
                 "a partnership under way with a Burgundy agricultural cooperative for biomass supply. "
                 "Pillar 2 — Green processes: the GreenCat project (heterogeneous catalysis to cut energy "
                 "consumption by 25% on esterification reactions), partial ANR funding requested. "
                 "Pillar 3 — Circular economy: recovery and valorisation of customers' used solvents "
                 "(a regeneration service), business model under study.",
                 "Mr Delorme (director) questioned the ability to certify bio-based origin: "
                 "Dr. Chabrol confirmed that the partnership with Bureau Veritas for ISCC+ certification is "
                 "under negotiation, with completion expected in September 2024.",
                 "Mr Bruneau presented the Green Chemistry business plan: total investment €2.8M over 3 years, "
                 "expected 5-year ROI: 18%. Funding: 40% equity, 30% bank debt, 30% grants "
                 "(ADEME, BPI France — applications in preparation).",
             ]),
            ("4. 2025-2027 investment plan",
             [
                 "Ms Marchand presented the consolidated 2025-2027 capex plan: total €7.4M over 3 years. "
                 "Priority 1 — Safety and regulatory compliance: €1.8M (SEVESO upgrades, "
                 "effluent treatment modernisation). "
                 "Priority 2 — Bio-based solvent capacity expansion: €2.2M (a new 5,000 L reactor "
                 "and a dedicated distillation unit). "
                 "Priority 3 — Digitalisation and automation: €1.4M (MES, LIMS, packaging "
                 "automation). "
                 "Priority 4 — R&amp;D (equipment): €2.0M (NMR spectrometer, GC-MS/MS chromatograph, "
                 "high-pressure autoclave reactor 100 mL×8).",
             ]),
        ],
        "actions": [
            ("Mr Valentin + Mr Bruneau", "Present valuation/divestment options for the 14 'dog' products", "2024-06-30"),
            ("Dr. Chabrol", "Finalise the ANR GreenCat application + the ADEME BioSolv application", "2024-04-30"),
            ("Ms Marchand", "Launch capex tenders for Priority 1 (safety/regulatory)", "2024-04-30"),
            ("Mr Bruneau", "Build the funding application for BPI France and partner banks", "2024-05-31"),
            ("Ms Hoffmann", "Present the SEVESO tier 2 compliance plan (if applicable)", "2024-04-30"),
        ],
        "next_meeting": "Next Strategy Committee: 12 September 2024",
    },
]

def build_meeting(meeting, out_dir):
    path = os.path.join(out_dir, f"{meeting['ref']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm)
    story = []

    # Header banner
    hdr = Table([[
        [p(COMPANY, 12, bold=True, color='#ffffff'),
         p("MEETING MINUTES", 9, color='#aaccee')],
        [p(meeting['title'], 11, bold=True, color='#ffffff'),
         p(f"Ref: {meeting['ref']}", 8.5, color='#aaccee', align='RIGHT')]
    ]], colWidths=[9.5*cm, 7.5*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (0,-1), 12), ('RIGHTPADDING', (1,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.4*cm))

    # Meta info
    meta = [
        ['Date', meeting['date'], 'Time', meeting['time']],
        ['Location', meeting['location'], 'Ref.', meeting['ref']],
        ['Chair', meeting['chair'], 'Secretary', meeting['secretary']],
    ]
    meta = [[Paragraph(c, ParagraphStyle('m', fontSize=9, fontName='Helvetica-Bold' if i in (0,2) else 'Helvetica', leading=11))
             for i, c in enumerate(row)] for row in meta]
    mt = Table(meta, colWidths=[3*cm, 7.5*cm, 2.5*cm, 4*cm])
    mt.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PALE)), ('BACKGROUND', (2,0), (2,-1), colors.HexColor(PALE)),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(mt)
    story.append(Spacer(1, 0.4*cm))

    # Attendees
    story.append(p("ATTENDEES", 10, bold=True, color=BLUE))
    att_rows = [['Name', 'Role / Department', 'Attendance']] + [[a, b, c] for a, b, c in meeting['attendees']]
    att_rows = [[Paragraph(c, ParagraphStyle('a', fontSize=9, leading=11,
                 fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                 textColor=colors.white if ri == 0 else colors.black)) for c in row]
                for ri, row in enumerate(att_rows)]
    at = Table(att_rows, colWidths=[4.5*cm, 7*cm, 5.5*cm], repeatRows=1)
    at.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.4*cm))

    # Agenda
    story.append(p("AGENDA", 10, bold=True, color=BLUE))
    for i, item in enumerate(meeting['agenda'], 1):
        story.append(p(f"  {i}. {item}", 9))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    # Discussion sections
    story.append(p("PROCEEDINGS", 11, bold=True, color=BLUE))
    story.append(Spacer(1, 0.2*cm))

    for sec_title, paragraphs in meeting['sections']:
        story.append(p(f"<b>{sec_title}</b>", 10, bold=False, color=LBLUE, sb=0.15))
        for para in paragraphs:
            story.append(p(para, 9, color='#222222', leading=14))
            story.append(Spacer(1, 0.1*cm))
        story.append(Spacer(1, 0.2*cm))

    # Actions table
    story.append(PageBreak())
    story.append(p(f"Minutes {meeting['ref']} — Action plan", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.4*cm))
    story.append(p("ACTION PLAN", 10, bold=True, color=BLUE))

    action_rows = [['Owner', 'Action to be taken', 'Due date']]
    for resp, action, date in meeting['actions']:
        action_rows.append([resp, action, date])
    action_rows = [[Paragraph(c, ParagraphStyle('ac', fontSize=9, leading=11,
                    fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                    textColor=colors.white if ri == 0 else colors.black)) for c in row]
                   for ri, row in enumerate(action_rows)]
    act_t = Table(action_rows, colWidths=[4.5*cm, 10*cm, 2.5*cm], repeatRows=1)
    act_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e67e22')),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#fef9f0'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(act_t)
    story.append(Spacer(1, 0.5*cm))

    story.append(p(f"Next meeting: {meeting['next_meeting']}", 9.5, bold=True, color=BLUE))
    story.append(Spacer(1, 0.3*cm))
    story.append(p("These minutes will be deemed approved unless written comments are received within 5 working days of circulation.", 8.5, color='#555555'))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'data', 'internal-meeting-notes')
    os.makedirs(out, exist_ok=True)
    for m in MEETINGS:
        build_meeting(m, out)
    print(f"Done — {len(MEETINGS)} internal meeting notes generated.")
