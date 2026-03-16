#!/usr/bin/env python3
"""Daily portal status checker. Writes results to status/data/YYYY-MM-DD.json."""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

PORTALS = [
    # (id, name, url, agency, tier)
    ("data-go-id", "Satu Data (SDI)", "https://data.go.id", "Bappenas", 1),
    ("bps", "BPS Statistics", "https://webapi.bps.go.id", "BPS", 1),
    ("bmkg", "BMKG Weather", "https://data.bmkg.go.id/DataMKG/TEWS/autogempa.json", "BMKG", 1),
    ("idx", "IDX / BEI", "https://idx.co.id", "BEI", 1),
    ("djpb-treasury", "DJPB Treasury", "https://data.treasury.kemenkeu.go.id", "Kemenkeu", 1),
    ("jdih-bpk", "JDIH BPK", "https://jdih.bpk.go.id", "BPK", 1),
    ("putusan-ma", "Putusan MA", "https://putusan3.mahkamahagung.go.id", "MA", 1),
    ("lpse", "LPSE / INAPROC", "https://spse.inaproc.id", "LKPP", 1),
    ("apbn", "Portal APBN", "https://data.anggaran.kemenkeu.go.id", "Kemenkeu", 1),
    ("bi", "Bank Indonesia", "https://www.bi.go.id", "BI", 1),
    ("big", "BIG Geospatial", "https://tanahair.indonesia.go.id", "BIG", 1),
    ("bnpb", "BNPB Disaster", "https://dibi.bnpb.go.id", "BNPB", 1),
    # Tier 2
    ("bpjph-old", "BPJPH Halal (old)", "https://sertifikasi.halal.go.id", "BPJPH", 2),
    ("bpjph-new", "BPJPH Halal (new)", "https://bpjph.halal.go.id", "BPJPH", 2),
    ("bpom", "BPOM Products", "https://cekbpom.pom.go.id", "BPOM", 2),
    ("ahu", "AHU Company Registry", "https://ahu.go.id", "Kemenkumham", 2),
    ("oss", "OSS / NIB", "https://oss.go.id", "BKPM", 2),
    ("ojk-registry", "OJK Registry", "https://sikapiuangmu.ojk.go.id", "OJK", 2),
    ("ojk-api", "OJK API", "https://api.ojk.go.id", "OJK", 2),
    ("lhkpn", "KPK e-LHKPN", "https://elhkpn.kpk.go.id", "KPK", 2),
    ("putusan-mk", "Putusan MK", "https://putusan.mahkamahkonstitusi.go.id", "MK", 2),
    ("ksei", "KSEI Statistics", "https://www.ksei.co.id", "KSEI", 2),
    ("ppid", "e-PPID", "https://ppid.kemenkeu.go.id", "Kemenkeu", 2),
    ("pajak", "Pajak / DJP", "https://ereg.pajak.go.id", "DJP", 2),
    # Tier 3
    ("jakarta", "Satu Data Jakarta", "https://data.jakarta.go.id", "DKI Jakarta", 3),
    ("jabar", "Open Data Jabar", "https://opendata.jabarprov.go.id", "Jawa Barat", 3),
    ("jatim", "Open Data Jatim", "https://data.jatimprov.go.id", "Jawa Timur", 3),
    ("surabaya", "Satu Data Surabaya", "https://data.surabaya.go.id", "Surabaya", 3),
    ("bandung", "Open Data Bandung", "https://data.bandung.go.id", "Bandung", 3),
    ("bali", "Open Data Bali", "https://data.baliprov.go.id", "Bali", 3),
    # Tier 4
    ("kemnaker", "Kemnaker", "https://kemnaker.go.id", "Ketenagakerjaan", 4),
    ("komdigi", "Komdigi", "https://komdigi.go.id", "Komunikasi Digital", 4),
    ("esdm", "ESDM Energy", "https://www.esdm.go.id", "ESDM", 4),
    ("kkp", "KKP Fisheries", "https://kkp.go.id", "KKP", 4),
    ("atr-bpn", "ATR/BPN Land", "https://www.atrbpn.go.id", "ATR/BPN", 4),
    ("kemdikbud", "Kemendikdasmen", "https://dapo.kemdikbud.go.id", "Pendidikan", 4),
    ("kemenkes", "Kemenkes Health", "https://sirs.kemkes.go.id", "Kemenkes", 4),
    ("kemenag", "Kemenag", "https://simas.kemenag.go.id", "Kemenag", 4),
    # Tier 5
    ("occrp", "OCCRP Aleph", "https://aleph.occrp.org", "OCCRP", 5),
    ("opencorporates", "OpenCorporates", "https://opencorporates.com", "OpenCorporates", 5),
    ("eiti", "EITI Indonesia", "https://eiti.esdm.go.id", "EITI/ESDM", 5),
    ("ahu-bo", "AHU-BO", "https://ahu.go.id/pencarian/pencarian-bo", "Kemenkumham", 5),
    ("icw", "ICW Corruption Watch", "https://antikorupsi.org", "ICW", 5),
    # Tier 6
    ("ojk-sikepo", "OJK SIKEPO", "https://ojk.go.id", "OJK", 6),
    ("satgas-waspada", "Satgas Waspada", "https://sikapiuangmu.ojk.go.id", "OJK", 6),
    ("ksei-stats", "KSEI Investor Stats", "https://www.ksei.co.id/publications", "KSEI", 6),
    ("djpb-budget", "DJPB Budget", "https://djpb.kemenkeu.go.id", "DJPB", 6),
    # Tier 7
    ("lapor", "LAPOR!", "https://www.lapor.go.id", "KemenPANRB", 7),
    ("indolii", "IndoLII", "https://www.indolii.org", "USAID", 7),
    ("geoportal", "Geoportal One Map", "https://tanahair.indonesia.go.id", "BIG/KLHK", 7),
    ("inarisk", "SIGAP / InaRisk", "https://inarisk.bnpb.go.id", "BNPB", 7),
    ("pasal-id", "pasal.id", "https://pasal.id", "Community", 7),
]


def check_url(url: str, timeout: int = 10) -> dict:
    """Check a URL and return status info."""
    try:
        r = subprocess.run(
            [
                "curl", "-s", "-o", "/dev/null",
                "-w", "%{http_code}|%{time_total}|%{redirect_url}",
                "-L", "--max-redirs", "3", "--max-time", str(timeout),
                url,
            ],
            capture_output=True, text=True, timeout=timeout + 5,
        )
        parts = r.stdout.strip().split("|")
        code = int(parts[0]) if parts[0].isdigit() else 0
        latency = float(parts[1]) if len(parts) > 1 else 0
        redirect = parts[2] if len(parts) > 2 else ""
    except Exception:
        code, latency, redirect = 0, 0, ""

    # Classify
    if code == 0:
        status = "dns_dead"
    elif code >= 200 and code < 400:
        status = "up"
    elif code == 403:
        status = "blocked"
    elif code >= 500:
        status = "error"
    else:
        status = "error"

    return {
        "http_code": code,
        "latency_ms": round(latency * 1000),
        "status": status,
        "redirect": redirect,
    }


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ts = datetime.now(timezone.utc).isoformat()

    results = {
        "date": today,
        "checked_at": ts,
        "checked_from": "sydney-au",
        "portals": {},
    }

    for pid, name, url, agency, tier in PORTALS:
        print(f"  Checking {name} ({url})...", end=" ", flush=True)
        r = check_url(url)
        r["name"] = name
        r["url"] = url
        r["agency"] = agency
        r["tier"] = tier
        results["portals"][pid] = r
        icon = {"up": "✅", "blocked": "⚠️", "dns_dead": "❌", "error": "❌"}.get(r["status"], "?")
        print(f"{icon} {r['http_code']} ({r['latency_ms']}ms)")

    out = DATA_DIR / f"{today}.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nSaved to {out}")

    # Also write latest.json for the status page
    latest = DATA_DIR / "latest.json"
    latest.write_text(json.dumps(results, indent=2))

    # Build index of all days
    days = sorted(p.stem for p in DATA_DIR.glob("????-??-??.json"))
    (DATA_DIR / "index.json").write_text(json.dumps(days))

    # Summary
    statuses = [r["status"] for r in results["portals"].values()]
    up = statuses.count("up")
    blocked = statuses.count("blocked")
    dead = statuses.count("dns_dead")
    err = statuses.count("error")
    total = len(statuses)
    print(f"\n✅ {up}/{total} up | ⚠️ {blocked} blocked | ❌ {dead} DNS dead | ❌ {err} error")


if __name__ == "__main__":
    main()
