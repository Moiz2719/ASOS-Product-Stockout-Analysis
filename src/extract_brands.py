"""Extract a brand label from product descriptions and calculate stockout metrics."""
from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "processed" / "products_cleaned.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "products_enriched.csv"

# Normalisations supported by labels visible in the supplied notebook PDF.
BRAND_ALIASES = {
    "new": "New Look",
    "river": "River Island",
    "miss": "Miss Selfridge",
    "topshopwelcome": "Topshop",
    "stradivariusjacket": "Stradivarius",
    "stradivariuslayer": "Stradivarius",
    "stradivariuslow-key": "Stradivarius",
    "jdy-low-key": "JDY",
    "columbiaexclusive": "Columbia",
    "bershkalow-key": "Bershka",
    "bershkajacket": "Bershka",
    "bershkamid-season": "Bershka",
    "asos-design": "ASOS DESIGN",
    "na-kd-x": "NA-KD",
    "other-stories": "& Other Stories",
    "river-island": "River Island",
    "miss-selfridge": "Miss Selfridge",
    "new-look": "New Look",
}


def clean_token(token: str) -> str:
    return token.strip().strip("[]{}()\"' ").strip()


def brand_from_description(value: object) -> str | None:
    """Use the first brand-like token after ' by ', as in the notebook, then normalise known cases."""
    if pd.isna(value):
        return None
    text = str(value)
    match = re.search(r"\bby\s+([^,;\]\}\"']+)", text, flags=re.IGNORECASE)
    if not match:
        return None
    phrase = clean_token(match.group(1))
    first = phrase.split()[0] if phrase else ""
    # Match longest known prefixes first so product text glued to a brand can be normalised.
    for alias, normal in sorted(BRAND_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase.casefold().startswith(alias.casefold()) or first.casefold() == alias.casefold():
            return normal
    if first:
        return first
    return None


def brand_from_url(value: object) -> str | None:
    if pd.isna(value):
        return None
    try:
        parts = [p for p in urlparse(str(value)).path.strip("/").split("/") if p]
    except ValueError:
        return None
    if not parts:
        return None
    slug = parts[0].lower()
    if slug in BRAND_ALIASES:
        return BRAND_ALIASES[slug]
    if slug == "asos-design":
        return "ASOS DESIGN"
    # Convert URL slug to a readable fallback label without pretending it's validated.
    return " ".join(word.capitalize() for word in slug.replace("_", "-").split("-") if word)


def count_stockouts(size_value: object) -> tuple[int, float]:
    """Count 'Out of stock' size entries and divide by comma-separated size entries."""
    if not isinstance(size_value, str) or not size_value.strip():
        return 0, 0.0
    entries = [part.strip() for part in size_value.split(",") if part.strip()]
    if not entries:
        return 0, 0.0
    count = sum("out of stock" in part.casefold() for part in entries)
    return int(count), float(count / len(entries))


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError("Run src/clean_data.py first; products_cleaned.csv was not found.")
    df = pd.read_csv(INPUT_FILE)

    if "description" in df.columns:
        from_description = df["description"].apply(brand_from_description)
    else:
        from_description = pd.Series([None] * len(df), index=df.index)
    if "url" in df.columns:
        from_url = df["url"].apply(brand_from_url)
    else:
        from_url = pd.Series([None] * len(df), index=df.index)

    df["Brand"] = from_description.fillna(from_url).fillna("Unknown")

    if "size" in df.columns:
        metrics = df["size"].apply(count_stockouts)
    else:
        metrics = pd.Series([(0, 0.0)] * len(df), index=df.index)
    df["Stockout_Count"] = metrics.apply(lambda x: x[0]).astype(int)
    df["Stockout_Rate"] = metrics.apply(lambda x: x[1]).astype(float)

    if "price" in df.columns:
        df["Lost_Revenue"] = pd.to_numeric(df["price"], errors="coerce").fillna(0) * df["Stockout_Count"]
    else:
        df["Lost_Revenue"] = 0.0

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved enriched products: {OUTPUT_FILE.relative_to(ROOT)}")
    print("Review distinct Brand labels before relying on brand-level findings.")


if __name__ == "__main__":
    main()
