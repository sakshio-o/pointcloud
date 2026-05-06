import subprocess
import os
import sys

# ── CONFIG ──────────────────────────────────────────────
IMAGE_DIR    = "data/filtered"
SPARSE_DIR   = "outputs/sparse"
DENSE_DIR    = "outputs/dense"
DATABASE     = "outputs/database.db"
# ────────────────────────────────────────────────────────

def run(cmd, step_name):
    print(f"\n{'='*60}")
    print(f"  STEP: {step_name}")
    print(f"{'='*60}")
    print(f"  CMD: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, capture_output=False, text=True)
    if result.returncode != 0:
        print(f"\n ERROR in {step_name}")
        print(f"  Return code: {result.returncode}")
        sys.exit(1)
    print(f"\n  DONE: {step_name}")

def main():
    # ── Create output dirs ──
    os.makedirs(SPARSE_DIR, exist_ok=True)
    os.makedirs(DENSE_DIR,  exist_ok=True)

    print("\n COLMAP 3D Reconstruction Pipeline")
    print(f"  Images   : {IMAGE_DIR}")
    print(f"  Sparse   : {SPARSE_DIR}")
    print(f"  Dense    : {DENSE_DIR}")
    print(f"  Database : {DATABASE}")

    # ── Step 1: Feature Extraction ──
    run([
        "colmap", "feature_extractor",
        "--database_path", DATABASE,
        "--image_path",    IMAGE_DIR,
        "--ImageReader.single_camera", "1",
    ], "Feature Extraction")

    # ── Step 2: Feature Matching ──
    run([
        "colmap", "sequential_matcher",
        "--database_path", DATABASE,
    ], "Feature Matching")

    # ── Step 3: Sparse Reconstruction (SfM) ──
    run([
        "colmap", "mapper",
        "--database_path", DATABASE,
        "--image_path",    IMAGE_DIR,
        "--output_path",   SPARSE_DIR,
    ], "Sparse Reconstruction (SfM)")

    # ── Step 4: Undistort Images ──
    run([
        "colmap", "image_undistorter",
        "--image_path",      IMAGE_DIR,
        "--input_path",      os.path.join(SPARSE_DIR, "0"),
        "--output_path",     DENSE_DIR,
        "--output_type",     "COLMAP",
    ], "Image Undistortion")

    # ── Step 5: Dense Reconstruction (MVS) ──
    run([
        "colmap", "patch_match_stereo",
        "--workspace_path",  DENSE_DIR,
        "--workspace_format","COLMAP",
        "--PatchMatchStereo.geom_consistency", "true",
    ], "Dense Reconstruction (MVS)")

    # ── Step 6: Stereo Fusion ──
    run([
        "colmap", "stereo_fusion",
        "--workspace_path",   DENSE_DIR,
        "--workspace_format", "COLMAP",
        "--input_type",       "geometric",
        "--output_path",      os.path.join(DENSE_DIR, "fused.ply"),
    ], "Stereo Fusion")

    print("\n" + "="*60)
    print("  RECONSTRUCTION COMPLETE")
    print("="*60)
    print(f"\n  Sparse model : {SPARSE_DIR}/0/")
    print(f"  Dense cloud  : {DENSE_DIR}/fused.ply")
    print(f"\n  Next step    : run mesh_generator.py")

if __name__ == "__main__":
    main()
