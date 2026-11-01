from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APP_NAME = "سعّر"
DB_DIR = ROOT / "backend" / "instance"
DB_PATH = DB_DIR / "siarad.sqlite"
LISTINGS_CSV = ROOT / "data" / "processed" / "listings.csv"
IMAGES_CSV = ROOT / "data" / "processed" / "images.csv"
UPLOAD_DIR = ROOT / "tmp" / "siarad_uploads"
IDENTITY_CACHE_DIR = DB_DIR / "cache" / "identity"
IMAGE_PRICE_CACHE_DIR = DB_DIR / "cache" / "image_price"
IMAGE_PRICE_RUNTIME = ROOT / "models" / "image_price_hamoud_20261028"
IMAGE_PRICE_POINTER = ROOT / "models" / "image_price_current.json"
IDENTITY_POINTER = ROOT / "models" / "identity_current.json"
TABULAR_POINTER = ROOT / "models" / "price_current.json"
MAX_UPLOAD_BYTES = 15 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000
