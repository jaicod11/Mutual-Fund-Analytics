import requests
import pandas as pd
import os

# ──────────────────────────────────────────────
# SCHEMES TO FETCH
# ──────────────────────────────────────────────
schemes = {
    "HDFC_Top100_Direct": 125497,
    "SBI_Bluechip":        119551,
    "ICICI_Bluechip":      120503,
    "Nippon_LargeCap":     118632,
    "Axis_Bluechip":       119092,
    "Kotak_Bluechip":      120841,
}

os.makedirs("data/raw", exist_ok=True)

print("=" * 60)
print("  FETCHING LIVE NAV DATA FROM mfapi.in")
print("=" * 60)

for name, code in schemes.items():
    print(f"\n⬇️  Fetching: {name} (code: {code})")

    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        print(f"   ❌ Failed — HTTP {response.status_code}")
        continue

    data = response.json()

    # Parse JSON response
    df = pd.DataFrame(data["data"])   # columns: 'date', 'nav'
    df["scheme_name"] = name
    df["scheme_code"] = code

    # Save to CSV
    output_path = f"data/raw/nav_{name}.csv"
    df.to_csv(output_path, index=False)

    print(f"   ✅ Saved → {output_path}")
    print(f"   Records : {len(df)}")
    print(f"   Latest NAV: {df.iloc[0]['date']} → ₹{df.iloc[0]['nav']}")

print("\n" + "=" * 60)
print("  ✅ ALL NAV DATA FETCHED SUCCESSFULLY")
print("=" * 60)