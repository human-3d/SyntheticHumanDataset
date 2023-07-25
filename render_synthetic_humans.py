import json
import open3d as o3d
import numpy as np
from PIL import Image
from tqdm import tqdm
from pathlib import Path


def main(args):
    # Read selected synthetic bodies per scene
    selected_bodies = open(args.selected_bodies_path)
    selected_bodies = json.load(selected_bodies)["scenes"]

    # Read camera parameters per scene
    camera_parameters = json.load(open(args.camera_parameters_path))
    cam_intrinsics = np.array(camera_parameters["intrinsics"], dtype=np.float64)
    cam_extrinsics = camera_parameters["extrinsics"]

    # Read body part segmentation file
    faces_segmentation = np.load(args.faces_segmentation_path, allow_pickle=True).item()

    # Id to color, use valid colors to map to ids
    body_parts_color_map_ids = tuple(range(100, 127))

    # Dict other way around
    color_to_id = dict((tuple(v), k) for k, v in args.color_map.items())

    material = o3d.visualization.rendering.MaterialRecord()
    label_renderer = o3d.visualization.rendering.OffscreenRenderer(
        args.image_width, args.image_height
    )
    color_renderer = o3d.visualization.rendering.OffscreenRenderer(
        args.image_width, args.image_height
    )
    instance_renderer = o3d.visualization.rendering.OffscreenRenderer(
        args.image_width, args.image_height
    )

    # Don't mess up with pixel values! We dont want shading
    label_renderer.scene.view.set_post_processing(False)
    color_renderer.scene.view.set_post_processing(False)
    instance_renderer.scene.view.set_post_processing(False)

    # Set cameras
    label_renderer.scene.camera.set_projection(
        cam_intrinsics,
        args.near_plane,
        args.far_plane,
        args.image_width,
        args.image_height,
    )
    color_renderer.scene.camera.set_projection(
        cam_intrinsics,
        args.near_plane,
        args.far_plane,
        args.image_width,
        args.image_height,
    )
    instance_renderer.scene.camera.set_projection(
        cam_intrinsics,
        args.near_plane,
        args.far_plane,
        args.image_width,
        args.image_height,
    )

    # Iterate through all scenes
    for scene_idx, scene in enumerate(tqdm(selected_bodies)):
        # Get scene name and which humans to put in the scene
        scene_name = scene["scene"]
        human_indices = scene["indices"]

        # Make sure we get parameters for the same scene from two json files
        assert cam_extrinsics[scene_idx]["scene"] == scene_name

        # Check if the folder is already created, skip if already rendered the scene.
        output_path = Path(args.output_base) / scene_name
        if output_path.exists():
            continue

        folder_list = [
            "color_image",
            "depth_image",
            "id_image",
            "instance_id_image",
            "label_image",
            "scene_mask_image",
        ]
        for f in folder_list:
            (output_path / f).mkdir(parents=True)

        # Read label and color meshes
        scene_label_mesh = o3d.io.read_triangle_mesh(
            str(
                Path(args.scannet_path)
                / scene_name
                / f"{scene_name}_vh_clean_2.labels.ply"
            )
        )
        scene_color_mesh = o3d.io.read_triangle_mesh(
            str(Path(args.scannet_path) / scene_name / f"{scene_name}_vh_clean_2.ply")
        )

        # Get scene center
        scene_center = cam_extrinsics[scene_idx]["scene_center"]

        # Repeat for required sample count
        for sample in range(args.samples_per_scene):
            # Set renderers
            label_renderer.scene.clear_geometry()
            color_renderer.scene.clear_geometry()
            instance_renderer.scene.clear_geometry()

            # Populate scenes
            label_renderer.scene.add_geometry("scene_label", scene_label_mesh, material)
            color_renderer.scene.add_geometry("scene_color", scene_color_mesh, material)

            # Get camera extrinsics
            cam_angle = cam_extrinsics[scene_idx]["cam"][sample]["angle"]
            cam_height = cam_extrinsics[scene_idx]["cam"][sample]["height"]

            # Get and add human meshes
            for k, idx in enumerate(human_indices):
                formatted_ind = "{:02d}".format(idx)
                human = o3d.io.read_triangle_mesh(
                    f"{args.synthetic_humans_path}/{scene_name}/{scene_name}_{formatted_ind}.ply"
                )

                # Human label is (0,0,1)
                human.paint_uniform_color(np.array([0, 0, 1]))

                # Add current human to the scene
                color_renderer.scene.add_geometry(f"human{k}", human, material)

                # Paint human based on instance id
                human_instance = human
                color_instance = float(k + 1) * np.array([20.0, 20.0, 20.0]) / 255.0
                human_instance.paint_uniform_color(color_instance)
                instance_renderer.scene.add_geometry(
                    f"human{k}", human_instance, material
                )

                # Add human parts
                vertices = human.vertices
                for idx, body_part in enumerate(args.body_segments_order):
                    body_part_faces = o3d.utility.Vector3iVector(
                        faces_segmentation[body_part]
                    )
                    body_part_mesh = o3d.geometry.TriangleMesh(
                        vertices, body_part_faces
                    )
                    color = np.array(args.color_map[100 + idx]) / 255.0
                    body_part_mesh.paint_uniform_color(color)
                    label_renderer.scene.add_geometry(
                        f"human{k}_{idx}", body_part_mesh, material
                    )

            # Set height of the camera, uniform between 140cm and 160cm
            cam_position = np.array(scene_center + [cam_height])

            # Set direction of the camera
            ray = [np.cos(cam_angle), np.sin(cam_angle), 0]
            label_renderer.scene.camera.look_at(
                cam_position + ray, cam_position, [0, 0, 1]
            )
            color_renderer.scene.camera.look_at(
                cam_position + ray, cam_position, [0, 0, 1]
            )
            instance_renderer.scene.camera.look_at(
                cam_position + ray, cam_position, [0, 0, 1]
            )

            # Render color, label and depth images
            label_img = label_renderer.render_to_image()
            label_img_array = np.asarray(label_img)

            instance_img = instance_renderer.render_to_image()
            instance_img_array = np.asarray(instance_img)

            depth_image = label_renderer.render_to_depth_image(z_in_view_space=True)
            depth_image_array = np.asarray(depth_image)

            color_img = color_renderer.render_to_image()

            # ! Known issue: open3d starts rendering all black images, detect it and exit
            if np.count_nonzero(label_img_array) == 0:
                return False

            # Save depth, color, label, id imgs + mask
            formatted_sample = "{:02d}".format(sample)  # index while saving

            o3d.io.write_image(
                str(output_path / "color_image" / f"{formatted_sample}.png"), color_img
            )
            np.save(
                str(output_path / "depth_image" / f"{formatted_sample}.npy"),
                depth_image_array,
            )

            # Create id image and mask
            id_img = np.zeros((args.image_height, args.image_width))
            instance_id_img = np.zeros((args.image_height, args.image_width))
            scene_mask = np.ones((args.image_height, args.image_width), dtype=bool)

            # Iterate each pixel for id image and mask
            for i in range(args.image_height):
                for j in range(args.image_width):
                    label_color = tuple(label_img_array[i, j, :])
                    instance_color = tuple(instance_img_array[i, j, :])

                    id = color_to_id.get(label_color)
                    if id in args.valid_color_map_ids or id in body_parts_color_map_ids:
                        if id == 31:
                            label_img_array[i, j, :] = args.color_map[41]
                        if id == 41:
                            id = 31  # very little real humans in the scene
                        id_img[i, j] = id

                    if (
                        id in body_parts_color_map_ids
                        and id not in args.valid_color_map_ids
                    ):
                        instance_id_img[i, j] = instance_color[0] / 20.0
                    elif id == 0 or id == -1:
                        scene_mask[i, j] = False

            label_img = Image.fromarray(label_img_array)
            label_img.save(output_path / "label_image" / f"{formatted_sample}.png")

            id_img = Image.fromarray(id_img.astype(np.uint8))
            id_img.save(output_path / "id_image" / f"{formatted_sample}.png")

            instance_id_img = Image.fromarray(instance_id_img.astype(np.uint8))
            instance_id_img.save(
                output_path / "instance_id_image" / f"{formatted_sample}.png"
            )

            not_inf = np.logical_not(np.isinf(depth_image_array))
            scene_mask = 255 * (np.logical_and(not_inf, scene_mask)).astype(
                dtype=np.uint8
            )

            scene_mask_img = Image.fromarray(scene_mask)
            scene_mask_img.save(
                output_path / "scene_mask_image" / f"{formatted_sample}.png"
            )

    return True
