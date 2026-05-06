# Vision-Based 3D Digital Pointcloud Generator

> Record a 360° video of any object. Get a fully textured 3D point cloud and mesh back.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-red?style=flat-square&logo=opencv)
![Open3D](https://img.shields.io/badge/Open3D-0.19+-green?style=flat-square)
![COLMAP](https://img.shields.io/badge/COLMAP-4.x-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

---

## What is this?

Pointcloud From Video is a complete computer vision pipeline that converts a simple phone video into an interactive 3D reconstruction using **Structure from Motion (SfM)** and **Multi-View Stereo (MVS)**.

Record a shoe → get a colored 3D point cloud.  
Record a helmet → get a textured surface mesh.  
Record any rigid object → rotate and inspect it live in 3D.

---

## Demo

| Step | What happens |
|------|-------------|
| Record 360° video | Walk slowly around any object |
| Frame extraction | Video split into individual frames |
| Quality filtering | Blurry and duplicate frames removed |
| COLMAP reconstruction | Camera poses + sparse point cloud computed |
| Mesh generation | Point cloud converted to surface mesh |
| 3D viewer | Rotate, zoom, pan your digital twin |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frame extraction | OpenCV |
| Blur detection | Laplacian variance |
| Duplicate removal | SSIM (scikit-image) |
| 3D Reconstruction | COLMAP (SfM + MVS) |
| Mesh generation | Open3D Poisson reconstruction |
| Visualization | Open3D interactive viewer |
| Language | Python 3.10 |

---

## Project Structure

```
pointcloud-from-video/
│
├── data/
│   ├── videos/            # Input video goes here
│   ├── frames/            # Extracted frames
│   └── filtered/          # Quality filtered frames
│
├── outputs/
│   ├── sparse/            # COLMAP sparse model
│   ├── dense/             # COLMAP dense model
│   └── meshes/            # Final .ply and .obj files
│
├── src/
│   ├── frame_extractor.py # Video → frames
│   ├── check.py           # Check blur score
│   ├── quality_filter.py  # Remove bad frames
│   ├── reconstruction.py  # COLMAP pipeline
│   ├── mesh_generator.py  # Point cloud → mesh
│   └── visualizer.py      # Interactive 3D viewer
│
├── main.py                # Single entry point with menu
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/pointcloud-from-video.git
cd pointcloud-from-video
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install COLMAP
- Download from [github.com/colmap/colmap/releases](https://github.com/colmap/colmap/releases)
- Extract to `C:\colmap\`
- Add `C:\colmap\` to system PATH
- Verify with `colmap -h`

### 5. Run
```bash
python main.py
```

---

## Usage

| Option | Action |
|--------|--------|
| `0` | Run full pipeline end to end |
| `1` | Frame extraction only |
| `2` | Quality filtering only |
| `3` | COLMAP reconstruction only |
| `4` | Mesh generation only |
| `5` | Launch 3D visualizer |

---

## Requirements

```
opencv-python
numpy
matplotlib
open3d
tqdm
scikit-image
```

- Python 3.10 or higher
- COLMAP 4.x with CUDA recommended
- NVIDIA GPU recommended for dense reconstruction
- Works on Windows and Linux

---

## How it works

```
360° Phone Video
      ↓
Frame Extraction       (OpenCV — split video into frames)
      ↓
Quality Filtering      (remove blurry + duplicate frames)
      ↓
Feature Extraction     (COLMAP SIFT — keypoints per image)
      ↓
Feature Matching       (COLMAP — match keypoints across frames)
      ↓
Sparse Reconstruction  (COLMAP SfM — camera poses + point cloud)
      ↓
Mesh Generation        (Open3D Poisson — surface from points)
      ↓
Interactive 3D Viewer  (Open3D — rotate, zoom, pan)
```

## Description

---

> *"Built a full SfM + MVS 3D reconstruction pipeline from scratch, converting raw phone video into a colored point cloud and textured mesh using COLMAP, OpenCV, and Open3D."*

---

## License

MIT License — free to use, modify, and distribute.
