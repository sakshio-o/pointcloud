import open3d as o3d
import os

# ── CONFIG ──────────────────────────────────────────────
POINTCLOUD = "outputs/meshes/pointcloud.ply"
MESH       = "outputs/meshes/mesh.ply"
# ────────────────────────────────────────────────────────

def view_pointcloud():
    print("\n Loading point cloud...")
    pcd = o3d.io.read_point_cloud(POINTCLOUD)
    print(f"  Points: {len(pcd.points)}")
    print("\n Controls:")
    print("  Left click + drag : rotate")
    print("  Scroll            : zoom")
    print("  Right click + drag: pan")
    print("  Q or Escape       : close\n")

    o3d.visualization.draw_geometries(
        [pcd],
        window_name="Digital Twin — Point Cloud",
        width=1280,
        height=720,
        point_show_normal=False
    )

def view_mesh():
    print("\n Loading mesh...")
    mesh = o3d.io.read_triangle_mesh(MESH)
    mesh.compute_vertex_normals()
    print(f"  Vertices : {len(mesh.vertices)}")
    print(f"  Triangles: {len(mesh.triangles)}")
    print("\n Controls:")
    print("  Left click + drag : rotate")
    print("  Scroll            : zoom")
    print("  Right click + drag: pan")
    print("  Q or Escape       : close\n")

    o3d.visualization.draw_geometries(
        [mesh],
        window_name="Digital Twin — 3D Mesh",
        width=1280,
        height=720,
        mesh_show_back_face=True
    )

def main():
    print("\n Digital Twin Visualizer")
    print("="*40)
    print("  1. View Point Cloud")
    print("  2. View 3D Mesh")
    print("  3. View Both")
    print("="*40)
    choice = input("\n  Enter choice (1/2/3): ").strip()

    if choice == "1":
        view_pointcloud()
    elif choice == "2":
        view_mesh()
    elif choice == "3":
        view_pointcloud()
        view_mesh()
    else:
        print("  Invalid choice. Running mesh view by default.")
        view_mesh()

if __name__ == "__main__":
    main()
