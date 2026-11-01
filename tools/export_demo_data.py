#!/usr/bin/env python3
"""Export a privacy-filtered static demo snapshot from the local API."""

from __future__ import annotations

import hashlib
import json
import math
import mimetypes
from pathlib import Path
from typing import Any

import requests


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "frontend" / "public" / "demo"
API = "http://127.0.0.1:8012/api"
PLACEHOLDER = "/demo/placeholder.svg"
TIMEOUT = 30
LISTING_FIELDS = (
    "listing_id", "make", "model", "year", "price_sar", "mileage_km", "city", "trim",
    "body", "color", "transmission", "fuel", "condition", "listing_date", "image_count",
    "image_url", "historical",
)


def get(path: str, *, params: dict[str, Any] | None = None) -> Any:
    response = requests.get(f"{API}{path}", params=params, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()


def post_json(path: str, payload: dict[str, Any]) -> Any:
    response = requests.post(f"{API}{path}", json=payload, timeout=1000)
    response.raise_for_status()
    return response.json()


def safe_text(value: Any) -> Any:
    if isinstance(value, str):
        value = value.replace("سياراد", "سعّر").replace("Siyarad", "Saer").replace("siarad", "saer")
    elif isinstance(value, list):
        return [safe_text(item) for item in value]
    elif isinstance(value, dict):
        return {safe_text(key): safe_text(item) for key, item in value.items()}
    return value


def listing(row: dict[str, Any], ids: dict[str, str]) -> dict[str, Any]:
    result = {key: row.get(key) for key in LISTING_FIELDS}
    original_id = str(row.get("listing_id", ""))
    if original_id not in ids:
        raise RuntimeError("تعذر ربط سجل الإعلان بمعرّف العرض.")
    result["listing_id"] = ids[original_id]
    result["image_url"] = PLACEHOLDER if row.get("image_url") else None
    result["image_count"] = int(row.get("image_count") or 0)
    result["historical"] = True
    return safe_text(result)


def get_all_listings() -> list[dict[str, Any]]:
    first = get("/listings", params={"offset": 0, "limit": 100})
    total = int(first.get("total") or 0)
    rows = list(first.get("items") or [])
    for offset in range(100, total, 100):
        rows.extend(get("/listings", params={"offset": offset, "limit": 100}).get("items") or [])
    if len(rows) < min(total, 100):
        raise RuntimeError("لم تكتمل قراءة صفحات الإعلانات من API المحلي.")
    return rows


def pick_sample(all_rows: list[dict[str, Any]], featured: list[dict[str, Any]], recommendations: dict[str, Any]) -> list[dict[str, Any]]:
    by_id = {str(row["listing_id"]): row for row in all_rows}
    chosen: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(row: dict[str, Any]) -> None:
        key = str(row.get("listing_id", ""))
        source = by_id.get(key, row)
        if key and key not in seen and len(chosen) < 30:
            chosen.append(source)
            seen.add(key)

    for row in featured:
        add(row)
    for row in recommendations.get("items", []):
        add(row)
    for dimension in (
        lambda row: row.get("make"),
        lambda row: row.get("city"),
        lambda row: (row.get("year") or 0) // 3 if row.get("year") else None,
    ):
        present = {dimension(row) for row in chosen}
        for row in all_rows:
            value = dimension(row)
            if value is not None and value not in present:
                add(row)
                present.add(value)
                if len(chosen) >= 30:
                    break
    for row in all_rows:
        add(row)
        if len(chosen) >= 30:
            break
    if not chosen:
        raise RuntimeError("لم يرجع الخادم إعلانات صالحة للعينة.")
    return chosen


def sample_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    prices = [float(row["price_sar"]) for row in rows if isinstance(row.get("price_sar"), (int, float)) and math.isfinite(float(row["price_sar"])) and float(row["price_sar"]) > 0]
    with_images = sum(1 for row in rows if int(row.get("image_count") or 0) > 0)
    ordered = sorted(prices)
    middle = len(ordered) // 2
    med = (ordered[middle] if len(ordered) % 2 else (ordered[middle - 1] + ordered[middle]) / 2) if ordered else None
    return {
        "priced_count": len(prices),
        "median_price": med,
        "average_price": sum(prices) / len(prices) if prices else None,
        "with_images": with_images,
        "image_coverage_pct": 100 * with_images / len(rows) if rows else 0,
    }


def export_tabular_examples(all_rows: list[dict[str, Any]], pricing: dict[str, Any]) -> list[dict[str, Any]]:
    pairs = pricing.get("pairs") or {}
    available = {(str(make), str(model)) for make, models in pairs.items() for model in models}
    examples: list[dict[str, Any]] = []
    seen_pairs: set[tuple[str, str]] = set()
    for row in all_rows:
        make, model = str(row.get("make") or ""), str(row.get("model") or "")
        if (make, model) not in available or (make, model) in seen_pairs or row.get("year") is None or row.get("mileage_km") is None:
            continue
        input_data = {
            "make": make,
            "model_std": model,
            "year": int(row["year"]),
            "km_mileage": float(row["mileage_km"]),
            "trim_std": "",
            "transmission": "",
            "type_fuel": "",
            "condition": "used",
        }
        try:
            output = post_json("/estimate-tabular", input_data)
            price = output.get("سعر_الإعلان_المقدر_ريال")
            if isinstance(price, (int, float)) and math.isfinite(float(price)):
                examples.append({
                    "input": input_data,
                    "output": {"سعر_الإعلان_المقدر_ريال": price, "notice": "نتيجة محفوظة من تشغيل النموذج المحلي؛ ليست تقديرًا حيًا."},
                })
                seen_pairs.add((make, model))
        except requests.RequestException:
            continue
        if len(examples) == 3:
            break
    return examples


def model_result_identity(result: dict[str, Any]) -> dict[str, Any]:
    primary = result.get("الاقتراح_الرئيسي") or {}
    alternatives = []
    for item in primary.get("أفضل_الاحتمالات", []) or []:
        category = item.get("الفئة")
        confidence = item.get("درجة_غير_معايرة")
        if isinstance(category, str) and isinstance(confidence, (int, float)):
            alternatives.append({"الفئة": category, "درجة_غير_معايرة": confidence})
    return safe_text({
        "الاقتراح_الرئيسي": {
            "الماركة": primary.get("الماركة"),
            "الموديل": primary.get("الموديل"),
            "درجة_غير_معايرة": primary.get("درجة_غير_معايرة"),
            "أفضل_الاحتمالات": alternatives,
        }
    })


def export_image_examples(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    examples: list[dict[str, Any]] = []
    seen_digests: set[str] = set()
    seen_models: set[tuple[str, str]] = set()
    for row in rows:
        if int(row.get("image_count") or 0) <= 0:
            continue
        model_key = (str(row.get("make") or ""), str(row.get("model") or ""))
        if model_key in seen_models:
            continue
        try:
            detail = get(f"/listings/{requests.utils.quote(str(row['listing_id']), safe='')}")
            photos = detail.get("images") or []
            if not photos:
                continue
            image_response = requests.get(f"http://127.0.0.1:8012{photos[0]['url']}", timeout=60)
            image_response.raise_for_status()
            data = image_response.content
            digest = hashlib.sha256(data).hexdigest()
            if digest in seen_digests:
                continue
            content_type = image_response.headers.get("Content-Type") or mimetypes.guess_type(str(photos[0].get("url", "")))[0] or "image/jpeg"
            extension = "webp" if "webp" in content_type else "png" if "png" in content_type else "jpg"
            files = {"file": (f"example.{extension}", data, content_type)}
            identity_response = requests.post(f"{API}/recognize", files=files, timeout=1000)
            identity_response.raise_for_status()
            price_response = requests.post(f"{API}/estimate-image-price", files=files, timeout=1000)
            price_response.raise_for_status()
            identity = model_result_identity(identity_response.json())
            primary = identity["الاقتراح_الرئيسي"]
            estimate = price_response.json()
            if not primary.get("الماركة") or not primary.get("الموديل") or not isinstance(estimate.get("price_sar"), (int, float)):
                continue
            examples.append({
                "sha256": digest,
                "estimate": {
                    "price_sar": estimate.get("price_sar"),
                    "range_80_sar": estimate.get("range_80_sar"),
                    "range_90_sar": estimate.get("range_90_sar"),
                    "notice_ar": "نتيجة محفوظة من تشغيل النموذج المحلي؛ ليست تقديرًا حيًا.",
                    "notice": "نتيجة محفوظة من تشغيل النموذج المحلي؛ ليست تقديرًا حيًا.",
                },
                "identity": identity,
            })
            seen_models.add(model_key)
            seen_digests.add(digest)
        except requests.RequestException:
            continue
        if len(examples) == 3:
            break
    return examples


def write_json(name: str, value: Any) -> int:
    path = OUTPUT / f"{name}.json"
    content = json.dumps(safe_text(value), ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    path.write_text(content, encoding="utf-8")
    return path.stat().st_size


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    health = get("/health")
    meta = get("/meta")
    brands = get("/brands")
    pricing = get("/pricing-options")
    market = get("/market")
    featured = get("/featured")
    recommendations = get("/recommendations", params={"min_price": 0, "max_price": 1_000_000_000})
    all_rows = get_all_listings()
    selected = pick_sample(all_rows, featured, recommendations)

    id_map = {str(row["listing_id"]): f"demo-{index + 1:04d}" for index, row in enumerate(all_rows)}
    api_featured = [listing(row, id_map) for row in featured if str(row.get("listing_id")) in id_map]
    api_recommendations = {
        **recommendations,
        "items": [listing(row, id_map) for row in recommendations.get("items", []) if str(row.get("listing_id")) in id_map],
    }
    selected_safe = [listing(row, id_map) for row in all_rows]
    summary = sample_summary(all_rows)
    compare = post_json("/compare", {"listing_ids": [selected[0]["listing_id"], selected[1]["listing_id"]]}) if len(selected) > 1 else None
    if compare:
        compare["items"] = [listing(row, id_map) for row in compare.get("items", [])]

    health["app"] = "سعّر"
    meta["app_name"] = "سعّر"
    exported: dict[str, Any] = {
        "health": safe_text(health),
        "meta": safe_text(meta),
        "brands": safe_text(brands),
        "pricing-options": safe_text(pricing),
        "market": safe_text(market),
        "featured": api_featured,
        "recommendations": safe_text(api_recommendations),
        "compare": safe_text(compare),
        "listings": {"items": selected_safe, "total": len(selected_safe), "offset": 0, "limit": len(selected_safe), "summary": summary},
    }
    tabular = export_tabular_examples(all_rows, pricing)
    image_examples = export_image_examples(selected)
    exported["model-examples"] = {"tabular": tabular, "images": image_examples}

    sizes = {name: write_json(name, value) for name, value in exported.items()}
    total_size = sum(sizes.values())
    print(f"تم التصدير: {len(selected_safe)} إعلاناً؛ {len(api_featured)} مميزة؛ {len(api_recommendations['items'])} توصية؛ {len(tabular)} مثال مواصفات؛ {len(image_examples)} أمثلة صورة وهوية.")
    print(f"حجم ملفات JSON: {total_size:,} بايت.")
    print("أحجام الملفات:")
    for name, size in sorted(sizes.items()):
        print(f"- {name}.json: {size:,} بايت")
    if len(tabular) != 3 or len(image_examples) != 3:
        raise RuntimeError("لم تتوفر ثلاثة أمثلة ناجحة لكل مسار نموذج؛ لا تُستكمل نسخة العرض بنماذج مزيفة.")


if __name__ == "__main__":
    main()
