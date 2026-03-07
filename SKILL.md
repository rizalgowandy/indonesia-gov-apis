---
name: querying-indonesian-gov-data
description: >
  Query 50 Indonesian government APIs and data sources — BPJPH halal, BPOM food safety,
  OJK financial legality, BPS statistics, BMKG weather/earthquakes, Bank Indonesia rates,
  pasal.id law MCP, IDX stocks. Use when building apps with Indonesian government data,
  scraping .go.id websites, checking halal certification, verifying company legality,
  looking up financial entity status, or connecting to Indonesian MCP servers.
  Includes ready-to-run Python patterns, CSRF handling, CKAN API usage, DataTables
  scraping, and IP blocking workarounds.
---

# Querying Indonesian Government Data

🇮🇩 STARTER_CHARACTER = 🇮🇩

## Workflow

1. Identify which data source matches the user's need (see Quick Router below)
2. Read the source-specific doc in `apis/` for endpoint details
3. Copy the pattern from this file, adapt parameters, execute
4. Handle common failure modes (IP blocking, CSRF expiry, rate limits)

## Quick Router

Match the user's intent to the right source and pattern:

| User wants... | Source | Pattern # |
|--------------|--------|-----------|
| Halal certification status | BPJPH | 1 |
| Food/drug/cosmetic registration | BPOM | 2 |
| Is this fintech/investment legal? | OJK + Satgas Waspada | 3 |
| Weather forecast, earthquake data | BMKG | 4 |
| GDP, inflation, population stats | BPS | 5 |
| USD/IDR exchange rate, BI Rate | Bank Indonesia | 6 |
| Indonesian law, specific pasal | pasal.id MCP | 7 |
| Government datasets (any topic) | data.go.id CKAN | 8 |
| Disaster risk for a location | InaRisk BNPB | 9 |
| Verify a company is registered | AHU / OpenCorporates | 10 |
| Indonesian stock prices | IDX via yfinance | 11 |
| Government procurement tenders | LPSE / INAPROC | See `apis/tier1-open-apis/lpse-inaproc/` |
| Court decisions | Putusan MA | See `apis/tier1-open-apis/putusan-ma/` |
| Public official wealth declaration | KPK e-LHKPN | See `apis/tier2-scrapeable/kpk-lhkpn/` |
| Regional city data (Jakarta, etc.) | CKAN portals | Use Pattern 8 with regional portal URL |

## Patterns

### Pattern 1: BPJPH Halal Search

```python
import requests
resp = requests.post("https://cmsbl.halal.go.id/api/search/data_penyelia",
    json={"nama_penyelia": "QUERY", "start": 0, "length": 20},
    headers={"Content-Type": "application/json"}, timeout=30)
for biz in resp.json().get("data", []):
    print(f"{biz['nama']} | {biz.get('kota_kab','')} | Cert: {biz.get('nomor_sertifikat','')} | Exp: {biz.get('berlaku_sampai','')}")
```

- No auth. Max `length`: 100. Field `nama_penyelia` is supervisor name prefix — use single letters for broad results.
- Bulk: iterate A-Z with 1s delay. ~116K records/hour.

### Pattern 2: BPOM Product Lookup

```python
import requests
from bs4 import BeautifulSoup
s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
page = s.get("https://cekbpom.pom.go.id/produk/pangan-olahan", timeout=30)
csrf = BeautifulSoup(page.text, "html.parser").find("meta", {"name": "csrf-token"})["content"]
resp = s.post("https://cekbpom.pom.go.id/produk-dt", data={
    "_token": csrf, "draw": 1, "start": 0, "length": 25, "search[value]": "QUERY",
}, headers={"X-Requested-With": "XMLHttpRequest"}, timeout=30)
for p in resp.json().get("data", []):
    print(f"{p['no_reg']} | {p['nama_produk']} | {p['merk']} | {p['pendaftar']}")
```

- CSRF required — fetch page first. Refresh token every 30min or 10K requests.
- Categories: `pangan-olahan` (food), `obat` (drugs), `kosmetik` (cosmetics), `suplemen-kesehatan` (supplements).
- Rate limit: 2s minimum between requests.

### Pattern 3: OJK Financial Legality Check

```python
import requests
from bs4 import BeautifulSoup
resp = requests.get("https://sikapiuangmu.ojk.go.id/FrontEnd/AlertPortal/Search",
    params={"q": "COMPANY"}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
soup = BeautifulSoup(resp.text, "html.parser")
for row in soup.select("table tbody tr"):
    cols = [td.text.strip() for td in row.find_all("td")]
    if cols: print(f"⚠️ {' | '.join(cols)}")
```

- No result ≠ legal. Entity may simply not be in database.
- Also check: `waspadainvestasi.ojk.go.id` for illegal investment alerts.

### Pattern 4: BMKG Weather & Earthquakes

```python
import requests
# Latest earthquake — no auth, real-time
q = requests.get("https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", timeout=30).json()["Infogempa"]["gempa"]
print(f"M{q['Magnitude']} | {q['Wilayah']} | {q['Tanggal']} {q['Jam']}")

# Recent 15
for q in requests.get("https://data.bmkg.go.id/DataMKG/TEWS/gempaterkini.json", timeout=30).json()["Infogempa"]["gempa"]:
    print(f"M{q['Magnitude']} | {q['Wilayah']}")
```

- Weather XML: `data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-{Province}.xml`
- Province codes: `DKIJakarta`, `JawaBarat`, `JawaTimur`, `Bali`, `SulawesiSelatan`, etc.

### Pattern 5: BPS Statistics

```python
import requests
API_KEY = "YOUR_KEY"  # Free: webapi.bps.go.id/developer
resp = requests.get(f"https://webapi.bps.go.id/v1/api/list/model/data/domain/0000/var/1/key/{API_KEY}", timeout=30)
for item in resp.json().get("data", []):
    print(f"{item.get('tahun')}: {item.get('data_content')}")
```

- `domain=0000` national, `3100` Jakarta, `3200` Jabar. `var=1` CPI, `var=104` population.
- ~100 req/day. Returns HTML on error — check content-type.

### Pattern 6: Bank Indonesia Exchange Rates

```python
import requests
from bs4 import BeautifulSoup
resp = requests.get("https://www.bi.go.id/id/statistik/informasi-kurs/transaksi-bi/Default.aspx",
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}, timeout=30)
for row in BeautifulSoup(resp.text, "html.parser").find("table", class_="table1").find_all("tr")[1:]:
    cols = [td.text.strip() for td in row.find_all("td")]
    if len(cols) >= 3: print(f"{cols[0]}: Buy {cols[1]} / Sell {cols[2]}")
```

- Published 10:00 WIB (03:00 UTC) business days only.
- BI API sandbox: `api-sandbox.bi.go.id` (OAuth2).

### Pattern 7: Indonesian Law via MCP

```bash
# Setup
claude mcp add --transport http pasal-id https://pasal-mcp-server-production.up.railway.app/mcp
```

Tools: `search_laws`, `get_pasal`, `get_law_status`, `get_law_content`. 40K regulations, 937K articles.

### Pattern 8: CKAN Open Data Search

```python
import requests
# Same pattern for: data.go.id, satudata.jakarta.go.id, opendata.jabarprov.go.id, opendata.jatimprov.go.id
PORTAL = "data.go.id"
resp = requests.get(f"https://{PORTAL}/api/3/action/package_search",
    params={"q": "KEYWORD_BAHASA", "rows": 10}, timeout=30)
for ds in resp.json()["result"]["results"]:
    print(ds["title"])
    for r in ds.get("resources", []): print(f"  └ {r['format']}: {r['url']}")
```

- Search in Indonesian: `keuangan` (finance), `kesehatan` (health), `penduduk` (population).

### Pattern 9: InaRisk Disaster Risk

```python
import requests
resp = requests.get("https://inarisk.bnpb.go.id/api/risk/score",
    params={"lat": -6.2088, "lon": 106.8456}, timeout=30)
# Returns risk scores per hazard type
```

### Pattern 10: Company Verification

```python
import requests
# OpenCorporates (500 free req/day)
resp = requests.get("https://api.opencorporates.com/v0.4/companies/search",
    params={"q": "COMPANY", "jurisdiction_code": "id"}, timeout=30)

# OCCRP Aleph (60 req/min, free key at aleph.occrp.org)
resp = requests.get("https://aleph.occrp.org/api/2/entities",
    params={"q": "COMPANY", "filter:countries": "id"},
    headers={"Authorization": "ApiKey YOUR_KEY"}, timeout=30)
```

### Pattern 11: IDX Stock Data

```python
import yfinance as yf
stock = yf.Ticker("BBCA.JK")  # .JK suffix for Indonesian stocks
print(stock.history(period="1mo")[["Close","Volume"]].tail())
# IHSG index: yf.Ticker("^JKSE")
```

Common tickers: BBCA.JK, BBRI.JK, BMRI.JK, TLKM.JK, ASII.JK, GOTO.JK.

## Failure Handling

### IP Blocked (403 / Timeout)
Most `.go.id` sites block datacenter IPs. Route through Cloudflare Workers proxy or add 2-5s delays.

### CSRF Expired
BPOM pattern: re-fetch the page, extract new `csrf-token` meta tag.

### Rate Limited
BPS: ~100/day. OpenCorporates: 500/day. OCCRP: 60/min. BPOM: 2s minimum gap.

### Required Headers
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept-Language": "id-ID,id;q=0.9,en;q=0.8",
}
```

## Extended Reference

For full endpoint documentation, response schemas, and bulk scraping strategies, read the source-specific docs:
- Tier 1 (Open APIs): `apis/tier1-open-apis/`
- Tier 2 (Scrapeable): `apis/tier2-scrapeable/`
- Tier 3 (Regional CKAN): `apis/tier3-regional/`
- Tier 4-7: `apis/tier4-ministry/` through `apis/tier7-civil-society/`
- MCP servers: `mcp-servers/`
