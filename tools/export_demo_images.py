#!/usr/bin/env python3
"""Build the local, anonymized static-demo image corpus from processed manifests.

This script reads source data only. It writes re-encoded WebP files and updates
the local demo JSON; generated files are ignored by Git.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageOps


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def number_key(value: object) -> str:
    if value is None or value == "":
        return ""
    try:
        return str(float(value))
    except (TypeError, ValueError):
        return str(value).strip().casefold()


def source_listings_in_demo_order(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    # The demo export follows /api/listings default order: date descending,
    # null dates last, and listing_uid ascending for ties.
    rows.sort(key=lambda row: row.get("listing_uid", ""))
    rows.sort(key=lambda row: row.get("listing_date") or "", reverse=True)
    return rows


def verify_alignment(demo_rows: list[dict], source_rows: list[dict[str, str]]) -> None:
    if len(demo_rows) != len(source_rows):
        raise RuntimeError(f"Listing count mismatch: demo={len(demo_rows)} source={len(source_rows)}")
    mapping = {
        "make": "make",
        "model": "model",
        "year": "year",
        "price_sar": "sar_price",
        "mileage_km": "km_mileage",
        "city": "city",
        "trim": "trim",
        "listing_date": "listing_date",
    }
    errors = []
    for index, (demo, source) in enumerate(zip(demo_rows, source_rows), start=1):
        for demo_key, source_key in mapping.items():
            left, right = demo.get(demo_key), source.get(source_key)
            if demo_key in {"year", "price_sar", "mileage_km"}:
                equal = number_key(left) == number_key(right)
            else:
                equal = str(left or "").strip().casefold() == str(right or "").strip().casefold()
            if not equal:
                errors.append((index, demo_key))
                break
    if errors:
        raise RuntimeError(f"Demo/source row alignment failed at {len(errors)} rows; first={errors[:5]}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, default=Path(r"C:\CAR"))
    parser.add_argument("--frontend-root", type=Path, default=Path(__file__).resolve().parents[1] / "frontend")
    parser.add_argument("--max-edge", type=int, default=1024)
    parser.add_argument("--quality", type=int, default=78)
    parser.add_argument("--method", type=int, default=4, help="WebP encoder effort; higher values are slower")
    args = parser.parse_args()
    source_root = args.source_root.resolve()
    frontend_root = args.frontend_root.resolve()
    demo_json_path = frontend_root / "public" / "demo" / "listings.json"
    image_manifest = load_csv(source_root / "data" / "processed" / "images.csv")
    source_listings = source_listings_in_demo_order(load_csv(source_root / "data" / "processed" / "listings.csv"))
    demo = json.loads(demo_json_path.read_text(encoding="utf-8"))
    demo_rows = demo["items"]
    verify_alignment(demo_rows, source_listings)

    by_listing: dict[str, list[dict[str, str]]] = defaultdict(list)
    raw_hash_to_demo_path: dict[str, str] = {}
    for image in image_manifest:
        if image.get("is_valid", "").casefold() != "true":
            raise RuntimeError("Image manifest contains an invalid source image; refusing partial export.")
        by_listing[image["listing_uid"]].append(image)
    for images in by_listing.values():
        images.sort(key=lambda row: row["image_uid"])

    output_root = frontend_root / "public" / "demo" / "img"
    output_root.mkdir(parents=True, exist_ok=True)
    total_bytes = 0
    total_images = 0
    largest_file = 0
    listing_assets: dict[str, dict[str, object]] = {}
    for index, (demo_row, source_row) in enumerate(zip(demo_rows, source_listings), start=1):
        listing_uid = source_row["listing_uid"]
        source_images = by_listing.get(listing_uid, [])
        synthetic_id = str(demo_row["listing_id"])
        relative_urls = []
        for image_index, record in enumerate(source_images, start=1):
            source_path = source_root / Path(record["relative_path"])
            if not source_path.is_file():
                raise FileNotFoundError("A source image listed in the manifest is missing.")
            rel_url = f"/demo/img/{synthetic_id}/{image_index:02d}.webp"
            target = output_root / synthetic_id / f"{image_index:02d}.webp"
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.is_file():
                with Image.open(source_path) as opened:
                    image = ImageOps.exif_transpose(opened)
                    if image.mode not in {"RGB", "RGBA"}:
                        image = image.convert("RGBA" if "transparency" in image.info else "RGB")
                    image.thumbnail((args.max_edge, args.max_edge), Image.Resampling.LANCZOS)
                    image.save(target, "WEBP", quality=args.quality, method=args.method)
            file_size = target.stat().st_size
            total_bytes += file_size
            total_images += 1
            largest_file = max(largest_file, file_size)
            relative_urls.append(rel_url)
            raw_hash_to_demo_path[record["sha256"].casefold()] = rel_url
        demo_row["images"] = relative_urls
        demo_row["image_count"] = len(relative_urls)
        demo_row["image_url"] = relative_urls[0] if relative_urls else None
        listing_assets[synthetic_id] = {
            "images": relative_urls,
            "image_count": len(relative_urls),
            "image_url": relative_urls[0] if relative_urls else None,
        }
        if index % 250 == 0:
            print(f"processed listings={index}; images={total_images}")

    demo_json_path.write_text(json.dumps(demo, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    examples_path = frontend_root / "public" / "demo" / "model-examples.json"
    if examples_path.exists():
        examples = json.loads(examples_path.read_text(encoding="utf-8"))
        for example in examples.get("images", []):
            image_path = raw_hash_to_demo_path.get(str(example.get("sha256", "")).casefold())
            if image_path:
                target = frontend_root / "public" / image_path.lstrip("/")
                example["sha256"] = sha256(target)
                example["image_url"] = image_path
        examples_path.write_text(json.dumps(examples, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Other generated demo JSON files can also contain listing cards (for
    # example the default budget recommendations). Point them at the same
    # first real photo and retain the full gallery manifest.
    def patch_listing_assets(value: object) -> None:
        if isinstance(value, dict):
            asset = listing_assets.get(str(value.get("listing_id", "")))
            if asset:
                value.update(asset)
            for child in value.values():
                patch_listing_assets(child)
        elif isinstance(value, list):
            for child in value:
                patch_listing_assets(child)

    for json_path in (frontend_root / "public" / "demo").glob("*.json"):
        if json_path in {demo_json_path, examples_path}:
            continue
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        patch_listing_assets(payload)
        json_path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")

    unmatched = len([row for row in source_listings if not by_listing.get(row["listing_uid"])])
    if unmatched:
        raise RuntimeError(f"{unmatched} demo listings have no source photos.")
    if total_images != len(image_manifest):
        raise RuntimeError(f"Image count mismatch: exported={total_images}, manifest={len(image_manifest)}")
    print(json.dumps({
        "listings": len(demo_rows),
        "images": total_images,
        "total_bytes": total_bytes,
        "largest_file_bytes": largest_file,
        "max_edge": args.max_edge,
        "quality": args.quality,
        "method": args.method,
        "unmatched_listings": unmatched,
        "output": str(output_root),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
