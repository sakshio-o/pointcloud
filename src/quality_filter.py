import cv2
import os
import numpy as np
from tqdm import tqdm
from skimage.metrics import structural_similarity as ssim

# ── CONFIG ──────────────────────────────────────────────
INPUT_DIR      = "data/frames"
OUTPUT_DIR     = "data/filtered"
BLUR_THRESHOLD = 20.0   # lower = more blurry frames removed
SSIM_THRESHOLD = 0.92    # higher = stricter duplicate removal
# ────────────────────────────────────────────────────────

def laplacian_variance(image):
    """Higher = sharper image."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def is_duplicate(img1, img2, threshold):
    """Returns True if two frames are too similar."""
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    gray1 = cv2.resize(gray1, (320, 320))
    gray2 = cv2.resize(gray2, (320, 320))
    score, _ = ssim(gray1, gray2, full=True)
    return score > threshold

def filter_frames(input_dir, output_dir, blur_threshold, ssim_threshold):
    os.makedirs(output_dir, exist_ok=True)

    files = sorted([
        f for f in os.listdir(input_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

    if not files:
        print("ERROR: No images found in", input_dir)
        return

    print(f"\n Quality Filter")
    print(f"  Input frames  : {len(files)}")
    print(f"  Blur threshold: {blur_threshold}")
    print(f"  SSIM threshold: {ssim_threshold}\n")

    saved        = 0
    removed_blur = 0
    removed_dup  = 0
    last_saved   = None

    for fname in tqdm(files, desc="Filtering", unit="frame"):
        fpath = os.path.join(input_dir, fname)
        img   = cv2.imread(fpath)

        if img is None:
            continue

        # ── Blur check ──
        blur_score = laplacian_variance(img)
        if blur_score < blur_threshold:
            removed_blur += 1
            continue

        # ── Duplicate check ──
        if last_saved is not None and is_duplicate(img, last_saved, ssim_threshold):
            removed_dup += 1
            continue

        # ── Save good frame ──
        out_path = os.path.join(output_dir, f"filtered_{saved:04d}.jpg")
        cv2.imwrite(out_path, img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        last_saved = img
        saved += 1

    print(f"\n Done!")
    print(f"  Kept          : {saved}")
    print(f"  Removed (blur): {removed_blur}")
    print(f"  Removed (dup) : {removed_dup}")
    print(f"  Output folder : {output_dir}")

    if saved < 50:
        print(f"\n  WARNING: Only {saved} frames kept.")
        print(f"  Consider lowering BLUR_THRESHOLD or SSIM_THRESHOLD.")
    elif saved > 200:
        print(f"\n  TIP: {saved} frames is a lot. COLMAP will be slow.")
        print(f"  Consider raising SSIM_THRESHOLD to 0.95 to reduce further.")
    else:
        print(f"\n  Good frame count for COLMAP reconstruction.")

if __name__ == "__main__":
    filter_frames(INPUT_DIR, OUTPUT_DIR, BLUR_THRESHOLD, SSIM_THRESHOLD)
