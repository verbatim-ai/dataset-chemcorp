#!/usr/bin/env python3
"""Generate the static ChemCorp Industries website that hosts and documents the dataset.

Scans website/docs/ for the generated PDFs and parses test.md, so the site cannot
drift from the corpus. Output is plain static HTML — no build step; the only
external asset is the Verbatim AI chatbot widget, loaded from the Verbatim CDN
and configured in website/assets/verbatim-widget.js.
"""
import os, re, html, pathlib

ROOT = pathlib.Path(__file__).parent
SITE = ROOT / 'website'
DOCS = SITE / 'docs'
ASSETS = SITE / 'assets'
REPO = "https://github.com/verbatim-ai/dataset-chemcorp/tree/main"

# --- corpus description -----------------------------------------------------

CATEGORIES = [
    ("invoices", "Invoices", "FC-2024-NNNNN",
     "Sales invoices issued by ChemCorp to its customers. Each runs 4–5 pages: line items and "
     "20% VAT, payment details, delivered-batch traceability, ADR dangerous-goods classification, "
     "the general terms of sale, and a technical specification annex."),
    ("orders", "Purchase orders", "BC-2024-NNNN",
     "Orders placed by ChemCorp with its raw material suppliers. Three pages: line items priced "
     "per tonne, Incoterms and payment terms, the general purchasing conditions, and a technical "
     "specification the supplier must meet."),
    ("product-sheets", "Product data sheets", "FT-<REF>-2024",
     "Nine-section technical sheets: CAS and EC identity, physico-chemical properties, analytical "
     "specifications, CLP/GHS hazard and precautionary statements, storage, transport "
     "classification, and detailed application notes."),
    ("datasets", "Analytical datasets", "DS-<DOMAIN>-2024",
     "Tabular measurement data — solvent quality control, production batch history, and energy "
     "and environmental consumption — each with raw rows, a statistical summary and written "
     "conclusions."),
    ("internal-meeting-notes", "Internal meeting minutes", "CRI-<DEPT>-2024-NNN",
     "Minutes of R&amp;D, production and strategy meetings: attendees, agenda, narrative "
     "proceedings and a dated action plan."),
    ("customer-meeting-notes", "Customer meeting minutes", "CRC-<CLIENT>-2024-NN",
     "Minutes of customer visits and business reviews: account profile, background, proceedings, "
     "identified commercial opportunities and actions."),
    ("business-goals", "Business goals &amp; strategy", "OBJ-<THEME>-<YEARS>",
     "Confidential strategy documents: the 2024 objectives and performance plan, and the "
     "2024–2030 green-chemistry roadmap, each with a risk analysis and governance section."),
]

SEGMENTS = [("Industrial solvents", 38), ("Inorganic acids &amp; bases", 28),
            ("Chemical specialities", 21), ("Trading", 13)]

PEOPLE = [
    ("François Lemercier", "Chief Executive Officer"),
    ("Hélène Marchand", "Operations Director (COO)"),
    ("Dr. Martine Chabrol", "R&amp;D Director (CTO)"),
    ("Thierry Bruneau", "Finance Director (CFO)"),
    ("Pierre Valentin", "Sales Director"),
    ("Bertrand Vidal", "Production Manager"),
    ("Ingrid Hoffmann", "QHSE &amp; Regulatory"),
    ("Alain Rousset", "Purchasing Manager"),
    ("Samuel Osei", "International Logistics"),
    ("Antoine Ferretti", "R&amp;D Project Manager"),
]

CUSTOMERS = [
    ("Plastex GmbH", "Munich, Germany", "Technical plastic parts (PC, ABS, POM) for automotive and electronics"),
    ("Solvalor S.A.S.", "Harfleur, France", "Industrial cleaning solvents and degreasers"),
    ("Nordic Resins AB", "Södertälje, Sweden", "Alkyd and unsaturated polyester resins for paints and coatings"),
    ("Iberchem S.L.", "Sevilla, Spain", "Speciality chemical formulation"),
    ("Deltasolv NV", "Antwerpen, Belgium", "Solvent distribution"),
]

SUPPLIERS = [
    ("BASF SE", "Ludwigshafen, Germany", "10 working days"),
    ("Solvay S.A.", "Brussels, Belgium", "15 working days"),
    ("Arkema France S.A.S.", "Colombes, France", "8 working days"),
    ("Brenntag SAS", "Limonest, France", "5 working days"),
    ("TotalEnergies Fluids", "Paris La Défense, France", "12 working days"),
]

DISCLAIMER_SHORT = (
    "ChemCorp Industries S.A. is a <strong>fictional company</strong>. Every document, figure, "
    "person and transaction on this site is synthetic, created solely to benchmark "
    "retrieval-augmented generation systems."
)

# --- helpers ----------------------------------------------------------------

def page_count(pdf: pathlib.Path) -> int:
    m = re.search(rb'/Count (\d+)', pdf.read_bytes())
    return int(m.group(1)) if m else 0

def scan_docs():
    """Return {category_slug: [(filename, pages, kb), ...]} from the generated corpus."""
    out = {}
    for slug, *_ in CATEGORIES:
        d = DOCS / slug
        files = sorted(d.glob('*.pdf')) if d.is_dir() else []
        out[slug] = [(f.name, page_count(f), round(f.stat().st_size / 1024)) for f in files]
    return out

def parse_benchmark():
    """Parse test.md into [(section_title, [(qid, question, answer, source), ...]), ...]."""
    md = (ROOT / 'test.md').read_text()
    sections, cur = [], None
    for block in md.split('\n## ')[1:]:
        title, _, body = block.partition('\n')
        title = title.strip()
        items = []
        for m in re.finditer(
            r'\*\*(Q\d+)\.\*\*\s*(.+?)\n> \*\*A\.\*\*\s*(.+?)\n> \*(.+?)\*', body, re.S):
            qid, q, a, src = (x.strip().replace('\n', ' ') for x in m.groups())
            items.append((qid, q, a, src))
        if items:
            sections.append((title, items))
    return sections

def md_inline(text: str) -> str:
    """Minimal inline markdown → HTML for benchmark text already escaped upstream."""
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    text = re.sub(r'"([^"]+)"', r'&ldquo;\1&rdquo;', text)
    return text

def page(title, active, body, description):
    nav_items = [("index.html", "Overview"), ("company.html", "The company"),
                 ("dataset.html", "Dataset"), ("benchmark.html", "Benchmark")]
    nav_links = []
    for href, label in nav_items:
        cls = ' class="is-active"' if href == active else ''
        nav_links.append('      <a href="%s"%s>%s</a>' % (href, cls, label))
    nav = "\n".join(nav_links)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — ChemCorp Industries (fictional)</title>
<meta name="description" content="{description}">
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="googlebot" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="bingbot" content="noindex, nofollow, noarchive, nosnippet">
<link rel="stylesheet" href="assets/site.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='13'>&#127883;</text></svg>">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">CC</span>
      <span class="brand-text"><strong>ChemCorp Industries</strong><span class="brand-sub">Synthetic RAG benchmark corpus</span></span>
    </a>
    <nav aria-label="Primary">
{nav}
    </nav>
  </div>
</header>

<div class="disclaimer" role="note">
  <div class="wrap">
    <span class="disclaimer-tag">Fictional</span>
    <p>{DISCLAIMER_SHORT}</p>
  </div>
</div>

<main id="main">
{body}
</main>

<footer class="site-foot">
  <div class="wrap foot-grid">
    <div>
      <h2>ChemCorp Industries S.A.</h2>
      <p class="muted">A fictional chemical distributor. This entire site and every document it
      hosts is synthetic material built to benchmark retrieval-augmented generation systems.
      No real company, person, transaction, price or certification is represented. Company names
      that exist in reality (BASF, Solvay, Arkema, Brenntag, TotalEnergies) appear only as
      placeholder counterparties; nothing stated about them is factual.</p>
    </div>
    <div>
      <h2>Corpus</h2>
      <ul class="plain">
        <li><a href="dataset.html">Browse all 30 documents</a></li>
        <li><a href="benchmark.html">50-question QA benchmark</a></li>
        <li><a href="{REPO}">Source repository</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap foot-bar"><p class="muted">Generated by <code>gen_website.py</code> — static output, no analytics.
  The assistant in the corner is the <a href="https://www.verbatim-ai.com">Verbatim AI</a> widget, answering from this corpus.</p></div>
</footer>

<!-- Verbatim AI chatbot widget — configure in assets/verbatim-widget.js -->
<div id="verbatim-chatbot"></div>
<script src="https://cdn.verbatim-ai.com/widget/chatbot/v1/chatbot-widget.iife.js"></script>
<script src="assets/verbatim-widget.js"></script>
</body>
</html>
"""

# --- stat tiles & chart -----------------------------------------------------

def stats(items):
    tiles = "\n".join(
        f'    <div class="stat"><div class="stat-value">{v}</div>'
        f'<div class="stat-label">{l}</div>'
        f'<div class="stat-note">{n}</div></div>'
        for v, l, n in items)
    return f'  <div class="stat-row">\n{tiles}\n  </div>'

def segment_chart():
    """Single-measure horizontal bars: one hue, direct labels, recessive axis."""
    rows, y, step, bar_h = [], 0, 46, 18
    maxv = max(v for _, v in SEGMENTS)
    plot_w = 560
    for label, val in SEGMENTS:
        w = round(val / maxv * plot_w, 1)
        rows.append(
            f'    <g class="bar-g">'
            f'<title>{label}: {val}% of 2023 revenue</title>'
            f'<text class="bar-label" x="0" y="{y + 12}">{label}</text>'
            f'<rect class="bar" x="0" y="{y + 20}" width="{w}" height="{bar_h}" rx="4"/>'
            f'<text class="bar-value" x="{w + 8}" y="{y + 20 + bar_h - 4}">{val}%</text>'
            f'</g>')
        y += step
    height = y + 4
    return f"""<figure class="chart">
  <figcaption>
    <h3>Revenue by segment, 2023</h3>
    <p class="muted">Share of €47.2M total. Chemical specialities carry margins above 30% and are
    the stated growth priority.</p>
  </figcaption>
  <svg viewBox="0 0 720 {height}" width="100%" height="{height}"
       preserveAspectRatio="xMinYMin meet" role="img"
       aria-label="Horizontal bar chart of 2023 revenue share by segment: industrial solvents 38 percent, inorganic acids and bases 28 percent, chemical specialities 21 percent, trading 13 percent.">
{chr(10).join(rows)}
  </svg>
  <table class="visually-hidden">
    <caption>Revenue by segment, 2023</caption>
    <thead><tr><th>Segment</th><th>Share of revenue</th></tr></thead>
    <tbody>{"".join(f"<tr><td>{l}</td><td>{v}%</td></tr>" for l, v in SEGMENTS)}</tbody>
  </table>
</figure>"""

# --- pages ------------------------------------------------------------------

def build_index(docs):
    total_docs = sum(len(v) for v in docs.values())
    total_pages = sum(p for v in docs.values() for _, p, _ in v)
    return page("Overview", "index.html", f"""
<section class="hero">
  <div class="wrap">
    <p class="eyebrow">Synthetic document corpus</p>
    <h1>A complete company paper trail, invented on purpose.</h1>
    <p class="lede">ChemCorp Industries S.A. is a fictional chemical distributor in Villeurbanne,
    France. This site publishes its entire document universe — invoices, purchase orders, product
    data sheets, meeting minutes, analytical datasets and strategy papers — as a public benchmark
    for retrieval-augmented generation systems.</p>
    <p class="cta-row">
      <a class="btn btn-primary" href="dataset.html">Browse the {total_docs} documents</a>
      <a class="btn" href="benchmark.html">See the 50-question benchmark</a>
    </p>
  </div>
</section>

<section class="wrap band">
  <h2>The corpus</h2>
{stats([(str(total_docs), "PDF documents", "across 7 categories"),
        (str(total_pages), "pages", "dense, with repeated boilerplate"),
        ("50", "benchmark questions", "5 of them cross-document"),
        ("100%", "verified ground truth", "every answer checked against its PDF")])}
</section>

<section class="wrap band">
  <h2>What the company does</h2>
  <div class="prose">
    <p>ChemCorp buys bulk chemical raw materials by the tonne, processes and repackages them, and
    sells solvents, acids, bases and speciality chemicals by the litre and kilogram to industrial
    formulators across Western Europe. It runs production at Villeurbanne and Roussillon, ships
    through the Lyon-Est chemical terminal, and holds a safety stock at Limonest.</p>
    <p>The company is certified to ISO 9001:2015 and ISO 14001:2015 and runs a COFRAC-accredited
    laboratory (No. 1-5421). Its stated ambition is to become the leading supplier of bio-based,
    low-impact chemical specialities in Southern and Western Europe — a transition documented
    across the strategy papers, R&amp;D minutes and customer meetings in this corpus.</p>
  </div>
</section>

<section class="wrap band">
  <h2>2023 performance</h2>
{stats([("€47.2M", "revenue", "+6.3% against 2022"),
        ("€8.4M", "EBITDA", "17.8% margin, against an 18.5% target"),
        ("€4.1M", "net income", "+2.8% against 2022"),
        ("1.4×", "debt / EBITDA", "target below 2×")])}
  {segment_chart()}
</section>

<section class="wrap band">
  <h2>Why this exists</h2>
  <div class="prose">
    <p>Real corporate corpora cannot be published — they carry commercial and personal data. A
    synthetic one can, and it can be built to be <em>hard</em> in the ways that matter for
    retrieval: near-identical boilerplate repeated across documents of the same type, facts that
    only resolve by combining two sources, deliberately inconsistent batch numbering, and two
    product catalogues that overlap on exactly two chemicals under different reference codes.</p>
    <p>Every document is produced by a committed Python generator, so the corpus is reproducible
    and every expected answer can be traced to the line of code that emitted it.</p>
  </div>
  <p class="cta-row"><a class="btn" href="{REPO}">View the generators on GitHub</a></p>
</section>
""", "A fictional chemical distributor whose complete document set is published as a public RAG benchmark corpus.")

def build_company(docs):
    people = "".join(f"<tr><td>{n}</td><td>{r}</td></tr>" for n, r in PEOPLE)
    customers = "".join(f"<tr><td><strong>{n}</strong></td><td>{loc}</td><td>{d}</td></tr>"
                        for n, loc, d in CUSTOMERS)
    suppliers = "".join(f"<tr><td><strong>{n}</strong></td><td>{loc}</td><td>{lead}</td></tr>"
                        for n, loc, lead in SUPPLIERS)
    return page("The company", "company.html", f"""
<section class="wrap band">
  <p class="eyebrow">The company</p>
  <h1>ChemCorp Industries S.A.</h1>
  <p class="lede">Everything on this page is drawn from the documents in the corpus. It is the
  world the benchmark questions are asked about.</p>
</section>

<section class="wrap band">
  <h2>Identity</h2>
  <dl class="factgrid">
    <div><dt>Registered name</dt><dd>ChemCorp Industries S.A.</dd></div>
    <div><dt>Head office</dt><dd>14 Rue des Réactifs, 69100 Villeurbanne, France</dd></div>
    <div><dt>VAT number</dt><dd><code>FR 42 387 542 891</code></dd></div>
    <div><dt>Certifications</dt><dd>ISO 9001:2015, ISO 14001:2015</dd></div>
    <div><dt>Laboratory</dt><dd>COFRAC-accredited, No. 1-5421</dd></div>
    <div><dt>Quality system</dt><dd>LIMS <code>QC-TRACK v4.2</code></dd></div>
  </dl>
  <p class="muted small">There is deliberately no SIRET, RCS entry or share capital anywhere in the
  corpus — the identity is intentionally incomplete so it can never be mistaken for a real filing.
  Bank details appear on the invoices and are equally fictional.</p>
</section>

<section class="wrap band">
  <h2>Sites</h2>
  <div class="cards">
    <div class="card"><h3>Villeurbanne</h3><p>Head office, laboratory and warehouses A, B and C.
    Production workshops for solvents, acids, bases and specialities.</p></div>
    <div class="card"><h3>Roussillon</h3><p>Secondary production site, Zone A building 12.</p></div>
    <div class="card"><h3>Lyon-Est terminal</h3><p>Chemical terminal, bay 7 — bulk tanker
    reception and dispatch.</p></div>
    <div class="card"><h3>Limonest</h3><p>Depot holding the permanent safety stock that backs
    48-hour urgent deliveries.</p></div>
  </div>
</section>

<section class="wrap band">
  <h2>Who works there</h2>
  <p class="muted">The same cast recurs consistently across meeting minutes and strategy papers,
  which is what makes people-based retrieval questions answerable.</p>
  <table class="data"><thead><tr><th>Name</th><th>Role</th></tr></thead><tbody>{people}</tbody></table>
</section>

<section class="wrap band">
  <h2>Two catalogues</h2>
  <div class="prose">
    <p>ChemCorp <strong>sells</strong> 18 finished products priced per litre or kilogram, and
    <strong>buys</strong> 15 raw materials priced per tonne. The two catalogues are almost
    disjoint: only methanol and ethyl acetate appear in both, and they carry different reference
    codes on each side (<code>ME-PUR</code> vs <code>MeOH-T</code>, <code>EA-99</code> vs
    <code>EtOAc-T</code>). No query can join an invoice line to a purchase-order line by reference
    — which is exactly the trap the cross-document questions probe.</p>
  </div>
  <div class="cards two">
    <div class="card">
      <h3>Sold — 18 SKUs</h3>
      <p class="muted small">Priced in €/L and €/kg. Five have a published data sheet.</p>
      <p class="chips">
        <span class="chip">AK-995 acetone</span><span class="chip">TL-DIS toluene</span>
        <span class="chip">ET-96D ethanol</span><span class="chip">HCL-33 hydrochloric acid</span>
        <span class="chip">NaOH-P sodium hydroxide</span><span class="chip">ME-PUR methanol</span>
        <span class="chip">IPA-99 isopropanol</span><span class="chip">H2SO4-96 sulfuric acid</span>
        <span class="chip">DCM-TEC dichloromethane</span><span class="chip">EA-99 ethyl acetate</span>
        <span class="chip">NaCl-A sodium chloride</span><span class="chip">H2O2-30 hydrogen peroxide</span>
        <span class="chip">NH3-25 ammonia</span><span class="chip">GLY-USP glycerol</span>
        <span class="chip">HNO3-65 nitric acid</span><span class="chip">XYL-MIX xylenes</span>
        <span class="chip">PG-USP propylene glycol</span><span class="chip">TEA-99 triethylamine</span>
      </p>
    </div>
    <div class="card">
      <h3>Bought — 15 raw materials</h3>
      <p class="muted small">Priced in €/tonne, from five suppliers.</p>
      <p class="chips">
        <span class="chip">EG-999P ethylene glycol</span><span class="chip">PO-99 propylene oxide</span>
        <span class="chip">MAH-PAS maleic anhydride</span><span class="chip">MeOH-T methanol</span>
        <span class="chip">AA-GLA acrylic acid</span><span class="chip">nBA-99 butyl acrylate</span>
        <span class="chip">STY-INH styrene</span><span class="chip">AcOH-G acetic acid</span>
        <span class="chip">DEG-99 diethylene glycol</span><span class="chip">MEK-99 MEK</span>
        <span class="chip">CHCl3-S chloroform</span><span class="chip">AcO-99 acetic anhydride</span>
        <span class="chip">CyHex-T cyclohexane</span><span class="chip">DMF-99 DMF</span>
        <span class="chip">EtOAc-T ethyl acetate</span>
      </p>
    </div>
  </div>
</section>

<section class="wrap band">
  <h2>Customers</h2>
  <table class="data"><thead><tr><th>Company</th><th>Location</th><th>Business</th></tr></thead>
  <tbody>{customers}</tbody></table>
  <p class="muted small">Plastex, Solvalor and Nordic Resins appear in both invoices and meeting
  minutes; Iberchem and Deltasolv appear in invoices only.</p>
</section>

<section class="wrap band">
  <h2>Suppliers</h2>
  <table class="data"><thead><tr><th>Company</th><th>Location</th><th>Standard lead time</th></tr></thead>
  <tbody>{suppliers}</tbody></table>
  <p class="muted small">Real company names used as placeholder counterparties. Nothing stated
  about them in this corpus is factual.</p>
</section>

<section class="wrap band">
  <h2>Where the company says it is going</h2>
  <div class="cards">
    <div class="card"><h3>2027 targets</h3><p>Revenue €62M (+32% on 2023), EBITDA margin 22%,
    bio-based products at 25% of revenue against below 1% in 2023.</p></div>
    <div class="card"><h3>BioSolv</h3><p>Bio-based solvents from biomass. BioSolv-3 reached a
    Kauri-Butanol value of 42 against a target of 50; commercial launch planned for Q3 2024.</p></div>
    <div class="card"><h3>GreenCat</h3><p>Reusable heterogeneous catalysts. GreenCat-Est uses a
    modified H-ZSM-5 zeolite for an estimated 23% energy saving on esterification.</p></div>
    <div class="card"><h3>Green roadmap</h3><p>€14.2M over 2024–2030 across five pillars, funded
    40% from equity, 25% green debt, 20% grants and 15% research tax credit.</p></div>
  </div>
</section>
""", "The fictional company behind the benchmark corpus: identity, sites, people, catalogues, customers and strategy.")

def build_dataset(docs):
    total_docs = sum(len(v) for v in docs.values())
    total_pages = sum(p for v in docs.values() for _, p, _ in v)
    blocks = []
    for slug, name, pattern, desc in CATEGORIES:
        files = docs[slug]
        pages = sum(p for _, p, _ in files)
        rows = "".join(
            f'<tr><td><a href="docs/{slug}/{fn}">{fn}</a></td>'
            f'<td class="num">{p}</td><td class="num">{kb} KB</td></tr>'
            for fn, p, kb in files)
        blocks.append(f"""
  <section class="doccat" id="{slug}">
    <div class="doccat-head">
      <h3>{name}</h3>
      <p class="muted">{len(files)} documents · {pages} pages · reference pattern <code>{pattern}</code></p>
      <p>{desc}</p>
    </div>
    <table class="data docs">
      <thead><tr><th>File</th><th class="num">Pages</th><th class="num">Size</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </section>""")
    toc = "".join(f'<a class="chip" href="#{slug}">{name} ({len(docs[slug])})</a>'
                  for slug, name, _, _ in CATEGORIES)
    return page("Dataset", "dataset.html", f"""
<section class="wrap band">
  <p class="eyebrow">Dataset</p>
  <h1>All {total_docs} documents</h1>
  <p class="lede">The complete corpus, free to download and use. Every file is generated by a
  committed Python script and served here as a plain PDF — no login, no API, no rate limit.</p>
  <p class="chips">{toc}</p>
</section>

<section class="wrap band">
{stats([(str(total_docs), "documents", "7 categories"),
        (str(total_pages), "pages", "A4, text-based PDFs"),
        ("English", "language", "EUR amounts, ISO dates"),
        ("Reproducible", "generation", "seeded, deterministic")])}
</section>

<section class="wrap band">
  <h2>Conventions</h2>
  <div class="prose">
    <p>All content is in English. Amounts are in euros with English number formatting
    (<code>1,556.40</code>), VAT is a flat 20%, and dates are ISO <code>YYYY-MM-DD</code> in
    metadata and tables, spelled out in prose. Reference codes keep French-derived prefixes —
    <code>FC</code> facture, <code>BC</code> bon de commande, <code>FT</code> fiche technique,
    <code>CRI</code>/<code>CRC</code> compte rendu interne/client — because they are identifiers
    that benchmark questions cite verbatim.</p>
    <p>Business documents span January to June 2024; the analytical datasets cover all twelve
    months of 2024; strategy documents look ahead to 2027 and 2030.</p>
  </div>
</section>

<section class="wrap band">
  <h2>How the documents connect</h2>
  <div class="prose">
    <p>There are no foreign keys. Every link between documents is semantic, which is the point:</p>
    <ul>
      <li><strong>Product reference → data sheet.</strong> <code>AK-995</code> resolves to
      <code>FT-AK995-2024</code>, and likewise for <code>NaOH-P</code>, <code>H2SO4-96</code>,
      <code>HCL-33</code> and <code>PG-USP</code>. Only 5 of the 18 sold products have a sheet.</li>
      <li><strong>Customer name</strong> joins invoices to customer meeting minutes.</li>
      <li><strong>Supplier name</strong> joins purchase orders to internal minutes.</li>
      <li><strong>KPI values</strong> join minutes to strategy papers to datasets — first-pass
      yield of 94.1% actual against a 97% target, for instance.</li>
      <li><strong>No invoice cites an order number and no order cites an invoice.</strong> Sales
      and purchasing are separate universes by design.</li>
    </ul>
    <p>Batch numbering is intentionally inconsistent across document types, so there is no single
    registry to resolve against.</p>
  </div>
</section>

<section class="wrap band docs-listing">
  <h2>Browse by category</h2>
{"".join(blocks)}
</section>

<section class="wrap band">
  <h2>Regenerating the corpus</h2>
  <div class="prose">
    <p>Clone the repository and run <code>./build.sh</code>. It creates a virtualenv, installs
    reportlab and runs all seven document generators plus this site. Output lands in
    <code>website/docs/</code>. Six generators are fully deterministic; the analytical datasets use
    <code>random.seed(42)</code>, so a complete run reproduces identical values.</p>
  </div>
  <p class="cta-row"><a class="btn btn-primary" href="{REPO}">Source repository</a></p>
</section>
""", f"All {total_docs} documents of the ChemCorp synthetic corpus, free to download for RAG benchmarking.")

def build_benchmark(docs):
    sections = parse_benchmark()
    total = sum(len(items) for _, items in sections)
    blocks = []
    for title, items in sections:
        qs = "".join(f"""
      <li class="qa">
        <p class="q"><span class="qid">{qid}</span>{md_inline(q)}</p>
        <p class="a">{md_inline(a)}</p>
        <p class="src">{md_inline(src)}</p>
      </li>""" for qid, q, a, src in items)
        blocks.append(f"""
  <section class="qgroup">
    <h3>{title}</h3>
    <ol class="qa-list">{qs}</ol>
  </section>""")
    return page("Benchmark", "benchmark.html", f"""
<section class="wrap band">
  <p class="eyebrow">Benchmark</p>
  <h1>{total} questions with verified answers</h1>
  <p class="lede">Each question names the document its answer should be retrieved from, so
  retrieval precision and answer accuracy can be scored separately. Every ground-truth string below
  has been checked to appear in the PDF it cites.</p>
</section>

<section class="wrap band">
  <h2>Scoring notes</h2>
  <div class="prose">
    <ul>
      <li><strong>Normalise numbers before comparing.</strong> Answers use English formatting
      (<code>1,556.40</code>). A system that reports <code>1556.40</code> is correct.</li>
      <li><strong>The last five questions are cross-document</strong> — each needs two or more
      sources combined, and a single-passage retriever will fail them even with perfect ranking.</li>
      <li><strong>Some questions probe absence.</strong> There is no toluene data sheet, and the
      quality-control dataset does not list individual batch identifiers. Confabulating a source is
      the failure mode being measured.</li>
    </ul>
  </div>
</section>

<section class="wrap band">
{"".join(blocks)}
</section>
""", f"{total} benchmark questions with verified answers and source attribution for the ChemCorp corpus.")

# --- stylesheet -------------------------------------------------------------

CSS = """/* ChemCorp Industries — static site styles. Generated by gen_website.py. */
:root {
  color-scheme: light;
  --plane:      #f9f9f7;
  --surface:    #fcfcfb;
  --ink:        #0b0b0b;
  --ink-2:      #52514e;
  --muted:      #6d6b66;
  --rule:       #e1e0d9;
  --ring:       rgba(11,11,11,0.10);
  --accent:     #1c5cab;
  --accent-ink: #ffffff;
  --series-1:   #2a78d6;
  --tag-bg:     #fdf1e3;
  --tag-ink:    #8a4b12;
  --tag-rule:   #eccfa8;
  --radius:     10px;
  --wrap:       72rem;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --plane:      #0d0d0d;
    --surface:    #1a1a19;
    --ink:        #ffffff;
    --ink-2:      #c3c2b7;
    --muted:      #93918a;
    --rule:       #2c2c2a;
    --ring:       rgba(255,255,255,0.12);
    --accent:     #6da7ec;
    --accent-ink: #0d0d0d;
    --series-1:   #3987e5;
    --tag-bg:     #2a2118;
    --tag-ink:    #e8bd85;
    --tag-rule:   #5a4529;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --plane:      #0d0d0d;
  --surface:    #1a1a19;
  --ink:        #ffffff;
  --ink-2:      #c3c2b7;
  --muted:      #93918a;
  --rule:       #2c2c2a;
  --ring:       rgba(255,255,255,0.12);
  --accent:     #6da7ec;
  --accent-ink: #0d0d0d;
  --series-1:   #3987e5;
  --tag-bg:     #2a2118;
  --tag-ink:    #e8bd85;
  --tag-rule:   #5a4529;
}

* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0;
  background: var(--plane);
  color: var(--ink);
  font: 16px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
  overflow-wrap: break-word;
}
.wrap { max-width: var(--wrap); margin: 0 auto; padding: 0 1.25rem; }
a { color: var(--accent); text-underline-offset: 2px; }
a:hover { text-decoration-thickness: 2px; }
code {
  font: 0.875em/1.4 ui-monospace, SFMono-Regular, Menlo, monospace;
  background: color-mix(in srgb, var(--ink) 7%, transparent);
  padding: 0.1em 0.35em; border-radius: 4px;
}
h1, h2, h3 { line-height: 1.25; letter-spacing: -0.011em; margin: 0 0 0.5rem; }
h1 { font-size: clamp(1.75rem, 1.2rem + 2.2vw, 2.75rem); }
h2 { font-size: clamp(1.25rem, 1.05rem + 0.8vw, 1.6rem); margin-top: 0; }
h3 { font-size: 1.05rem; }
p { margin: 0 0 1rem; }
.muted { color: var(--muted); }
.small { font-size: 0.875rem; }
.eyebrow {
  text-transform: uppercase; letter-spacing: 0.08em; font-size: 0.75rem;
  font-weight: 600; color: var(--muted); margin-bottom: 0.5rem;
}
.lede { font-size: 1.075rem; color: var(--ink-2); max-width: 62ch; }
.prose { max-width: 68ch; color: var(--ink-2); }
.prose ul { padding-left: 1.15rem; }
.prose li { margin-bottom: 0.5rem; }
.skip {
  position: absolute; left: -9999px; top: 0; background: var(--accent);
  color: var(--accent-ink); padding: 0.6rem 1rem; z-index: 10;
}
.skip:focus { left: 0; }
.visually-hidden {
  position: absolute; width: 1px; height: 1px; overflow: hidden;
  clip: rect(0 0 0 0); clip-path: inset(50%); white-space: nowrap;
}

/* header */
.site-head { background: var(--surface); border-bottom: 1px solid var(--rule); }
.head-inner {
  display: flex; align-items: center; justify-content: space-between;
  gap: 1rem; flex-wrap: wrap; padding-block: 0.75rem;
}
.brand { display: flex; align-items: center; gap: 0.65rem; text-decoration: none; color: var(--ink); }
.brand-mark {
  display: grid; place-items: center; width: 2.1rem; height: 2.1rem; flex: none;
  border-radius: 7px; background: var(--accent); color: var(--accent-ink);
  font-weight: 700; font-size: 0.8rem; letter-spacing: 0.02em;
}
.brand-text { display: flex; flex-direction: column; line-height: 1.2; }
.brand-sub { font-size: 0.72rem; color: var(--muted); }
.site-head nav { display: flex; gap: 0.25rem; flex-wrap: wrap; }
.site-head nav a {
  padding: 0.4rem 0.7rem; border-radius: 7px; text-decoration: none;
  color: var(--ink-2); font-size: 0.925rem;
}
.site-head nav a:hover { background: color-mix(in srgb, var(--ink) 6%, transparent); color: var(--ink); }
.site-head nav a.is-active { background: color-mix(in srgb, var(--accent) 14%, transparent); color: var(--accent); font-weight: 600; }

/* disclaimer — present on every page */
.disclaimer { background: var(--tag-bg); border-bottom: 1px solid var(--tag-rule); }
.disclaimer .wrap { display: flex; gap: 0.75rem; align-items: baseline; padding-block: 0.7rem; }
.disclaimer p { margin: 0; font-size: 0.875rem; color: var(--tag-ink); }
.disclaimer strong { font-weight: 700; }
.disclaimer-tag {
  flex: none; text-transform: uppercase; letter-spacing: 0.06em; font-size: 0.68rem;
  font-weight: 700; color: var(--tag-ink); border: 1px solid var(--tag-rule);
  border-radius: 999px; padding: 0.15rem 0.5rem;
}

/* sections */
.hero { background: var(--surface); border-bottom: 1px solid var(--rule); padding-block: clamp(2.5rem, 6vw, 4.5rem); }
.band { padding-block: clamp(1.75rem, 4vw, 3rem); }
.band + .band { border-top: 1px solid var(--rule); }
.cta-row { display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 1.25rem; }
.btn {
  display: inline-block; padding: 0.6rem 1.05rem; border-radius: 8px;
  border: 1px solid var(--ring); background: var(--surface); color: var(--ink);
  text-decoration: none; font-weight: 600; font-size: 0.925rem;
}
.btn:hover { border-color: var(--accent); color: var(--accent); }
.btn-primary { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
.btn-primary:hover { filter: brightness(1.08); color: var(--accent-ink); }

/* stat tiles */
.stat-row {
  display: grid; gap: 0.75rem; margin: 1.25rem 0 0;
  grid-template-columns: repeat(auto-fit, minmax(11rem, 1fr));
}
.stat {
  background: var(--surface); border: 1px solid var(--ring);
  border-radius: var(--radius); padding: 1rem;
}
.stat-value { font-size: clamp(1.5rem, 1.2rem + 1.1vw, 2rem); font-weight: 650; letter-spacing: -0.02em; font-variant-numeric: tabular-nums; }
.stat-label { font-size: 0.875rem; color: var(--ink-2); margin-top: 0.15rem; }
.stat-note { font-size: 0.78rem; color: var(--muted); margin-top: 0.3rem; }

/* chart */
.chart {
  margin: 1.5rem 0 0; padding: 1.25rem; background: var(--surface);
  border: 1px solid var(--ring); border-radius: var(--radius); overflow-x: auto;
}
.chart figcaption { margin-bottom: 0.75rem; }
.chart figcaption h3 { margin-bottom: 0.25rem; }
.chart figcaption p { margin: 0; max-width: 60ch; font-size: 0.875rem; }
.chart svg { display: block; min-width: 30rem; }
.bar { fill: var(--series-1); }
.bar-g:hover .bar { filter: brightness(1.1); }
.bar-label { fill: var(--ink-2); font-size: 12.5px; }
.bar-value { fill: var(--ink); font-size: 12.5px; font-weight: 620; font-variant-numeric: tabular-nums; }

/* cards */
.cards { display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); margin-top: 1rem; }
.cards.two { grid-template-columns: repeat(auto-fit, minmax(20rem, 1fr)); }
.card {
  background: var(--surface); border: 1px solid var(--ring);
  border-radius: var(--radius); padding: 1.1rem;
}
.card h3 { margin-bottom: 0.35rem; }
.card p { margin: 0; color: var(--ink-2); font-size: 0.925rem; }
.card p + p { margin-top: 0.6rem; }

/* chips */
.chips { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.75rem; }
.chip {
  display: inline-block; padding: 0.25rem 0.6rem; border-radius: 999px;
  border: 1px solid var(--ring); background: var(--surface);
  font-size: 0.8rem; color: var(--ink-2); text-decoration: none;
}
a.chip:hover { border-color: var(--accent); color: var(--accent); }

/* fact grid */
.factgrid { display: grid; gap: 0.75rem; grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr)); margin: 1rem 0 1rem; }
.factgrid > div { background: var(--surface); border: 1px solid var(--ring); border-radius: var(--radius); padding: 0.85rem 1rem; }
.factgrid dt { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); }
.factgrid dd { margin: 0.25rem 0 0; }

/* tables */
.data { width: 100%; border-collapse: collapse; margin-top: 1rem; font-size: 0.925rem; }
.data th, .data td { text-align: left; padding: 0.55rem 0.7rem; border-bottom: 1px solid var(--rule); }
.data thead th { font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); border-bottom-color: var(--ring); }
.data tbody tr:hover { background: color-mix(in srgb, var(--ink) 4%, transparent); }
.data .num { text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; }
.table-scroll { overflow-x: auto; }
ul.plain { list-style: none; padding: 0; margin: 0; }
ul.plain li { margin-bottom: 0.35rem; }

/* dataset listing */
.doccat { margin-top: 2rem; }
.doccat-head p { max-width: 68ch; color: var(--ink-2); font-size: 0.925rem; }
.doccat-head p.muted { color: var(--muted); font-size: 0.85rem; margin-bottom: 0.5rem; }
.docs { max-width: 46rem; }
.docs td a { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.875rem; }

/* benchmark */
.qgroup { margin-top: 2rem; }
.qgroup h3 { padding-bottom: 0.5rem; border-bottom: 1px solid var(--rule); }
.qa-list { list-style: none; padding: 0; margin: 1rem 0 0; display: grid; gap: 0.75rem; }
.qa { background: var(--surface); border: 1px solid var(--ring); border-radius: var(--radius); padding: 1rem 1.1rem; }
.qa p { margin: 0; }
.qa .q { font-weight: 600; }
.qa .qid {
  display: inline-block; margin-right: 0.55rem; padding: 0.1rem 0.45rem;
  border-radius: 5px; background: color-mix(in srgb, var(--accent) 14%, transparent);
  color: var(--accent); font-size: 0.78rem; font-weight: 700;
}
.qa .a { margin-top: 0.6rem; color: var(--ink-2); }
.qa .src { margin-top: 0.5rem; font-size: 0.8rem; color: var(--muted); }

/* footer */
.site-foot { background: var(--surface); border-top: 1px solid var(--rule); margin-top: 2rem; }
.foot-grid {
  display: grid; gap: 1.5rem; padding-block: 2rem;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
}
.foot-grid h2 { font-size: 0.95rem; }
.foot-grid p { max-width: 62ch; font-size: 0.85rem; margin: 0; }
.foot-bar { border-top: 1px solid var(--rule); padding-block: 0.9rem; }
.foot-bar p { margin: 0; font-size: 0.8rem; }

@media (max-width: 34rem) {
  .head-inner { align-items: flex-start; }
  .disclaimer .wrap { flex-direction: column; gap: 0.4rem; }
}
"""

# --- search engine exclusion -------------------------------------------------
#
# Two ways to stay out of search results, and they pull against each other:
#
#   "block-crawl"  (default) — robots.txt Disallow: /. Compliant crawlers never
#       fetch anything, so nothing is indexed. Correct for a site that has never
#       been published. Residual risk: if someone links to a URL from elsewhere,
#       Google may list the bare URL with no description, because it is not allowed
#       to fetch the page and therefore never sees the noindex tag.
#
#   "allow-crawl"  — robots.txt permits fetching, and every response carries
#       noindex (meta tag on HTML, X-Robots-Tag header on the PDFs). Crawlers must
#       fetch to see that, which is exactly why this is the only option that
#       *guarantees* a URL is dropped from an index, including one already listed
#       or discovered through an inbound link. Requires the CDN to send the header;
#       without it the PDFs would be indexable.
#
# Switch to "allow-crawl" if the site is ever linked publicly or if a URL has
# already been indexed. Keep "block-crawl" otherwise.
ROBOTS_MODE = "block-crawl"


# Blanket "User-agent: *" already covers every compliant crawler; the named agents
# below are listed explicitly so the intent is unambiguous to anyone reading the file,
# and because a few crawlers only honour directives addressed to them by name.
ROBOTS_AGENTS = [
    "Googlebot", "Googlebot-Image", "Googlebot-News", "Google-Extended", "AdsBot-Google",
    "Bingbot", "msnbot", "Slurp", "DuckDuckBot", "Baiduspider", "YandexBot", "Applebot",
    "Applebot-Extended", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot",
    "Claude-Web", "anthropic-ai", "PerplexityBot", "CCBot", "Amazonbot", "Bytespider",
    "meta-externalagent", "FacebookBot", "Diffbot", "omgili",
]

_ROBOTS_HEAD = """# ChemCorp Industries — synthetic benchmark corpus.
#
# This site is deliberately fabricated content published only as a RAG benchmark.
# It must never appear in search results or be ingested into a training corpus.
# Nothing here is factual, and indexing it would put invented company data,
# invented people and invented financial figures into search indexes.
"""

_BLOCK_CRAWL_BODY = """#
# Crawling is disallowed site-wide, including the PDF corpus under /docs/.
# The HTML pages additionally carry a noindex robots meta tag, and the CDN should
# send "X-Robots-Tag: noindex, nofollow" on every response — see _headers.

User-agent: *
Disallow: /

{named}
"""

_ALLOW_CRAWL_BODY = """#
# Crawling is deliberately ALLOWED so that crawlers fetch each URL and see the
# noindex directive — the meta robots tag on the HTML pages and the X-Robots-Tag
# header on every response (see _headers). This is what guarantees a URL is
# dropped from an index rather than merely never fetched.
#
# Do not add Disallow rules here without removing the reliance on noindex: a
# crawler that is blocked from fetching can never see the directive.

User-agent: *
Disallow:
"""

def _robots_txt():
    named = "\n\n".join("User-agent: %s\nDisallow: /" % a for a in ROBOTS_AGENTS)
    body = (_BLOCK_CRAWL_BODY.format(named=named) if ROBOTS_MODE == "block-crawl"
            else _ALLOW_CRAWL_BODY)
    return _ROBOTS_HEAD + body + "\n# No sitemap is published, by design.\n"

# Netlify and Cloudflare Pages both read a "_headers" file at the publish root.
# This is what covers the PDFs, which cannot carry a robots meta tag themselves.
HEADERS_FILE = """# Applied by Netlify / Cloudflare Pages at the publish root.
# X-Robots-Tag is the only way to mark non-HTML files (the PDF corpus) as noindex.

/*
  X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex

/docs/*
  X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex
"""

# Equivalent configuration for Vercel, if that is the target instead.
VERCEL_JSON = """{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Robots-Tag", "value": "noindex, nofollow, noarchive, nosnippet, noimageindex" }
      ]
    }
  ]
}
"""

# --- chatbot widget ---------------------------------------------------------

# Seeded into website/assets/verbatim-widget.js on the first run and never
# overwritten afterwards (see main()), so credentials survive every rebuild.
WIDGET_JS = """/* Verbatim AI chatbot widget — configuration for the ChemCorp demo site.
 *
 * HAND-MAINTAINED FILE. gen_website.py creates it once if missing and never
 * overwrites it, so your credentials survive every rebuild. To get a fresh
 * copy of this template, delete the file and re-run gen_website.py.
 *
 * Docs: https://verbatim-ai.gitbook.io/docs
 */
(function () {
  // --- Fill these in ------------------------------------------------------
  // Token needs 4 scopes: session:read, session:create, post:read, post:create
  var ACCESS_TOKEN = "YOUR_ACCESS_TOKEN";
  var CORPUS_IDS   = ["YOUR_CORPUS_ID"];   // at least one corpus id
  // ------------------------------------------------------------------------

  if (typeof ChatbotWidget === "undefined") {
    console.warn("[chemcorp] Verbatim widget bundle did not load — skipping mount.");
    return;
  }
  if (!ACCESS_TOKEN || ACCESS_TOKEN === "YOUR_ACCESS_TOKEN" ||
      !CORPUS_IDS.length || CORPUS_IDS[0] === "YOUR_CORPUS_ID") {
    console.info("[chemcorp] Verbatim widget not configured yet — set ACCESS_TOKEN " +
                 "and CORPUS_IDS in website/assets/verbatim-widget.js.");
    return;
  }

  ChatbotWidget.mountChatbotWidget("#verbatim-chatbot", {
    // Connection
    // apiBaseUrl: "https://staging-api.verbatim-ai.com",  // staging; default is production
    accessToken: ACCESS_TOKEN,
    corpusIds: CORPUS_IDS,
    lang: "en",

    // Content
    title: "ChemCorp Assistant",
    greeting: "Hi! Ask me anything about the ChemCorp corpus — invoices, product data " +
              "sheets, purchase orders, meeting minutes and strategy documents.",
    greetingOutside: true,
    chatPrompts: [
      "What is the total including VAT on invoice FC-2024-00187?",
      "What is the CAS number of acetone and its auto-ignition temperature?",
      "Which supplier received the highest-value purchase order?",
      "What are the 2024–2030 green-chemistry objectives?"
    ],

    // Appearance — tracks the site accent (--accent #1c5cab, --series-1 #2a78d6)
    theme: {
      preset: "boring",
      tokens: {
        headerBackground: "linear-gradient(90deg, #1c5cab, #2a78d6)",
        openButtonBackground: "#1c5cab",
        openButtonColor: "#ffffff",
        badgeBackground: "#8a4b12"
      }
    }
  });
})();
"""

# --- main -------------------------------------------------------------------

def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    docs = scan_docs()
    total = sum(len(v) for v in docs.values())
    if total == 0:
        raise SystemExit("No PDFs found in website/docs — run the document generators first.")

    (ASSETS / 'site.css').write_text(CSS)
    print(f"  Generated: {ASSETS / 'site.css'}")

    widget_cfg = ASSETS / 'verbatim-widget.js'
    if widget_cfg.exists():
        print(f"  Kept:      {widget_cfg} (hand-maintained — not regenerated)")
    else:
        widget_cfg.write_text(WIDGET_JS)
        print(f"  Generated: {widget_cfg} — fill in ACCESS_TOKEN and CORPUS_IDS")

    for name, builder in [('index.html', build_index), ('company.html', build_company),
                          ('dataset.html', build_dataset), ('benchmark.html', build_benchmark)]:
        path = SITE / name
        path.write_text(builder(docs))
        print(f"  Generated: {path}")

    for name, content in [('robots.txt', _robots_txt()), ('_headers', HEADERS_FILE),
                          ('vercel.json', VERCEL_JSON)]:
        path = SITE / name
        path.write_text(content)
        print(f"  Generated: {path}")

    print(f"Done — 4 pages + stylesheet + widget config + 3 exclusion files, "
          f"indexing {total} documents.")

if __name__ == '__main__':
    main()
