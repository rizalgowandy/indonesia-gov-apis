# 🇮🇩 Indonesia Government APIs & Data Sources

A comprehensive reference for **50 Indonesian government data portals, APIs, and data sources** — with practical Python examples, scraping patterns, and gotchas learned from production use.

> **Why this exists:** Indonesian government APIs are poorly documented, frequently change without notice, and have quirks not covered in official docs. This repo captures real-world knowledge from building production applications against these data sources.

## 🤖 Use as an AI Agent Skill

This repo includes a [`SKILL.md`](SKILL.md) that makes it usable as a Claude/OpenClaw agent skill:

```bash
# Clone and use as a local skill reference
git clone https://github.com/suryast/indonesia-gov-apis.git
```

## 🔌 MCP Servers

Connect Indonesian data sources to AI assistants via [Model Context Protocol](https://modelcontextprotocol.io):

```bash
# Connect pasal.id (third-party Indonesian law index) to Claude
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```

See [`mcp-servers/`](mcp-servers/) for full setup instructions and a list of data sources ready for MCP wrapping.

---

## Data Sources by Tier

### Tier 1: Open APIs — Ready to Consume (12 sources)

| # | Source | Agency | Docs | API? |
|---|--------|--------|------|------|
| 1 | [Portal Satu Data (SDI)](apis/tier1-open-apis/data-go-id/) | Bappenas | CKAN portal, 10K+ datasets | ✅ CKAN API |
| 2 | [BPS Statistics](apis/tier1-open-apis/bps/) | Badan Pusat Statistik | GDP, CPI, population, trade | ✅ REST API |
| 3 | [BMKG Weather](apis/tier1-open-apis/bmkg/) | BMKG | Weather, earthquakes, tsunami | ✅ JSON feeds |
| 4 | [IDX / BEI](apis/tier1-open-apis/idx/) | Bursa Efek Indonesia | Stock prices, corporate data | ⚠️ Unofficial |
| 5 | [DJPB Treasury](apis/tier1-open-apis/djpb-treasury/) | Kemenkeu | Treasury, disbursement data | ✅ CKAN API |
| 6 | [JDIH BPK](apis/tier1-open-apis/jdih-bpk/) | BPK / Perpusnas | Legal documentation network | ✅ Partial API |
| 7 | [Putusan MA](apis/tier1-open-apis/putusan-ma/) | Mahkamah Agung | Court decisions (millions) | ✅ Public search |
| 8 | [LPSE / INAPROC](apis/tier1-open-apis/lpse-inaproc/) | LKPP | Government procurement tenders | ⚠️ Scrape (689 hosts) |
| 9 | [Portal APBN](apis/tier1-open-apis/apbn-kemenkeu/) | Kemenkeu | State budget data | ✅ CSV/XLSX |
| 10 | [Bank Indonesia](apis/tier1-open-apis/bank-indonesia/) | Bank Indonesia | Exchange rates, BI Rate | ✅ REST API |
| 11 | [BIG Geospatial](apis/tier1-open-apis/big-geospatial/) | BIG | Admin boundaries, zoning | ✅ WMS/WFS |
| 12 | [BNPB Disaster](apis/tier1-open-apis/bnpb-disaster/) | BNPB | Disaster events, risk data | ✅ REST + GeoJSON |

### Tier 2: Scrapeable Web — Structured Data, No Formal API (10 sources)

| # | Source | Agency | Docs | Format |
|---|--------|--------|------|--------|
| 13 | [BPJPH Halal](apis/tier2-scrapeable/bpjph/) | BPJPH Kemenag | 1.98M halal businesses | JSON POST |
| 14 | [BPOM Products](apis/tier2-scrapeable/bpom/) | BPOM | 242K food/drug registrations | DataTables+CSRF |
| 15 | [AHU Company Registry](apis/tier2-scrapeable/ahu-company/) | Kemenkumham | All registered PT, CV, Firma | HTML+CAPTCHA |
| 16 | [OSS / NIB](apis/tier2-scrapeable/oss-nib/) | BKPM | Business ID (NIB) lookup | HTML forms |
| 17 | [OJK Registry](apis/tier2-scrapeable/ojk/) | OJK | Licensed financial entities | HTML+XLS |
| 18 | [KPK e-LHKPN](apis/tier2-scrapeable/kpk-lhkpn/) | KPK | Officials' wealth declarations | HTML+PDF |
| 19 | [Putusan MK](apis/tier2-scrapeable/putusan-mk/) | Mahkamah Konstitusi | Constitutional court decisions | HTML+PDF |
| 20 | [KSEI Statistics](apis/tier2-scrapeable/ksei/) | KSEI | Securities investor stats | PDF/XLSX |
| 21 | [e-PPID](apis/tier2-scrapeable/ppid/) | All Ministries | Public information requests | Per ministry |
| 22 | [Pajak / DJP](apis/tier2-scrapeable/pajak-djp/) | DJP | NPWP verification | Login required |

### Tier 3: Regional Open Data Portals (6 sources)

| # | Source | Region | Docs | Quality |
|---|--------|--------|------|---------|
| 23 | [Satu Data Jakarta](apis/tier3-regional/satu-data-jakarta/) | DKI Jakarta | Best-in-class regional | ⭐ CKAN API |
| 24 | [Open Data Jabar](apis/tier3-regional/opendata-jabar/) | Jawa Barat | Good API quality | ⭐ CKAN API |
| 25 | [Open Data Jatim](apis/tier3-regional/opendata-jatim/) | Jawa Timur | 38 kabupaten/kota | ✅ CKAN API |
| 26 | [Satu Data Surabaya](apis/tier3-regional/satu-data-surabaya/) | Surabaya | Complete city-level | ✅ CKAN API |
| 27 | [Open Data Bandung](apis/tier3-regional/opendata-bandung/) | Bandung | Smart city data | ✅ CKAN API |
| 28 | [Open Data Bali](apis/tier3-regional/opendata-bali/) | Bali | Tourism, agriculture | ⚠️ CSV/XLSX |

### Tier 4: Ministry-Specific Data (8 sources)

| # | Source | Ministry | Docs | Key Data |
|---|--------|----------|------|----------|
| 29 | [Kemnaker](apis/tier4-ministry/kemnaker/) | Ketenagakerjaan | UMR/UMP wages, employment stats | ⚠️ Partial API |
| 30 | [Komdigi](apis/tier4-ministry/komdigi/) | Komunikasi Digital | Internet penetration, digital literacy | ⚠️ XLSX |
| 31 | [ESDM Energy](apis/tier4-ministry/esdm-energy/) | ESDM | Energy production, mining permits | ⚠️ PDF/XLSX |
| 32 | [KKP Fisheries](apis/tier4-ministry/kkp-fisheries/) | Kelautan & Perikanan | Fish catch, aquaculture, vessels | ⚠️ XLSX |
| 33 | [ATR/BPN Land](apis/tier4-ministry/atr-bpn/) | ATR / BPN | Land certificates, PTSL | ❌ Login |
| 34 | [Kemendikdasmen](apis/tier4-ministry/kemendikdasmen/) | Pendidikan | School registry (NPSN), teachers | ⚠️ Partial API |
| 35 | [Kemenkes Health](apis/tier4-ministry/kemenkes/) | Kesehatan | Hospital/clinic registry, SATUSEHAT | ⚠️ Partial API |
| 36 | [Kemenag](apis/tier4-ministry/kemenag/) | Agama | 300K+ mosques, pesantren registry | ⚠️ Scrape |

### Tier 5: Anti-Corruption & Transparency (5 sources)

| # | Source | Organization | Docs | Key Data |
|---|--------|-------------|------|----------|
| 37 | [OCCRP Aleph](apis/tier5-transparency/occrp-aleph/) | OCCRP | Beneficial ownership, leaks data | ✅ REST API |
| 38 | [OpenCorporates](apis/tier5-transparency/opencorporates/) | OpenCorporates | Global company registry (ID subset) | ✅ REST API |
| 39 | [EITI Indonesia](apis/tier5-transparency/eiti-indonesia/) | EITI / ESDM | Mining & oil/gas revenue transparency | ⚠️ Reports |
| 40 | [AHU-BO](apis/tier5-transparency/ahu-bo/) | Kemenkumham | Beneficial ownership registry | ⚠️ Web search |
| 41 | [ICW Corruption Watch](apis/tier5-transparency/icw-corruption/) | ICW (NGO) | Corruption case tracker | ⚠️ Web database |

### Tier 6: Financial Sector (4 sources)

| # | Source | Agency | Docs | Key Data |
|---|--------|--------|------|----------|
| 42 | [OJK SIKEPO](apis/tier6-financial/ojk-sikepo/) | OJK | Fintech/crypto licensed platforms | ⚠️ PDF+HTML |
| 43 | [Satgas Waspada Investasi](apis/tier6-financial/satgas-waspada/) | OJK Task Force | Illegal investment alerts | ✅ Public list |
| 44 | [KSEI Investor Stats](apis/tier6-financial/ksei-stats/) | KSEI | Monthly investor statistics | ⚠️ XLSX/PDF |
| 45 | [DJPB Budget](apis/tier6-financial/djpb-budget/) | DJPB Kemenkeu | APBN spending execution | ⚠️ XLS/CSV |

### Tier 7: Civil Society & Geospatial (5 sources)

| # | Source | Organization | Docs | Key Data |
|---|--------|-------------|------|----------|
| 46 | [LAPOR!](apis/tier7-civil-society/lapor/) | KemenPANRB | Public complaint system | ⚠️ Web portal |
| 47 | [IndoLII](apis/tier7-civil-society/indolii/) | USAID | Bilingual legal information | ⚠️ Web search |
| 48 | [OGP Indonesia](apis/tier7-civil-society/ogp-indonesia/) | OGP | Ministry transparency scores | ⚠️ Reports |
| 49 | [Geoportal One Map](apis/tier7-civil-society/geoportal-onemap/) | BIG / KLHK | 85 thematic maps, One Map Policy | ✅ WMS/WFS |
| 50 | [SIGAP / InaRisk](apis/tier7-civil-society/sigap-inarisk/) | BNPB | Disaster risk scores by location | ✅ REST API |
| 51 | [pasal.id](apis/tier7-civil-society/pasal-id/) | Community (third-party) | 40K regulations, 937K articles via MCP | 🔵 MCP Ready |

---

## Quick Start

```python
# Search BPJPH halal database
import requests

resp = requests.post(
    "https://cmsbl.halal.go.id/api/search/data_penyelia",
    json={"length": 20, "start": 0, "nama_penyelia": "A"},
    headers={"Content-Type": "application/json"}
)
businesses = resp.json()["data"]
print(f"Found {len(businesses)} businesses")
```

```python
# Get BMKG earthquake data (no auth needed)
resp = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json")
quake = resp.json()["Infogempa"]["gempa"]
print(f"Latest: M{quake['Magnitude']} at {quake['Wilayah']}")
```

## Common Gotchas

### 🚫 IP Blocking
Most Indonesian gov sites block datacenter IPs (AWS, GCP, DO). Use Cloudflare Workers proxy or residential proxy.

### 📄 Data Formats
Government sites love Excel and PDF. Use `openpyxl` for Excel, `pdfplumber` for PDF.

### 🔐 CSRF Tokens
BPOM and some OJK pages require session cookies + CSRF tokens. Always use `requests.Session()`.

### 🔄 CKAN API
data.go.id, Jakarta, Jabar, Jatim, Surabaya, Bandung all use CKAN. Same API pattern works everywhere:
```python
requests.get("https://{portal}/api/3/action/package_search", params={"q": "keyword", "rows": 10})
```

## Project Structure

```
├── README.md
├── SKILL.md                      # AI agent skill file
├── mcp-servers/                  # MCP server setup guides
├── apis/
│   ├── tier1-open-apis/          # 12 sources with REST/JSON APIs
│   ├── tier2-scrapeable/         # 10 sources requiring scraping
│   ├── tier3-regional/           # 6 regional open data portals
│   ├── tier4-ministry/           # 8 ministry-specific sources
│   ├── tier5-transparency/       # 5 anti-corruption sources
│   ├── tier6-financial/          # 4 financial sector sources
│   └── tier7-civil-society/      # 5 civil society & geospatial
└── examples/                     # Working Python examples
```

## Contributing

Know an Indonesian government API not listed here? Found a gotcha? PRs welcome!

## Disclaimer

This project documents publicly available government data sources for educational and research purposes. It is not affiliated with any Indonesian government agency. Always respect rate limits and terms of service.

## License

MIT
