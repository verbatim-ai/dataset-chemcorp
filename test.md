# Question & Answer set — ChemCorp Industries dataset

RAG benchmark questions covering the 7 document categories in the dataset.
Each question states the expected source so retrieval precision can be scored.

---

## Invoices (`invoices/`)

**Q1.** What is the total including VAT on invoice FC-2024-00187?
> **A.** 1,556.40 € incl. VAT (subtotal excl. VAT 1,297.00 € + VAT 20% 259.40 €).
> *Source: FC-2024-00187.pdf*

**Q2.** Which customer was invoice FC-2024-00318 addressed to, and when was it due?
> **A.** Nordic Resins AB. Invoice date: 2024-02-28, due date: 2024-03-29.
> *Source: FC-2024-00318.pdf*

**Q3.** Which products appear on invoice FC-2024-00489 addressed to Deltasolv NV?
> **A.** Pure methanol (300 L), Dichloromethane (150 L), Propylene glycol USP (500 kg), Triethylamine 99% (80 kg), plus freight charges of 275.00 €.
> *Source: FC-2024-00489.pdf*

**Q4.** Which invoice shows a credit note of €230 deducted, and what is the credit note reference?
> **A.** Invoice FC-2024-00563 (Plastex GmbH). The credit note referenced is FC-2023-00891 for €230.
> *Source: FC-2024-00563.pdf*

**Q5.** What is ChemCorp Industries' IBAN for bank transfers, and which BIC is associated with it?
> **A.** IBAN: FR76 3000 6000 0112 3456 7890 189 — BIC: BNPAFRPPXXX.
> *Source: FC-2024-00187.pdf (and every invoice)*

**Q6.** Which is the highest-value invoice including VAT among the 8 invoices in the dataset, and which customer does it belong to?
> **A.** Invoice FC-2024-00728 is the highest at 4,051.68 € incl. VAT, addressed to Nordic Resins AB.
> *Source: FC-2024-00728.pdf*

**Q7.** Which ADR classification is stated on the solvent invoices, and which tunnel code applies to acetone?
> **A.** Solvents are classified ADR class 3. Acetone (UN 1090) falls under packing group II with tunnel code D/E.
> *Source: FC-2024-00187.pdf (ADR table, page 2)*

**Q8.** How many invoices were issued to the customer Plastex GmbH in the dataset, and what are their numbers?
> **A.** Two invoices: FC-2024-00187 (2024-01-15) and FC-2024-00563 (2024-04-22).
> *Source: FC-2024-00187.pdf, FC-2024-00563.pdf*

---

## Product data sheets (`product-sheets/`)

**Q9.** What is the CAS number of acetone and what is its auto-ignition temperature?
> **A.** CAS 67-64-1. Auto-ignition temperature: 465 °C.
> *Source: FT-AK995-2024.pdf*

**Q10.** What are the explosive limits (LEL/UEL) of acetone in air?
> **A.** LEL: 2.5% vol. — UEL: 13.0% vol.
> *Source: FT-AK995-2024.pdf*

**Q11.** What is the maximum benzene specification for ChemCorp distilled toluene?
> **A.** Benzene ≤ 1 ppm (typical COA result: < 0.5 ppm).
> *Source: FC-2024-00187.pdf (technical specifications annex, page 3 — there is no toluene product data sheet in the dataset; the specification appears in the invoice annex, which is reproduced on every invoice)*

**Q12.** What is the solubility of sodium hydroxide in water at 20 °C, and why must care be taken when dissolving it?
> **A.** Solubility: 111 g/100 mL. Dissolution is strongly exothermic, creating a risk of splashing and burns.
> *Source: FT-NaOHP-2024.pdf*

**Q13.** Is USP propylene glycol subject to ADR regulations? Which food certifications does it hold?
> **A.** No, it is not subject to ADR in packages of 1,000 L or less. It is certified USP/NF, BP/EP, FCC and qualifies as food additive E1520 (FSSC 22000, ISO 22000).
> *Source: FT-PG-USP-2024.pdf*

**Q14.** What is the density at 20 °C of 96% sulfuric acid and which 3 CLP hazard statements are associated with it?
> **A.** Density: 1.835 g/mL. Hazard statements: H290 (may be corrosive to metals), H314 (causes severe skin burns and eye damage), H335 (may cause respiratory irritation).
> *Source: FT-H2SO496-2024.pdf*

**Q15.** What is the UN number and ADR class of 33% hydrochloric acid, and what is the maximum iron specification?
> **A.** UN 1789, ADR class 8, packing group II, tunnel code E. Iron (Fe) ≤ 3 ppm.
> *Source: FT-HCL33-2024.pdf*

---

## Purchase orders (`orders/`)

**Q16.** What is the total including VAT on purchase order BC-2024-0142 placed with BASF SE, and which products does it contain?
> **A.** Incl. VAT: 12,204.00 € (excl. VAT 10,170.00 €). Products: Ethylene glycol 99.9% (5 t), Technical methanol 99.9% (10 t), Diethylene glycol (3 t).
> *Source: BC-2024-0142.pdf*

**Q17.** What are the payment terms on purchase order BC-2024-0331 placed with Arkema France, and which Incoterm applies?
> **A.** Payment 30 days end of month. Incoterm: EXW Colombes (Incoterms 2020).
> *Source: BC-2024-0331.pdf*

**Q18.** Which purchase order carries a late penalty clause of 0.1% of the order value per day, and what is the context?
> **A.** BC-2024-0672 (BASF SE), placed urgently following an unexpected stock-out. The delivery date is declared firm and non-negotiable.
> *Source: BC-2024-0672.pdf*

**Q19.** Which supplier received the highest-value order in the purchase order dataset, and what is that amount?
> **A.** TotalEnergies Fluids via BC-2024-0589: 22,428.00 € incl. VAT (excl. VAT 18,690.00 €), covering ethylene glycol (8 t), methanol (15 t), DEG (5 t) and acetic anhydride (2 t).
> *Source: BC-2024-0589.pdf*

**Q20.** Which documents are mandatory for each delivery under the ChemCorp general purchasing conditions?
> **A.** Certificate of analysis (COA) per batch number with the reference analytical methods, an SDS compliant with Regulation (EU) 2020/878 (no more than 3 years old), ADR documents where applicable (transport document, instructions in writing, loader's declaration), a delivery note showing the ChemCorp order number, batch number, date of manufacture and best-before date, and a certificate of origin where required.
> *Source: BC-2024-0142.pdf (and every purchase order, technical specification page 3)*

**Q21.** On which purchase order does dimethylformamide (DMF) appear, and what particular storage precaution is stated?
> **A.** BC-2024-0445 (Brenntag SAS). DMF is classified reprotoxic category 1B; access is restricted and storage in a ventilated cabinet is mandatory. Delivery by ventilated tanker truck is required.
> *Source: BC-2024-0445.pdf*

---

## Internal meeting minutes (`internal-meeting-notes/`)

**Q22.** What is the KB index (Kauri-Butanol solvency) of formulation F-12C in the BioSolv-3 project, and what is the target?
> **A.** Formulation F-12C reaches a KB of 42; the target is 50. The gap is attributed to an insufficient limonene fraction (15% instead of the 22% target).
> *Source: CRI-RD-2024-003.pdf*

**Q23.** What budget was allocated to the BioSolv-3 project in 2024 and how is it split?
> **A.** €380k in total: €120k for analytical work and external testing, €85k for patent costs, and €175k for pilot and raw material costs.
> *Source: CRI-RD-2024-003.pdf*

**Q24.** What was the output achieved and the variance against target in January 2024?
> **A.** 847 tonnes produced against a target of 920 t, a variance of -8.0%. Solvents workshop: 312 t (target 350 t), acids 203 t (target 210 t), bases 180 t (target 185 t), specialities 152 t (target 175 t).
> *Source: CRI-PROD-2024-007.pdf*

**Q25.** Which two near misses were recorded in January 2024 and what corrective measures were decided?
> **A.** PA-2024-003: a minor leak on valve V-218 → an audit of all valves in the solvents workshop more than 3 years old (budget €22k, March-April 2024). PA-2024-004: an operator without a harness on walkway P-07 → procedure reminder, and a practical assessment added to the working-at-height training module.
> *Source: CRI-PROD-2024-007.pdf*

**Q26.** What was the supply pressure on monoethylene glycol (MEG) in January 2024, and what emergency actions were decided?
> **A.** A price rise of +18% in 3 weeks caused by a SABIC production cut and strong Asian demand. ChemCorp stock: 45 tonnes (12 days of cover). Actions: a spot order of 30 t from Brenntag (delivery 8 Feb), contact with BASF to bring forward 15 t, and a study into partially substituting DEG for MEG in 5 formulations.
> *Source: CRI-PROD-2024-007.pdf*

**Q27.** What was ChemCorp Industries' consolidated revenue in 2023 and the corresponding EBITDA margin?
> **A.** 2023 revenue (provisional): €47.2M (+6.3% vs 2022). EBITDA: €8.4M, a margin of 17.8% (below the 18.5% target).
> *Source: CRI-STRAT-2024-002.pdf*

**Q28.** How many products in the ChemCorp portfolio were classified as "dogs" in the March 2024 BCG analysis, and what decision was taken about them?
> **A.** 14 products. Executive management launched a valuation analysis with options for divestment or progressive discontinuation, assigned to Mr Valentin and Mr Bruneau for presentation in June 2024.
> *Source: CRI-STRAT-2024-002.pdf*

---

## Customer meeting minutes (`customer-meeting-notes/`)

**Q29.** What ChemCorp service rate was recorded at Plastex GmbH in 2023, and what notable delivery incident occurred?
> **A.** Service rate: 96.8% (Plastex target: 97%). Incident: a delivery delay in August 2023 (week 33, acetone) caused a 4h line stoppage at Plastex, valued at €12k of internal cost.
> *Source: CRC-PLASTEX-2024-01.pdf*

**Q30.** What late delivery penalty rate was finally negotiated with Plastex GmbH for the 2025 framework contract?
> **A.** 0.08% of the delivery value per day of delay (a compromise between ChemCorp's 0.05% proposal and Plastex's 0.10% request).
> *Source: CRC-PLASTEX-2024-01.pdf*

**Q31.** Which test result blocked validation of the EcoSolv-D4 formulation at Solvalor, and what solution was proposed?
> **A.** The formulation caused whitening on ABS plastics, with all other criteria compliant (KB 7.2 > 7.0, drying 8 min < 10 min). ChemCorp proposed an EcoSolv-D4-mod reformulation with 5% less aromatic co-solvent, delivering 500 mL for re-testing within 3 weeks.
> *Source: CRC-SOLVALOR-2024-03.pdf*

**Q32.** What commercial risk did ChemCorp face from Solvalor's "low VOC" transition, and how was it quantified?
> **A.** Solvalor must cut its methanol purchases by 40% over 3 years (-240 t/year). Combined with the substitution of ethyl acetate, the revenue risk for ChemCorp is estimated at approximately €200k/year if no alternative is offered.
> *Source: CRC-SOLVALOR-2024-03.pdf*

**Q33.** What was the on-time delivery rate to Nordic Resins AB in H1 2024, and how did it evolve?
> **A.** 100% on-time across 14 deliveries in H1 2024, a significant improvement on 92% in H2 2023.
> *Source: CRC-NORDIC-2024-05.pdf*

**Q34.** Which new product does Nordic Resins AB want to source from ChemCorp for its Tampere site, what volume is targeted, and what is the price difference against the current supplier?
> **A.** Fumaric acid, 50 t/year. The current Chinese supplier (CNHC Chemical) charges approximately €750/t; ChemCorp offers €920/t via Bartek Ingredients, with higher quality (purity above 99.5%, systematic COA). Recurring quality problems at the Chinese supplier justify the price differential.
> *Source: CRC-NORDIC-2024-05.pdf*

---

## Objectives and strategy (`business-goals/`)

**Q35.** What revenue is ChemCorp targeting for 2027, and what share should be bio-based?
> **A.** 2027 revenue target: €62M (+32% vs 2023), with a target EBITDA margin of 22%. The bio-based share of revenue must reach 25% by 2027 (against below 1% in 2023).
> *Source: OBJ-STRAT-2024.pdf*

**Q36.** What NPS (Net Promoter Score) target was set for 2024, and what was the 2023 score?
> **A.** 2024 target: NPS above 50, with quarterly surveys and corrective actions within 30 days. 2023 score: 38.
> *Source: OBJ-STRAT-2024.pdf*

**Q37.** What are the 5 pillars of the ChemCorp Green Chemistry roadmap 2024-2030?
> **A.** (1) Bio-based products (the BioSolv range), (2) Clean processes (energy -40%, water -30% by 2030), (3) Circular economy (used solvent regeneration service from 2026), (4) Sustainable supply chain (100% of key suppliers CSR-assessed by 2026), (5) Carbon transparency (operational neutrality on scopes 1+2 by 2030).
> *Source: OBJ-VERT-2024-2030.pdf*

**Q38.** What is the total budget of the Green Chemistry roadmap over 2024-2030, and how is it funded?
> **A.** €14.2M over 7 years: 40% equity, 25% BPI green debt, 20% grants (ANR, ADEME, Horizon Europe), 15% research tax credit.
> *Source: OBJ-VERT-2024-2030.pdf*

**Q39.** What energy saving is expected from the GreenCat-Est programme, what ANR funding is planned, and with which catalytic technology?
> **A.** Estimated energy saving of -23% on esterification reactions. ANR funding: €180k. Technology: modified H-ZSM-5 zeolite in heterogeneous catalysis (replacing the current homogeneous acid catalyst).
> *Source: OBJ-VERT-2024-2030.pdf*

---

## Analytical datasets (`datasets/`)

**Q40.** What is the mean GC purity of acetone 99.5% measured during 2024 in the quality control dataset, and which analytical method is used?
> **A.** Mean purity: 99.65% (observed range: 99.52–99.82%, standard deviation 0.08%). Method: GC-FID chromatography, Agilent DB-624 column, external calibration, in-house method QC-GC-001 based on ISO 11013.
> *Source: DS-QC-SOL-2024.pdf*

**Q41.** How many batches were placed under review in the solvent quality control dataset, and what happened to them?
> **A.** 3 batches were placed under review. All were successfully reprocessed, and no definitively non-conforming batch was released to a customer. (The dataset states this in its conclusions; it does not list the individual batch identifiers.)
> *Source: DS-QC-SOL-2024.pdf*

**Q42.** Which reactor shows the best mean yield in the production dataset, and what is that value?
> **A.** Reactor R-102 (methanol) shows the best mean yield: 91.0% (range 85.2–95.6%, standard deviation 2.1%).
> *Source: DS-PROD-BATCH-2024.pdf*

**Q43.** What is the mean duration of a production batch across all 45 batches in the dataset?
> **A.** 6.5 hours on average (range 4.2–9.1 h, standard deviation 0.8 h).
> *Source: DS-PROD-BATCH-2024.pdf*

**Q44.** What was the site's total electricity consumption in 2023, and what is the 2024 target?
> **A.** 8,102 MWh in 2023. 2024 target: 7,454 MWh (-8%). 2027 target: 6,320 MWh (-22% vs 2023).
> *Source: DS-ENERGIE-2024.pdf*

**Q45.** What CO₂ emissions formula is used in the energy dataset, and which emission factors are applied?
> **A.** CO₂ (t) = Electricity (MWh) × 0.0567 + Gas (MWh NCV) × 0.185 + Steam (t) × 0.070. Factor sources: ADEME 2024 for French grid electricity and natural gas; the steam factor is derived from the in-house gas boiler.
> *Source: DS-ENERGIE-2024.pdf*

---

## Cross-document questions (cross-document retrieval)

**Q46.** In January 2024 the BioSolv-3 project planned a PCT patent filing for the end of June 2024. Does this date also appear in the strategic plan, and which firm was engaged?
> **A.** Yes. The R&D meeting of 18 January 2024 approved the milestone "PCT patent filing on 30 June 2024" (Mr Ferretti coordinating). The strategic plan OBJ-STRAT-2024 confirms the objective of 2 patents filed in 2024 (BioSolv-3 PCT + GreenCat FR). The firm engaged is Lebret & Associés.
> *Cross source: CRI-RD-2024-003.pdf + OBJ-STRAT-2024.pdf*

**Q47.** Methanol appears both as a product sold and as a raw material purchased. In which invoice and on what commercial terms is it sold? In which purchase order and from which supplier is it bought?
> **A.** Invoice: FC-2024-00489 (Deltasolv NV), 300 L of Pure methanol (ref. ME-PUR) at €1.15/L = €345.00. Purchase order: BC-2024-0589 (TotalEnergies Fluids), 15 t of Technical methanol 99.9% (ref. MeOH-T) at €420/t = €6,300.00. Methanol and ethyl acetate are the only two chemicals present in both the sales catalogue and the purchasing catalogue, and they carry different reference codes in each.
> *Cross source: FC-2024-00489.pdf + BC-2024-0589.pdf*

**Q48.** The production meeting of 1 February 2024 reports an FPY of 94.1%. The 2024 strategic plan sets an FPY target for the year. What is that target and what gap does this represent against the January actual?
> **A.** The 2024 FPY target is 97% (OBJ-STRAT-2024). The January actual (94.1%) shows a gap of -2.9 points against the annual target, with identified causes: 3 rejected batches (acetone, HCl, glycerol) and reduced throughput in the solvents workshop.
> *Cross source: CRI-PROD-2024-007.pdf + OBJ-STRAT-2024.pdf*

**Q49.** Nordic Resins AB appears as a customer both in the invoices and in the sales meeting minutes. How consistent are the products invoiced with those discussed in the customer meeting?
> **A.** Invoices FC-2024-00318 and FC-2024-00728 deliver mineral acids (HCl, H₂SO₄, HNO₃), xylenes, NaOH, DCM, propylene glycol and triethylamine to Nordic Resins. The meeting CRC-NORDIC-2024-05 instead cites annual purchases of "phthalic acid (300 t), maleic anhydride (200 t) and propylene glycol (400 t)" — volumes well above the invoice lines in the dataset, which is consistent: propylene glycol is common to both, confirming its place in the framework contract.
> *Cross source: FC-2024-00318.pdf + FC-2024-00728.pdf + CRC-NORDIC-2024-05.pdf*

**Q50.** The 33% hydrochloric acid data sheet lists metal pickling applications. Is this application reflected in an order or invoice in the dataset?
> **A.** Invoice FC-2024-00641 (Solvalor S.A.S.) includes 400 kg of 33% hydrochloric acid (ref. HCL-33 at €0.54/kg). Data sheet FT-HCL33-2024 explicitly cites "acid pickling of steel before galvanising or welding" and "regeneration of cationic ion-exchange resins" as typical applications, consistent with Solvalor's profile as a formulator.
> *Cross source: FC-2024-00641.pdf + FT-HCL33-2024.pdf*

---

*Total: 50 questions covering 7 document categories and 5 cross-source questions.*
*Dataset: 30 PDFs, 104 pages — ChemCorp Industries S.A. (fictional, for RAG benchmarking only)*
