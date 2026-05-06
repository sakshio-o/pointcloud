import os
import sys
import subprocess

print("""
╔══════════════════════════════════════════╗
║   Vision-Based 3D Digital Twin Generator ║
╚══════════════════════════════════════════╝
""")

steps = [
    ("Frame Extraction",    "src/frame_extractor.py"),
    ("Quality Filtering",   "src/quality_filter.py"),
    ("3D Reconstruction",   "src/reconstruction.py"),
    ("Mesh Generation",     "src/mesh_generator.py"),
]

print("Select step to run:")
print("  0. Run full pipeline")
for i, (name, _) in enumerate(steps, 1):
    print(f"  {i}. {name}")
print("  5. Visualize result")

choice = input("\nEnter choice (0-5): ").strip()

if choice == "0":
    for name, script in steps:
        print(f"\n{'='*50}")
        print(f"  Running: {name}")
        print(f"{'='*50}")
        result = subprocess.run([sys.executable, script])
        if result.returncode != 0:
            print(f"\nERROR in {name}. Stopping.")
            sys.exit(1)
    print("\n Pipeline complete. Run visualizer? (y/n): ", end="")
    if input().strip().lower() == "y":
        subprocess.run([sys.executable, "src/visualizer.py"])

elif choice == "5":
    subprocess.run([sys.executable, "src/visualizer.py"])

elif choice in ["1","2","3","4"]:
    name, script = steps[int(choice)-1]
    print(f"\n Running: {name}")
    subprocess.run([sys.executable, script])

else:
    print("Invalid choice.")
