import open3d as o3d
import numpy as np
import struct
import os

# ── CONFIG ──────────────────────────────────────────────
SPARSE_DIR  = "outputs/sparse/0"
MESH_DIR    = "outputs/meshes"
PLY_OUT     = "outputs/meshes/pointcloud.ply"
MESH_OUT    = "outputs/meshes/mesh.ply"
MESH_OBJ    = "outputs/meshes/mesh.obj"
# ────────────────────────────────────────────────────────

def read_points3d_binary(path):
    """Read COLMAP points3D.bin and return Nx3 points and Nx3 colors."""
    points = []
    colors = []

    with open(path, "rb") as f:
        num_points = struct.unpack("<Q", f.read(8))[0]
        print(f"  Reading {num_points} 3D points...")

        for _ in range(num_points):
            point_id = struct.unpack("<Q", f.read(8))[0]
            x, y, z  = struct.unpack("<ddd", f.read(24))
            r, g, b  = struct.unpack("<BBB", f.read(3))
            error    = struct.unpack("<d", f.read(8))[0]

            # track array
            track_length = struct.unpack("<Q", f.read(8))[0]
            f.read(8 * track_length)  # skip track entries

            points.append([x, y, z])
            colors.append([r / 255.0, g / 255.0, b / 255.0])

    return np.array(points), np.array(colors)


def main():
    os.makedirs(MESH_DIR, exist_ok=True)

    points3d_path = os.path.join(SPARSE_DIR, "points3D.bin")

    if not os.path.exists(points3d_path):
        print(f"ERROR: {points3d_path} not found.")
        print("Make sure sparse reconstruction completed successfully.")
        return

    print("\n Mesh Generator")
    print(f"  Source: {points3d_path}\n")

    # ── Load points ──
    points, colors = read_points3d_binary(points3d_path)
    print(f"  Loaded : {len(points)} points")

    # ── Create Open3D point cloud ──
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points)
    pcd.colors = o3d.utility.Vector3dVector(colors)

    # ── Remove outliers ──
    print("\n  Removing outliers...")
    pcd, _ = pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
    print(f"  After cleanup: {len(pcd.points)} points")

    # ── Save point cloud ──
    o3d.io.write_point_cloud(PLY_OUT, pcd)
    print(f"\n  Point cloud saved: {PLY_OUT}")

    # ── Estimate normals ──
    print("\n  Estimating normals...")
    pcd.estimate_normals(
        search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30)
    )
    pcd.orient_normals_consistent_tangent_plane(100)

    # ── Poisson mesh reconstruction ──
    print("  Running Poisson reconstruction...")
    mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
        pcd, depth=9
    )

    # ── Remove low density vertices ──
    print("  Cleaning mesh...")
    densities = np.asarray(densities)
    keep_mask = densities > np.percentile(densities, 10)
    mesh.remove_vertices_by_mask(~keep_mask)

    mesh.compute_vertex_normals()

    # ── Save mesh ──
    o3d.io.write_triangle_mesh(MESH_OUT, mesh)
    o3d.io.write_triangle_mesh(MESH_OBJ, mesh)

    print(f"\n  Mesh saved : {MESH_OUT}")
    print(f"  OBJ saved  : {MESH_OBJ}")
    print(f"  Vertices   : {len(mesh.vertices)}")
    print(f"  Triangles  : {len(mesh.triangles)}")
    print(f"\n  Next step  : run visualizer.py")


if __name__ == "__main__":
    main()
