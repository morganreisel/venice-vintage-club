#!/usr/bin/env python3
"""
Venice Vintage Club — Google Drive → Site Image Sync

Pulls photos from a shared Google Drive folder (organized by section),
converts/optimizes them, and updates index.html with new image references.

Drive folder structure expected:
  VVC Media/
    HERO/       → 1 image (hero background)
    MOOD/       → slideshow images
    COMMUNITY/  → filmstrip carousel images
    SPACE/      → venue photos (2-column split)
    LOOKBOOK/   → lookbook filmstrip images
    EVENT/      → 1 image (event background)
    DROP/       → product images (up to 4)

Usage:
    python3 sync-drive.py [--replace]

    --replace   Replace ALL section images (default on first run)
                Without this flag, new images are ADDED to existing ones.
"""

import os
import sys
import subprocess
import shutil
import re
import json
import hashlib
from pathlib import Path
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────────
DRIVE_FOLDER_ID = "1RQYXWqeBc-NXHm_OqCLkf6MBkUJVUGAu"
PROJECT_DIR = Path(__file__).parent
IMAGES_DIR = PROJECT_DIR / "images"
INDEX_HTML = PROJECT_DIR / "index.html"
STAGING_DIR = PROJECT_DIR / ".drive-staging"
MANIFEST_FILE = PROJECT_DIR / ".drive-manifest.json"

# Find gdown — works on macOS local install or Linux (GitHub Actions)
GDOWN_PATH = shutil.which("gdown") or os.path.expanduser("~/Library/Python/3.9/bin/gdown")
IS_LINUX = sys.platform.startswith("linux")

# Max image dimensions per section (width x height)
IMAGE_SIZES = {
    "hero": (2400, 1600),
    "mood": (1920, 1280),
    "community": (800, 1000),
    "space": (1200, 900),
    "lookbook": (800, 1000),
    "event": (2400, 1600),
    "drop": (800, 1000),
}

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".webp"}


def log(msg):
    print(f"  [sync] {msg}")


def load_manifest():
    """Load the sync manifest (tracks what's been synced before)."""
    if MANIFEST_FILE.exists():
        with open(MANIFEST_FILE) as f:
            return json.load(f)
    return {"synced_files": {}, "last_sync": None}


def save_manifest(manifest):
    """Save the sync manifest."""
    manifest["last_sync"] = datetime.now().isoformat()
    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2)


def download_from_drive():
    """Download the entire Drive folder structure to staging."""
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
    STAGING_DIR.mkdir()

    log(f"Downloading from Google Drive folder {DRIVE_FOLDER_ID}...")
    result = subprocess.run(
        [
            GDOWN_PATH, "--folder",
            f"https://drive.google.com/drive/folders/{DRIVE_FOLDER_ID}",
            "--remaining-ok",
            "-O", str(STAGING_DIR),
        ],
        capture_output=True, text=True, timeout=600
    )
    if result.returncode != 0:
        log(f"Warning: gdown exited with code {result.returncode}")
        log(result.stderr[-500:] if result.stderr else "No stderr")

    # List what we got
    sections_found = []
    for item in sorted(STAGING_DIR.iterdir()):
        if item.is_dir():
            files = list(item.iterdir())
            sections_found.append((item.name, len(files)))
            log(f"  {item.name}: {len(files)} files")

    return sections_found


def file_hash(filepath):
    """Get a quick hash of a file for change detection."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def convert_and_optimize(src_path, dest_path, section):
    """Convert image to JPG and resize for web. Uses ImageMagick on Linux, sips on macOS."""
    max_w, max_h = IMAGE_SIZES.get(section, (1200, 1000))
    max_dim = max(max_w, max_h)
    ext = src_path.suffix.lower()

    if IS_LINUX:
        # ImageMagick: convert + resize + optimize in one command
        subprocess.run(
            ["convert", str(src_path),
             "-resize", f"{max_dim}x{max_dim}>",
             "-quality", "85",
             "-strip",
             str(dest_path)],
            capture_output=True, timeout=120
        )
    else:
        # macOS: use sips
        if ext in {".heic", ".tif", ".tiff", ".png", ".webp"}:
            subprocess.run(
                ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "85",
                 str(src_path), "--out", str(dest_path)],
                capture_output=True, timeout=60
            )
        else:
            shutil.copy2(src_path, dest_path)

        if dest_path.exists():
            subprocess.run(
                ["sips", "--resampleHeightWidthMax", str(max_dim),
                 str(dest_path)],
                capture_output=True, timeout=60
            )

    return dest_path.exists()


def process_section(section_name, staging_path, replace_mode):
    """Process downloaded files for one section → images/ directory."""
    section = section_name.lower()
    src_dir = staging_path / section_name

    if not src_dir.exists() or not src_dir.is_dir():
        log(f"  Skipping {section_name} (not found in download)")
        return []

    # Get all image files, sorted by name
    image_files = sorted([
        f for f in src_dir.iterdir()
        if f.suffix.lower() in SUPPORTED_EXTENSIONS
    ])

    if not image_files:
        log(f"  Skipping {section_name} (no images)")
        return []

    # Generate destination filenames: section-01.jpg, section-02.jpg, etc.
    new_images = []
    existing = []

    if not replace_mode:
        # Find existing section images to determine next number
        existing = sorted(IMAGES_DIR.glob(f"{section}-[0-9][0-9].jpg"))

    start_num = len(existing) + 1 if not replace_mode else 1

    for i, src_file in enumerate(image_files):
        num = start_num + i
        dest_name = f"{section}-{num:02d}.jpg"
        dest_path = IMAGES_DIR / dest_name

        log(f"  Converting {src_file.name} → {dest_name}")
        if convert_and_optimize(src_file, dest_path, section):
            new_images.append(dest_name)
        else:
            log(f"  !! Failed to convert {src_file.name}")

    # If replacing, remove old section images that aren't in the new set
    if replace_mode:
        for old_file in IMAGES_DIR.glob(f"{section}-[0-9][0-9].jpg"):
            if old_file.name not in new_images:
                old_file.unlink()
                log(f"  Removed old {old_file.name}")

    return new_images


def update_html_hero(html, images):
    """Update the hero background image."""
    if not images:
        return html
    # Replace the background: url(...) in .hero-bg
    old_pattern = r"(background:\s*url\('images/)[^']+('\)\s*center/cover)"
    new_ref = f"\\g<1>{images[0]}\\2"
    return re.sub(old_pattern, new_ref, html)


def update_html_mood(html, images):
    """Update the mood slideshow images."""
    if not images:
        return html
    # Build new slideshow img tags
    img_tags = []
    for i, img in enumerate(images):
        active = ' class="active"' if i == 0 else ''
        img_tags.append(
            f'        <img src="images/{img}" alt="Venice Vintage Club"{active} loading="lazy">'
        )
    img_block = "\n".join(img_tags)

    # Replace everything between mood-slideshow opening and the arrow buttons
    pattern = (
        r'(<div class="mood-slideshow"[^>]*>)\s*\n'
        r'(.*?)'
        r'(\s*<button class="slide-arrow)'
    )
    replacement = f'\\1\n{img_block}\n\\3'
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def build_filmstrip_html(images, section_label):
    """Build filmstrip frames HTML for community/lookbook sections."""
    frames = []
    for img in images:
        frames.append(
            f'                    <div class="filmstrip-frame">'
            f'<img src="images/{img}" alt="{section_label}" loading="lazy">'
            f'</div>'
        )
    # Duplicate for seamless loop
    set_a = "\n".join(frames)
    set_b = "\n".join(frames)
    return f"{set_a}\n                    <!-- Duplicate for seamless loop -->\n{set_b}"


def update_html_community(html, images):
    """Update the community filmstrip carousel."""
    if not images:
        return html
    new_frames = build_filmstrip_html(images, "Venice Vintage Club")
    # Replace the filmstrip-track contents in the community section
    pattern = (
        r'(<!-- Section 4: Community.*?<div class="filmstrip-track"[^>]*>)\s*\n'
        r'(.*?)'
        r'(\s*</div>\s*</div>\s*<div class="community-carousel-overlay")'
    )
    replacement = f"\\1\n{new_frames}\n\\3"
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def update_html_space(html, images):
    """Update the space section images (2-column split)."""
    if not images:
        return html
    # Take first 2 images, label them
    labels = ["The Garage", "The Office"]
    split_items = []
    for i, img in enumerate(images[:2]):
        label = labels[i] if i < len(labels) else f"Space {i+1}"
        split_items.append(
            f'            <div class="community-split-img">\n'
            f'                <img src="images/{img}" alt="{label}">\n'
            f'                <span class="corner-label">{label}</span>\n'
            f'            </div>'
        )
    new_split = "\n".join(split_items)

    pattern = (
        r'(<div class="community-split">)\s*\n'
        r'(.*?)'
        r'(\s*</div>\s*</section>\s*\n\s*<!-- Section 6: Lookbook)'
    )
    replacement = f"\\1\n{new_split}\n\\3"
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def update_html_lookbook(html, images):
    """Update the lookbook filmstrip."""
    if not images:
        return html
    # Build Set A and Set B
    frames_a = []
    for img in images:
        frames_a.append(
            f'                <div class="filmstrip-frame">'
            f'<img src="images/{img}" alt="Lookbook">'
            f'</div>'
        )
    set_a = "\n".join(frames_a)
    set_b = "\n".join(frames_a)  # duplicate for loop
    new_filmstrip = f"                <!-- Set A -->\n{set_a}\n                <!-- Set B (duplicate for seamless loop) -->\n{set_b}"

    pattern = (
        r'(<!-- Section 6: Lookbook.*?<div class="filmstrip-track">)\s*\n'
        r'(.*?)'
        r'(\s*</div>\s*</div>\s*</section>\s*\n\s*<!-- Section 8:)'
    )
    replacement = f"\\1\n{new_filmstrip}\n\\3"
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def update_html_event(html, images):
    """Update the event section background image."""
    if not images:
        return html
    pattern = r'(<div class="event-bg">\s*<img src="images/)[^"]+(")'
    replacement = f"\\g<1>{images[0]}\\2"
    return re.sub(pattern, replacement, html, flags=re.DOTALL)


def update_html_drop(html, images):
    """Update the drop product images (replace globe watermarks with actual photos)."""
    if not images:
        return html
    # Replace each drop item's image, up to 4
    for i, img in enumerate(images[:4]):
        # Find the i-th drop-item and replace its image
        pattern = r'(<div class="item-image">\s*)<img src="images/[^"]*"[^>]*>'
        count = 0
        def replacer(match):
            nonlocal count
            count += 1
            if count == i + 1:
                return f'{match.group(1)}<img src="images/{img}" alt="Product photo" class="product-photo">'
            return match.group(0)
        html = re.sub(pattern, replacer, html)
    return html


def update_index_html(section_images, replace_mode):
    """Read index.html, update image references, write back."""
    log("Updating index.html...")
    with open(INDEX_HTML, "r") as f:
        html = f.read()

    original = html

    # Apply section updates
    updaters = {
        "hero": update_html_hero,
        "mood": update_html_mood,
        "community": update_html_community,
        "space": update_html_space,
        "lookbook": update_html_lookbook,
        "event": update_html_event,
        "drop": update_html_drop,
    }

    for section, images in section_images.items():
        if images and section in updaters:
            log(f"  Updating {section} with {len(images)} images")
            html = updaters[section](html, images)

    if html != original:
        with open(INDEX_HTML, "w") as f:
            f.write(html)
        log("index.html updated!")
    else:
        log("No HTML changes needed.")


def main():
    replace_mode = "--replace" in sys.argv
    log(f"Mode: {'REPLACE' if replace_mode else 'ADD'}")
    log(f"Project: {PROJECT_DIR}")
    log(f"Started: {datetime.now().isoformat()}")

    # Step 1: Download from Drive
    sections_found = download_from_drive()
    if not sections_found:
        log("No sections found in Drive. Exiting.")
        return

    # Step 2: Process each section
    section_images = {}
    for section_name, _ in sections_found:
        section = section_name.lower()
        log(f"\nProcessing {section_name}...")
        images = process_section(section_name, STAGING_DIR, replace_mode)
        if images:
            section_images[section] = images
            log(f"  → {len(images)} images ready")

    # Step 3: Update HTML
    if section_images:
        update_index_html(section_images, replace_mode)
    else:
        log("No images to update.")

    # Step 4: Clean up staging
    if STAGING_DIR.exists():
        shutil.rmtree(STAGING_DIR)
        log("Cleaned up staging directory.")

    # Step 5: Save manifest
    manifest = load_manifest()
    for section, images in section_images.items():
        manifest["synced_files"][section] = images
    save_manifest(manifest)

    # Summary
    log("\n✓ Sync complete!")
    for section, images in section_images.items():
        log(f"  {section}: {len(images)} images")
    log(f"\nNext step: review changes, then commit and push to deploy.")


if __name__ == "__main__":
    main()
