#!/usr/bin/env python3
"""Generate mock customer meeting notes for ChemCorp Industries."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
import os

BLUE = '#1a3a5c'; LBLUE = '#2d6a9f'; PALE = '#eef4fa'; GREEN = '#1a6b3a'
COMPANY = "ChemCorp Industries S.A."

def p(text, size=9, bold=False, color='#000000', align='LEFT', leading=14, sb=0, sa=0):
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
    al = {'LEFT': TA_LEFT, 'RIGHT': TA_RIGHT, 'CENTER': TA_CENTER}.get(align, TA_LEFT)
    return Paragraph(text, ParagraphStyle('x', fontSize=size,
                                          fontName='Helvetica-Bold' if bold else 'Helvetica',
                                          textColor=colors.HexColor(color), alignment=al,
                                          leading=leading, spaceBefore=sb*cm, spaceAfter=sa*cm))

MEETINGS = [
    {
        "ref": "CRC-PLASTEX-2024-01",
        "type": "Annual sales visit",
        "title": "Minutes — Customer visit to Plastex GmbH (Munich)",
        "date": "2024-01-30", "time": "10:00–16:30",
        "location": "Plastex GmbH head office, Industriestraße 44, Munich",
        "chemcorp_attendees": [
            ("Mr Pierre Valentin", "Sales Director"),
            ("Ms Sophie Durand", "Key Account Manager DACH"),
            ("Dr. Martine Chabrol", "R&amp;D Director (present in the afternoon)"),
        ],
        "customer_attendees": [
            ("Dr. Klaus Weber", "Purchasing Director"),
            ("Ms Anna Krüger", "Supply Manager"),
            ("Mr Thomas Bauer", "Head of R&amp;D, Plastex"),
            ("Ms Lena Schreiber", "Quality Manager"),
        ],
        "customer": "Plastex GmbH",
        "customer_profile": "Manufacturer of technical plastic parts (polycarbonate, ABS, POM) for the automotive and electronics industries. 2023 revenue: approx. €180M. Main purchases from ChemCorp: acetone (1,200 t/year), toluene (400 t/year), isopropyl alcohol (300 t/year).",
        "context": "Annual review of the partnership. The current framework contract expires on 2024-12-31. In 2023 Plastex launched a \"Green Manufacturing\" initiative imposing sustainability criteria on its suppliers.",
        "sections": [
            ("1. 2023 review and customer satisfaction",
             [
                 "Dr. Weber opened the meeting and presented the 2023 purchasing review: volumes delivered were in line with forecast "
                 "(acetone 1,187 t, toluene 398 t, IPA 312 t). ChemCorp service rate: 96.8% (Plastex target: 97%). "
                 "A delivery delay in August (acetone, week 33) caused a 4h line stoppage; the internal cost was "
                 "estimated by Ms Krüger at €12k.",
                 "Ms Schreiber (Quality) was satisfied with the certificates of analysis but raised 2 non-conformities: "
                 "batch ACK-230814 (acetone): APHA colour 15 against a specification of 10 max — accepted under concession but to be avoided; "
                 "batch IPA-231102 (IPA): water content 0.23% against 0.20% max — batch rejected and replaced at no extra cost.",
                 "Mr Valentin presented the ChemCorp indicators: customer satisfaction score 7.8/10 (annual survey), "
                 "complaints resolved in 5 days on average. He set out the 2024 improvements: a new customer "
                 "platform for real-time delivery tracking, and automatic alerts 3 days before delivery.",
             ]),
            ("2. Commercial terms for the 2025 framework contract",
             [
                 "Mr Valentin presented the ChemCorp proposal for the 2025 framework contract: committed volumes of acetone "
                 "1,300 t (+9%), toluene 400 t (flat), IPA 320 t (+3%). Pricing: indexed monthly to the IHS Markit "
                 "Chemical Price Index plus a fixed contractual margin. Progressive volume discount: -1.5% from 1,200 t, "
                 "-3% above 1,500 t of acetone.",
                 "Dr. Weber asked whether ChemCorp could absorb late delivery penalties: Mr Valentin proposed "
                 "0.05% of the value of the delivery concerned per day of delay, capped at 5%. Dr. Weber counter-proposed "
                 "0.1% — a compromise at 0.08% was accepted in the meeting.",
                 "Ms Krüger asked about the possibility of urgent partial deliveries within 48h (instead of 5 days): "
                 "Mr Valentin confirmed this is feasible for volumes below 5 t from the Limonest depot (permanent safety stock "
                 "confirmed by Ms Marchand by email). Urgency surcharge: +8% on the contract price.",
             ]),
            ("3. Plastex Green Manufacturing initiative",
             [
                 "Ms Krüger presented the new Plastex CSR requirements for Tier-1 suppliers (applicable "
                 "from January 2025): a minimum Carbon Disclosure Project (CDP) score of B, an annual sustainability report "
                 "aligned with GRI, and documented traceability of renewable raw materials.",
                 "Dr. Chabrol (arrived at 14:00) presented the ChemCorp Green Chemistry programme: the BioSolv range under development "
                 "(limonene, lactic esters), ISCC+ certification in progress, and an annual ESG report published since 2022 "
                 "(current CDP score: C+ — with a plan to reach B by 2025).",
                 "Mr Bauer (R&amp;D Plastex) expressed strong interest in a bio-based version of ethyl acetate for "
                 "plastic paint formulations. Dr. Chabrol proposed a co-development programme: "
                 "supply of 500 kg of BioEster-1 prototype for testing in Q3 2024, with an NDA signed in the meeting (annex 1).",
                 "Plastex undertook to grant exclusivity in principle (without firm commitment) for 18 months "
                 "if the test results are satisfactory and if ChemCorp can deliver 50 t/year at nominal rate.",
             ]),
            ("4. Visit to the Plastex production site",
             [
                 "Afternoon: a tour of the injection moulding and extrusion workshops. Mr Valentin identified an "
                 "unaddressed opportunity: Plastex uses DMF (dimethylformamide) from a third-party supplier for "
                 "certain polishing applications. Volume: approx. 80 t/year. Ms Durand will send a "
                 "competitive offer with a full SDS within 2 weeks.",
                 "Ms Schreiber showed the quality control room: ChemCorp needs to align with the Plastex "
                 "analytical methods for 4 parameters (colorimetry, evaporation residue, acidity, miscibility). "
                 "An inter-laboratory correlation plan was proposed by Ms Schreiber — Dr. Chabrol accepted "
                 "and appointed Mr Lecomte as technical contact.",
             ]),
        ],
        "opportunities": [
            ("DMF 80 t/year", "New product — currently third-party supplier", "High", "Ms Durand — offer within 15 days"),
            ("BioEster-1 prototype", "Bio-based co-development", "Very high", "Dr. Chabrol — Q3 2024 programme"),
            ("IPA extension 2025", "Volume +3% framework contract", "Confirmed", "Mr Valentin — contract being drafted"),
        ],
        "actions": [
            ("Mr Valentin", "Draft and send the 2025 framework contract proposal", "2024-02-15"),
            ("Ms Durand", "Send a competitive DMF offer for 80 t/year + SDS", "2024-02-14"),
            ("Dr. Chabrol", "Schedule production of 500 kg BioEster-1 prototype + test protocol", "2024-02-29"),
            ("Mr Lecomte", "Contact Ms Schreiber about the inter-laboratory correlation plan", "2024-02-10"),
            ("Ms Durand", "Prepare the visit report for the CRM (Salesforce)", "2024-02-02"),
        ],
        "next_contact": "Monthly call on 2024-02-28, then framework contract review in March 2024.",
    },
    {
        "ref": "CRC-SOLVALOR-2024-03",
        "type": "Technical and commercial meeting",
        "title": "Minutes — Meeting with Solvalor S.A.S. (Harfleur)",
        "date": "2024-02-20", "time": "09:30–14:00",
        "location": "Solvalor S.A.S., ZI Nord, Bldg C, Harfleur (site visit included)",
        "chemcorp_attendees": [
            ("Ms Sophie Durand", "Key Account Manager, Northern France"),
            ("Mr Antoine Ferretti", "R&amp;D Project Manager (bio-based solvents)"),
        ],
        "customer_attendees": [
            ("Mr Marc Tessier", "Managing Director"),
            ("Ms Julie Morin", "Purchasing &amp; Supply Manager"),
            ("Mr Didier Fontaine", "Production Manager"),
        ],
        "customer": "Solvalor S.A.S.",
        "customer_profile": "Formulator of industrial cleaning solvents and degreasers. Revenue approx. €22M. Main purchases from ChemCorp: methanol (600 t/year), isopropanol (250 t/year), ethyl acetate (180 t/year). A customer for 11 years.",
        "context": "Solvalor is going through a strategic transition towards low-VOC (volatile organic compound) products to meet the DECO directive and new REACH regulations on solvents. The meeting focused on adapting the ChemCorp offer.",
        "sections": [
            ("1. Update on the VOC regulatory situation",
             [
                 "Mr Tessier opened by setting out the context: the European DECO directive (2004/42/EC) and its "
                 "national revisions impose ever stricter VOC contents in degreaser "
                 "formulations. Solvalor must reformulate 60% of its catalogue by the end of 2025 to maintain its "
                 "sector accreditations (aerospace, rail).",
                 "Ms Morin detailed the volumes to be substituted: methanol -40% over 3 years (impact: -240 t/year for ChemCorp), "
                 "and partial replacement of ethyl acetate by esters with a higher boiling point. "
                 "This represents a revenue risk of approximately €200k/year for ChemCorp if no alternative is offered.",
                 "Mr Ferretti presented the ChemCorp solutions: (a) the EcoSolv range: high boiling point / "
                 "low VOC solvent blends available since Q4 2023, (b) BioSolv-3 under development: bio-based "
                 "methyl lactate acetate, boiling point 145°C, negligible VOC. Ms Morin asked for samples and data sheets.",
             ]),
            ("2. Evaluation of the EcoSolv-D4 formulation",
             [
                 "Mr Fontaine presented the in-house test results for the EcoSolv-D4 formulation received in "
                 "December 2023 (5 L samples). Tests were run on 3 applications: degreasing rolled steel, "
                 "cleaning anodised aluminium, and cleaning ABS plastics.",
                 "Results: degreasing power, Kavale test 7.2 (target: above 7.0) — met. Drying time 8 min at 20°C "
                 "(target: under 10 min) — met. Material compatibility: OK on steel and aluminium, traces of whitening on ABS "
                 "— requires a formulation adjustment. Odour judged acceptable by the operators (5-person panel test).",
                 "Mr Fontaine asked for a version with 5% less aromatic co-solvent to avoid the ABS whitening. "
                 "Mr Ferretti undertook to prepare an EcoSolv-D4-mod formulation within 3 weeks, with 500 mL "
                 "for re-testing. If validated, a 5 t pilot order is envisaged.",
             ]),
            ("3. Commercial terms and the 2024-2025 contract",
             [
                 "Ms Morin asked for an 18-month price commitment on the stable volumes (methanol 360 t, "
                 "IPA 250 t) despite the transition. Ms Durand accepted a fixed price based on the September "
                 "2023 index, with revision possible if the index moves by more than 15% (hardship clause).",
                 "New product EcoSolv-D4: proposed price €1,285/t (against methanol at €420/t), justified by the "
                 "formulated value. Mr Tessier asked for €1,200/t. No compromise was reached in the meeting — Ms Durand "
                 "will come back with a counter-proposal including a discount on bundled volumes.",
                 "Site visit: Ms Durand identified a storage problem: the methanol tanks are "
                 "undersized for bulk delivery (20 t tanker). Solvalor currently receives material "
                 "in 200 L drums (a logistics surcharge). Opportunity: a study into installing a 40 t tank by ChemCorp "
                 "(rental or co-funding) — Mr Vidal to be consulted.",
             ]),
            ("4. Future developments and roadmap",
             [
                 "Mr Tessier expressed interest in the possibility of co-branding \"Made in France Vert\" on the "
                 "EcoSolv ranges: Ms Durand will check with the legal department whether this is compatible with the existing "
                 "distribution agreements.",
                 "Mr Ferretti presented the BioSolv roadmap: commercial availability of BioSolv-3 is planned for Q1 2025, "
                 "with possible sector exclusivity for \"industrial cleaning\" for Solvalor subject to a volume commitment "
                 "of 100 t/year over 3 years. Mr Tessier was very interested — to be formalised at a future meeting.",
             ]),
        ],
        "opportunities": [
            ("EcoSolv-D4 5 t pilot", "After validation of the modified reformulation", "High", "Mr Ferretti — 3 weeks"),
            ("40 t methanol tank", "Logistics saving for Solvalor", "Medium", "Mr Vidal — co-funding study"),
            ("BioSolv-3 sector exclusivity", "Commitment of 100 t/year over 3 years", "Very high", "Meeting in Q4 2024"),
        ],
        "actions": [
            ("Mr Ferretti", "Prepare the EcoSolv-D4-mod formulation (500 mL) without aromatic co-solvent", "2024-03-12"),
            ("Ms Durand", "Send the EcoSolv-D4 price counter-proposal with a bundled volume discount", "2024-02-27"),
            ("Ms Durand", "Check co-branding compatibility with the legal department", "2024-02-28"),
            ("Mr Vidal", "Assess the feasibility and cost of installing a 40 t methanol tank at Solvalor", "2024-03-15"),
        ],
        "next_contact": "Feedback on the D4-mod reformulation: week of 2024-03-18. Review meeting: April 2024.",
    },
    {
        "ref": "CRC-NORDIC-2024-05",
        "type": "Half-year business review (conference call)",
        "title": "Minutes — H1 Business Review with Nordic Resins AB",
        "date": "2024-04-10", "time": "13:00–15:30 (CET)",
        "location": "Teams video conference",
        "chemcorp_attendees": [
            ("Mr Pierre Valentin", "Sales Director"),
            ("Ms Sophie Durand", "Key Accounts Nordic / Benelux"),
            ("Mr Samuel Osei", "International Logistics"),
        ],
        "customer_attendees": [
            ("Mr Erik Lindqvist", "Procurement Manager"),
            ("Ms Astrid Svensson", "Head of R&amp;D"),
            ("Mr Johan Persson", "Quality Assurance"),
        ],
        "customer": "Nordic Resins AB",
        "customer_profile": "Manufacturer of alkyd and unsaturated polyester resins for paints and coatings. Head office in Södertälje (Sweden). Revenue approx. €95M. Purchases from ChemCorp: phthalic acid (300 t/year), maleic anhydride (200 t/year), propylene glycol (400 t/year).",
        "context": "Standard half-year business review. Nordic Resins recently acquired a plant in Finland (Tampere), creating new requirements. Negotiation on extending the framework contract (expires June 2024).",
        "sections": [
            ("1. Delivery performance H1 2024",
             [
                 "Mr Osei presented the logistics KPIs: 14 deliveries completed since January 2024, on-time rate "
                 "100% (an improvement on 92% in H2 2023 following the transport reorganisation). H1 volume: 225 t (phthalic acid "
                 "85 t, maleic anhydride 65 t, propylene glycol 75 t). On track to exceed the annual target.",
                 "Mr Persson confirmed 0 quality complaints in H1 2024. He noted that Nordic Resins will adopt "
                 "the IATF 16949 standard for its new plant in Finland — additional requirements will be "
                 "sent in May for validation by ChemCorp.",
             ]),
            ("2. Requirements for the new Tampere site (Finland)",
             [
                 "Mr Lindqvist presented the requirements of the new site: production start-up planned for October 2024. "
                 "Estimated Tampere volumes: propylene glycol 150 t/year, phthalic acid 80 t/year, and potentially "
                 "fumaric acid 50 t/year (a product not yet supplied by ChemCorp).",
                 "Finland logistics: Mr Osei assessed the options — road transport via the Helsinki ferry from "
                 "Hamburg (6-day lead time), or storage with a Finnish forwarder (Kemi Logistics, a ChemCorp partner). "
                 "Solution selected: a 30-day forward stock at Kemi Logistics in Tampere, replenished monthly.",
                 "Ms Durand proposed an amendment to the framework contract covering the Tampere site on terms "
                 "identical to the Södertälje site. The combined volumes make it possible to move to the next discount tier "
                 "(-2.5% on all products). Mr Lindqvist was very favourable — the amendment is to be drafted.",
             ]),
            ("3. Fumaric acid — new item",
             [
                 "Ms Svensson explained the fumaric acid requirement: it is used as a co-monomer in unsaturated polyester "
                 "resins to improve chemical resistance. Nordic Resins currently buys from a Chinese "
                 "supplier (CNHC Chemical) with recurring quality problems (impurities, purity variations).",
                 "Mr Valentin checked during the meeting: ChemCorp has a qualified European supplier "
                 "(Bartek Ingredients, Canada/Europe) for technical grade fumaric acid. Purity: above 99.5%, with a "
                 "systematic COA. Price: approx. €920/t (against approx. €750/t from the current Chinese supplier plus transport and quality costs).",
                 "Ms Svensson agreed to receive 100 kg for internal qualification (10 weeks of testing). "
                 "If qualified: regular supply would start in Q1 2025. Volume: 50 t/year.",
             ]),
            ("4. Renewal of the 2024-2026 framework contract",
             [
                 "The current contract expires on 2024-06-30. Mr Valentin proposed a 2-year extension (July 2024 — June 2026) "
                 "with an annual price revision clause and extension to the Tampere site.",
                 "Key points negotiated: a price indexation mechanism based on ICIS Chemical Prices (published "
                 "monthly), notice of termination increased to 6 months (from 3 months currently), and a supplier site "
                 "audit accepted by ChemCorp every 2 years.",
                 "Agreement in principle on the terms. Mr Valentin will send the draft contract for Nordic Resins "
                 "legal review before 30 April. Signature targeted before 2024-05-31.",
             ]),
        ],
        "opportunities": [
            ("Fumaric acid 50 t/year", "Replacing the Chinese supplier on quality", "High", "Valentin — 100 kg qualification Q2"),
            ("Tampere extension", "Propylene glycol + phthalic acid + fumaric acid", "Confirmed", "Framework contract amendment"),
            ("Speciality alkyd resins", "Ms Svensson interested in bio-based diacids", "Prospective", "2025"),
        ],
        "actions": [
            ("Mr Valentin", "Send the 2024-2026 framework contract proposal including Tampere", "2024-04-30"),
            ("Mr Osei", "Contract the storage agreement with Kemi Logistics Tampere", "2024-05-30"),
            ("Mr Valentin / Purchasing", "Order 100 kg of Bartek fumaric acid + arrange shipment to Södertälje", "2024-04-20"),
            ("Ms Durand", "Pass the IATF 16949 requirements received in May to the ChemCorp Quality department", "2024-05-15"),
        ],
        "next_contact": "Framework contract draft review: week of 2024-05-06. H2 business review: October 2024.",
    },
]

def build_meeting(meeting, out_dir):
    path = os.path.join(out_dir, f"{meeting['ref']}.pdf")
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm, topMargin=2*cm, bottomMargin=2.5*cm)
    story = []

    # Header
    hdr = Table([[
        [p(COMPANY, 11, bold=True, color='#ffffff'),
         p(f"MINUTES — {meeting['type'].upper()}", 8, color='#aaccee')],
        [p(meeting['title'], 10, bold=True, color='#ffffff'),
         p(f"Ref: {meeting['ref']}", 8, color='#aaccee', align='RIGHT')]
    ]], colWidths=[10*cm, 7*cm])
    hdr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor(BLUE)),
        ('TOPPADDING', (0,0), (-1,-1), 10), ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (0,-1), 12), ('RIGHTPADDING', (1,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(hdr)
    story.append(Spacer(1, 0.4*cm))

    # Meta
    meta = [
        ['Date', meeting['date'], 'Time', meeting['time']],
        ['Location', meeting['location'], 'Ref.', meeting['ref']],
        ['Customer', meeting['customer'], 'Type', meeting['type']],
    ]
    meta = [[Paragraph(c, ParagraphStyle('m', fontSize=9, leading=11,
             fontName='Helvetica-Bold' if i in (0, 2) else 'Helvetica')) for i, c in enumerate(row)] for row in meta]
    mt = Table(meta, colWidths=[2.5*cm, 7.5*cm, 2.5*cm, 4.5*cm])
    mt.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor(PALE)), ('BACKGROUND', (2,0), (2,-1), colors.HexColor(PALE)),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(mt)
    story.append(Spacer(1, 0.4*cm))

    # Participants
    story.append(p("ATTENDEES", 10, bold=True, color=BLUE))
    att_rows = [['Name', 'Company', 'Role']]
    for name, role in meeting['chemcorp_attendees']:
        att_rows.append([name, COMPANY, role])
    for name, role in meeting['customer_attendees']:
        att_rows.append([name, meeting['customer'], role])
    att_rows = [[Paragraph(c, ParagraphStyle('a', fontSize=9, leading=11,
                 fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                 textColor=colors.white if ri == 0 else colors.black)) for c in row]
                for ri, row in enumerate(att_rows)]
    at = Table(att_rows, colWidths=[4.5*cm, 6*cm, 6.5*cm], repeatRows=1)
    at.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(LBLUE)),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor(PALE)]),
        ('TOPPADDING', (0,0), (-1,-1), 3), ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(at)
    story.append(Spacer(1, 0.3*cm))

    # Context
    story.append(p("BACKGROUND", 10, bold=True, color=BLUE))
    story.append(p(f"<b>Customer profile:</b> {meeting['customer_profile']}", 9, color='#333333'))
    story.append(Spacer(1, 0.1*cm))
    story.append(p(f"<b>Meeting context:</b> {meeting['context']}", 9, color='#333333'))
    story.append(Spacer(1, 0.4*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.3*cm))

    # Sections
    story.append(p("PROCEEDINGS", 11, bold=True, color=BLUE))
    for sec_title, paragraphs in meeting['sections']:
        story.append(p(f"<b>{sec_title}</b>", 10, bold=False, color=LBLUE, sb=0.15))
        for para in paragraphs:
            story.append(p(para, 9, color='#222222', leading=13.5))
            story.append(Spacer(1, 0.1*cm))
        story.append(Spacer(1, 0.2*cm))

    # Page 2 — Opportunities + Actions
    story.append(PageBreak())
    story.append(p(f"Minutes {meeting['ref']} — Opportunities &amp; action plan", 11, bold=True, color=BLUE))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor(BLUE)))
    story.append(Spacer(1, 0.4*cm))

    story.append(p("IDENTIFIED OPPORTUNITIES", 10, bold=True, color=GREEN))
    opp_rows = [['Opportunity', 'Context', 'Likelihood', 'Next step']]
    for opp in meeting['opportunities']:
        opp_rows.append(list(opp))
    opp_rows = [[Paragraph(c, ParagraphStyle('o', fontSize=8.5, leading=10.5,
                 fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                 textColor=colors.white if ri == 0 else colors.black)) for c in row]
                for ri, row in enumerate(opp_rows)]
    ot = Table(opp_rows, colWidths=[4*cm, 5.5*cm, 2.5*cm, 5*cm], repeatRows=1)
    ot.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor(GREEN)),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('GRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f0faf4'), colors.white]),
        ('TOPPADDING', (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(ot)
    story.append(Spacer(1, 0.5*cm))

    story.append(p("ACTION PLAN", 10, bold=True, color=BLUE))
    act_rows = [['ChemCorp owner', 'Action', 'Due date']]
    for resp, action, date in meeting['actions']:
        act_rows.append([resp, action, date])
    act_rows = [[Paragraph(c, ParagraphStyle('ac', fontSize=9, leading=11,
                 fontName='Helvetica-Bold' if ri == 0 else 'Helvetica',
                 textColor=colors.white if ri == 0 else colors.black)) for c in row]
                for ri, row in enumerate(act_rows)]
    act_t = Table(act_rows, colWidths=[4*cm, 10.5*cm, 2.5*cm], repeatRows=1)
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

    story.append(p(f"<b>Next contact:</b> {meeting['next_contact']}", 9.5, color=BLUE))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.3, color=colors.lightgrey))
    story.append(p(f"Confidential document — for internal ChemCorp Industries use only. Ref: {meeting['ref']} | Circulation: Sales + Management.", 7.5, color='#666666'))

    doc.build(story)
    print(f"  Generated: {path}")

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(__file__), 'website', 'docs', 'customer-meeting-notes')
    os.makedirs(out, exist_ok=True)
    for m in MEETINGS:
        build_meeting(m, out)
    print(f"Done — {len(MEETINGS)} customer meeting notes generated.")
