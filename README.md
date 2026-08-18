# Dateset and Question & Answer set over virtual ChemCorp Industries company

A synthetic document corpus for benchmarking Verbatim's AI RAG systems.

The dataset models the paper trail of **ChemCorp Industries S.A.**, a fictional French chemical
distributor based in Villeurbanne: 30 PDFs across 104 pages, spanning sales invoices, purchase
orders, product data sheets, analytical datasets, internal and customer meeting minutes, and
confidential strategy documents. All content is in **English**, generated deterministically by seven
standalone [reportlab](https://www.reportlab.com/) scripts committed alongside the output.

The corpus is paired with [`test.md`](test.md) — a 50-question QA benchmark with expected answers
and per-question source attribution — so retrieval precision and answer accuracy can both be scored.

Everything here is **fictional**. See [Disclaimer](#disclaimer).

---

## Disclaimer

ChemCorp Industries S.A. does not exist. Every company, person, address, bank detail, price,
financial figure, batch number and certification in this corpus is fabricated for benchmarking
purposes. Real company names (BASF, Solvay, Arkema, Brenntag, TotalEnergies) appear only as
synthetic supplier placeholders and none of the associated transactions, contacts or terms are real.

## Corpus at a glance

| Directory | Docs | Pages | Ref pattern | Content |
|---|---:|---:|---|---|
| `website/docs/invoices/` | 8 | 35 | `FC-2024-NNNNN` | Sales invoices (ChemCorp → customers), 4–5 pp: line items, 20% VAT, payment terms, batch traceability, ADR dangerous-goods classification, general T&Cs, COA specifications |
| `website/docs/orders/` | 6 | 18 | `BC-2024-NNNN` | Purchase orders (suppliers → ChemCorp), 3 pp: line items in tonnes, Incoterms, purchasing T&Cs, technical specification annex |
| `website/docs/product-sheets/` | 5 | 15 | `FT-<REF>-2024` | Product data sheets, 3 pp / 9 sections: CAS & EC identity, physico-chemical properties, analytical specs, CLP/GHS hazards, storage, transport |
| `website/docs/datasets/` | 3 | 11 | `DS-<DOMAIN>-2024` | Analytical tables (solvent QC, production batches, energy) with raw rows plus a statistical summary |
| `website/docs/internal-meeting-notes/` | 3 | 9 | `CRI-<DEPT>-2024-NNN` | Internal minutes (R&D, Production, Strategy): attendees, agenda, proceedings, action plan |
| `website/docs/customer-meeting-notes/` | 3 | 9 | `CRC-<CLIENT>-2024-NN` | Customer meeting minutes: account profile, background, identified opportunities, actions |
| `website/docs/business-goals/` | 2 | 7 | `OBJ-<THEME>-<YEARS>` | Confidential strategy documents: 2024 targets, 2024–2030 green-chemistry roadmap, risk analysis |
| **Total** | **30** | **104** | | |

Reference codes keep their original French-derived prefixes (`FC` facture, `BC` bon de commande,
`FT` fiche technique, `CRI`/`CRC` compte rendu interne/client) because they are identifiers, not
prose — retrieval questions cite them verbatim.

Documents are dense on purpose: boilerplate annexes (T&Cs, regulatory notices, generic application
notes) are repeated across documents of the same type, so retrieval has to discriminate between
near-identical passages rather than matching on surface novelty.

## The content universe

Queries target these entities, so they are worth knowing before authoring new questions.

**Company** — ChemCorp Industries S.A., 14 Rue des Réactifs, 69100 Villeurbanne, France.
VAT `FR 42 387 542 891`, IBAN `FR76 3000 6000 0112 3456 7890 189`, BIC `BNPAFRPPXXX`.
Certified ISO 9001:2015 and ISO 14001:2015, with a COFRAC-accredited lab (No. 1-5421) and a
`QC-TRACK v4.2` LIMS. Sites: Villeurbanne (HQ and warehouses), Roussillon, Lyon-Est chemical
terminal, Limonest safety-stock depot. Reference 2023 revenue €47.2M, EBITDA €8.4M (17.8%).
There is deliberately **no SIRET, RCS or share capital** anywhere in the corpus.

**Two near-disjoint product catalogues** — the most common source of confusion:

- **Sales catalogue** — 18 SKUs priced in €/L and €/kg (`gen_invoices.py:26-45`): `AK-995` acetone,
  `TL-DIS` toluene, `NaOH-P` sodium hydroxide, `H2SO4-96`, `HCL-33`, `PG-USP` propylene glycol, etc.
- **Purchasing catalogue** — 15 raw materials priced in €/tonne (`gen_orders.py:31-46`): `EG-999P`
  ethylene glycol, `MeOH-T` methanol, `STY-INH` styrene, `DMF-99`, `CHCl3-S`, etc.

Only **two chemicals appear in both** — methanol (`ME-PUR` sold vs `MeOH-T` purchased) and ethyl
acetate (`EA-99` vs `EtOAc-T`) — and they carry **different reference codes in each catalogue**, so
no query can join an invoice line to a purchase-order line by reference. Every other product exists
on one side only.

**Counterparties** — 5 customers (Plastex GmbH 🇩🇪, Solvalor S.A.S. 🇫🇷, Nordic Resins AB 🇸🇪,
Iberchem S.L. 🇪🇸, Deltasolv NV 🇧🇪) and 5 suppliers (BASF SE, Solvay S.A., Arkema France S.A.S.,
Brenntag SAS, TotalEnergies Fluids).

**Recurring cast** — the same ~20 people appear consistently across minutes and strategy documents:
François Lemercier (CEO), Hélène Marchand (Operations), Dr. Martine Chabrol (R&D), Thierry Bruneau
(CFO), Pierre Valentin (Sales), Bertrand Vidal (Production), Ingrid Hoffmann (QHSE), and others.

**Conventions** — business documents run **January–June 2024**; the datasets cover all twelve
months of 2024; product sheets carry a 2025-01-15 revision date; strategic targets look ahead to
2027 and 2030. Dates are **ISO `YYYY-MM-DD`** in metadata and tables, and spelled out
(`15 February 2024`) in prose. Amounts are in **EUR** with English number formatting —
`1,556.40`, `12,204.00` — consistently across all seven generators. VAT is a flat 20%.

## How documents cross-reference each other

Links are **semantic, not by identifier** — there are no foreign keys to follow, which is the point.

- **Product ref → data sheet** is the strongest join: `AK-995` → `FT-AK995-2024`, and likewise for
  `NaOH-P`, `H2SO4-96`, `HCL-33`, `PG-USP`. Only these 5 of the 18 sold SKUs have a data sheet.
- **Customer name** joins invoices ↔ customer meeting minutes. Plastex, Solvalor and Nordic Resins
  have both; Iberchem and Deltasolv appear in invoices only.
- **Supplier name** joins purchase orders ↔ internal minutes (e.g. BASF and Brenntag both surface in
  the MEG shortage discussed in `CRI-PROD-2024-007`).
- **KPI values** join minutes ↔ strategy documents ↔ datasets — e.g. first-pass yield 94.1% actual
  in the production minutes against a 97% target in `OBJ-STRAT-2024`.
- **Project names** thread throughout: BioSolv-3/-5/-7/-10, GreenCat-Est/-Hyd/-Ox, EcoSolv-D4.
- **No invoice references an order number, and no order references an invoice.** Sales and
  purchasing are separate universes by design.

Batch numbering is intentionally inconsistent across document types (`LOT-2410xx` in invoices and
the QC dataset, `B24xxxx` in the batch dataset, ad-hoc refs such as `ACK-230814` in the minutes) —
there is no single batch registry to resolve against.

## Regenerating the corpus and site

```bash
./build.sh
```

`build.sh` creates a virtualenv, installs `requirements.txt`, runs the seven document generators
and then `gen_website.py`. Documents land in `website/docs/<category>/`; the site pages are written
to `website/`. To run against an existing environment instead:

```bash
pip install -r requirements.txt
for f in gen_*.py; do [ "$f" = gen_website.py ] || python3 "$f"; done
python3 gen_website.py
```

Each document generator is independent — run just one to rebuild a single category, then
`gen_website.py` to refresh the index. Content is fully hardcoded in six of the seven; `gen_datasets.py`
synthesises measurement values through `random.gauss`, seeded once at module level with
`random.seed(42)` (`gen_datasets.py:11`). A **complete** run of that script is therefore
reproducible; generating its three datasets individually or in a different order would not be.
Regenerated PDFs differ from the committed ones only in their embedded creation timestamps.

## The website

`gen_website.py` emits a four-page static site into `website/`, ready to publish to a CDN with no
build step and no external assets:

| Page | Contents |
|---|---|
| `index.html` | What the company is, why the corpus exists, headline figures |
| `company.html` | Identity, sites, people, both catalogues, customers, suppliers, strategy |
| `dataset.html` | Every document listed by category with page counts and download links |
| `benchmark.html` | The 50 questions, parsed directly from `test.md` |

The document index is built by scanning `website/docs/`, and the benchmark page is parsed from
`test.md`, so neither can drift from the corpus. Every page carries a fictional-content disclaimer
in a banner and again in the footer. The CSS is theme-aware (light and dark).

### Keeping the site out of search engines

The corpus is fabricated, so it must never reach a search index. Three layers cover this, and
`gen_website.py` emits all of them:

| File | Covers |
|---|---|
| `robots.txt` | `Disallow: /` for `User-agent: *` plus 28 named crawlers, including Googlebot, Bingbot and the AI crawlers (GPTBot, ClaudeBot, CCBot, PerplexityBot, Google-Extended, …) |
| `_headers` | `X-Robots-Tag: noindex, nofollow, noarchive, nosnippet, noimageindex` — read by Netlify and Cloudflare Pages. **This is the only layer that covers the PDFs**, which cannot carry a meta tag |
| `vercel.json` | The same header, for Vercel |

Each HTML page additionally carries `noindex, nofollow, noarchive, nosnippet, noimageindex` as a
robots meta tag, with `googlebot` and `bingbot` variants. No sitemap is published.

**If your CDN is not Netlify, Cloudflare Pages or Vercel**, configure the equivalent response
header yourself — `X-Robots-Tag: noindex, nofollow` on every path. Without it the 30 PDFs rely on
`robots.txt` alone.

**One caveat worth understanding.** `Disallow: /` stops compliant crawlers from *fetching*, which
also means they never see the `noindex` directive. For a site that has never been published that is
exactly right — it is never indexed in the first place. But if a URL is ever linked publicly, Google
can list the bare URL with no description precisely because it is not allowed to fetch the page and
confirm the `noindex`. To *guarantee* a URL is dropped from an index, crawling must be allowed so
the directive is seen. Flip `ROBOTS_MODE` at the top of `gen_website.py` from `"block-crawl"` to
`"allow-crawl"` if the site is linked publicly or a URL has already been indexed; that mode depends
on the `X-Robots-Tag` header being served, so confirm your CDN sends it first.

## The QA benchmark

[`test.md`](test.md) holds 50 questions, each with an expected answer and the PDF it should be
retrieved from:

```markdown
**Q1.** What is the total including VAT on invoice FC-2024-00187?
> **A.** 1,556.40 € incl. VAT (subtotal excl. VAT 1,297.00 € + VAT 20% 259.40 €).
> *Source: FC-2024-00187.pdf*
```

| Questions | Category |
|---|---|
| Q1–Q8 | Invoices |
| Q9–Q15 | Product data sheets |
| Q16–Q21 | Purchase orders |
| Q22–Q28 | Internal meeting minutes |
| Q29–Q34 | Customer meeting minutes |
| Q35–Q39 | Business goals & strategy |
| Q40–Q45 | Analytical datasets |
| Q46–Q50 | **Cross-document** — each requires combining two or more sources |

Every ground-truth string in `test.md` is verified to appear in the PDF it cites.

## Notes for question authors

- The datasets' statistical-summary tables are hand-written constants, **not** computed from the
  generated rows. If you change the seed or the row count, those tables will no longer match the raw
  data above them.
- `DS-QC-SOL-2024` emits batches `LOT-241001`–`LOT-241036` only. Its "3 batches placed under review"
  figure is prose in the conclusions (`gen_datasets.py:279`), not derived from its own rows — so do
  not expect to find three `FAIL` rows in the table.
- There is **no toluene product data sheet**. The toluene specification (benzene ≤ 1 ppm) lives in
  the invoice technical annex (`gen_invoices.py:291-296`), which is reproduced on every invoice.
- **Stick to WinAnsi-encodable characters in document text.** The PDFs use the standard Helvetica
  font, so anything outside WinAnsiEncoding renders as a black box. Unicode subscripts, `≤`, `≥`,
  `✓` and `⚠` were all silently broken until they were replaced with `2`/`3`, `<=`, `>=` and plain
  words. Bullets must be `•` or `»` (both encode); `◆` and `▶` do not.
- Three earlier defects in `test.md` (a propylene glycol cross-reference to a purchase order that
  never contained it, a toluene spec attributed to the wrong PDF, and batch IDs attributed to the
  wrong dataset) have been corrected. If you are comparing against an older copy of the benchmark,
  Q11, Q41 and Q47 are the ones that changed.

## Repository layout

```
.
├── website/
│   ├── index.html               # generated site pages
│   ├── company.html
│   ├── dataset.html
│   ├── benchmark.html
│   ├── assets/site.css
│   ├── robots.txt               # search engine exclusion
│   ├── _headers                 # X-Robots-Tag for Netlify / Cloudflare Pages
│   ├── vercel.json              # X-Robots-Tag for Vercel
│   └── docs/                    # the corpus, served by the site
│       ├── business-goals/          ← gen_business_goals.py
│       ├── customer-meeting-notes/  ← gen_customer_meetings.py
│       ├── datasets/                ← gen_datasets.py
│       ├── internal-meeting-notes/  ← gen_internal_meetings.py
│       ├── invoices/                ← gen_invoices.py
│       ├── orders/                  ← gen_orders.py
│       └── product-sheets/          ← gen_product_sheets.py
├── gen_*.py                     # 7 document generators + gen_website.py
├── build.sh                     # venv + install + build corpus and site
├── requirements.txt             # reportlab (the only third-party dependency)
├── test.md                      # 50-question QA benchmark
└── README.md
```

Each generator defines its documents as module-level dicts (`INVOICES`, `ORDERS`, `PRODUCTS`,
`DATASETS`, `MEETINGS`, `DOCS`) near the top of the file — that is where to add or edit a document.
