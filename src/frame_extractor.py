import cv2
import os
from tqdm import tqdm

# ── CONFIG ──────────────────────────────────────────────
VIDEO_PATH   = "data/videos/video.mp4"      # Add your video recording in place of video.mp4
OUTPUT_DIR   = "data/frames"
FRAME_STEP   = 1         # extract every 5th frame
MAX_FRAMES   = 300        # safety cap
# ────────────────────────────────────────────────────────

def extract_frames(video_path, output_dir, frame_step, max_frames):
    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open video: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps          = cap.get(cv2.CAP_PROP_FPS)
    width        = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height       = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"\n Video Info")
    print(f"  File        : {video_path}")
    print(f"  Resolution  : {width} x {height}")
    print(f"  FPS         : {fps:.1f}")
    print(f"  Total frames: {total_frames}")
    print(f"  Frame step  : every {frame_step} frames")
    print(f"  Max extract : {max_frames} frames\n")

    saved     = 0
    frame_idx = 0

    with tqdm(total=min(total_frames // frame_step, max_frames),
              desc="Extracting", unit="frame") as pbar:

        while cap.isOpened() and saved < max_frames:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_step == 0:
                filename = os.path.join(output_dir, f"frame_{saved:04d}.jpg")
                cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                saved += 1
                pbar.update(1)

            frame_idx += 1

    cap.release()

    print(f"\n Done!")
    print(f"  Frames saved : {saved}")
    print(f"  Output folder: {output_dir}")


if __name__ == "__main__":
    extract_frames(VIDEO_PATH, OUTPUT_DIR, FRAME_STEP, MAX_FRAMES)
