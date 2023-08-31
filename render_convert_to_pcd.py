import os
import cv2
import json
import numpy as np
from PIL import Image as Image
from utils.pc_utils import save_point_cloud_w_inst_label
from utils.color_maps_and_labels import COLOR_MAP, COLOR_MAP_INSTANCES, BODY_PARTS_COLOR_MAP_IDS
from utils.process_renders_utils import get_pointcloud_mat_scene_mask, add_kinect_noise_to_depth

def extract_scene_pcds(cfg):

    # get config params
    verbose = cfg.verbose
    add_kinect_noise = cfg.add_kinect_noise
    kinect_dot_pattern_path = cfg.kinect_dot_pattern
    dot_pattern = cv2.imread(kinect_dot_pattern_path, 0)
    output_base_renders =  cfg.output_base_renders #path to the rendered scenes, read from this directory
    output_base_pcds = cfg.output_base_pcds #where to write the scene pcds

    # set camera parameters - ~60deg horizontal fov, fx=fy assumed, principal point at the center assumed
    near_plane, far_plane = cfg.near_plane, cfg.far_plane # in meters
    camera_parameters = json.load(open(cfg.camera_parameters_path))
    cam_intrinsics = np.array(camera_parameters["intrinsics"], dtype=np.float64)
    
    scene_list = sorted([el for el in os.listdir(output_base_renders) if os.path.isdir(os.path.join(output_base_renders, el))])

    for scene_folder in scene_list:
        scene_read_root = os.path.join(output_base_renders, scene_folder)
        
        color_root = os.path.join(scene_read_root, 'color_image')
        depth_root = os.path.join(scene_read_root, 'depth_image')
        id_root = os.path.join(scene_read_root, 'id_image')
        instance_id_root = os.path.join(scene_read_root, 'instance_id_image')
        label_root = os.path.join(scene_read_root, 'label_image')
        scene_mask_root = os.path.join(scene_read_root, 'scene_mask_image')

        color_imgs_list = [os.path.join(color_root, el) for el in sorted(os.listdir(color_root))]
        depth_imgs_list = [os.path.join(depth_root, el) for el in sorted(os.listdir(depth_root))]
        id_imgs_list = [os.path.join(id_root, el) for el in sorted(os.listdir(id_root))]
        instance_id_imgs_list = [os.path.join(instance_id_root, el) for el in sorted(os.listdir(instance_id_root))]
        label_imgs_list = [os.path.join(label_root, el) for el in sorted(os.listdir(label_root))]
        scene_mask_imgs_list = [os.path.join(scene_mask_root, el) for el in sorted(os.listdir(scene_mask_root))]

        assert (len(depth_imgs_list)==len(color_imgs_list)==len(id_imgs_list)==len(label_imgs_list)==len(scene_mask_imgs_list))

        scene_write_dir = os.path.join(output_base_pcds, scene_folder)
        if not os.path.exists(scene_write_dir):
            os.makedirs(scene_write_dir)

        for idx in range(len(depth_imgs_list)):
            id_str = str(idx).zfill(2)

            path_rgb = color_imgs_list[idx]
            path_depth = depth_imgs_list[idx]
            path_id_img = id_imgs_list[idx]
            path_instance_id_img = instance_id_imgs_list[idx]
            path_label_img = label_imgs_list[idx]
            path_scene_mask_img = scene_mask_imgs_list[idx]

            img_rgb = np.asarray(Image.open(path_rgb))
            img_depth_np = np.load(path_depth)
            img_id = np.asarray(Image.open(path_id_img))
            img_instance_id = np.asarray(Image.open(path_instance_id_img)) # including 0: background, e.g. 0,4,5,8
            img_label = np.asarray(Image.open(path_label_img))
            img_scene_mask = np.asarray(Image.open(path_scene_mask_img)).copy()

            if add_kinect_noise:
                img_depth_np_w_kinect_noise = add_kinect_noise_to_depth(img_depth_np, dot_pattern, a_min=near_plane, a_max=far_plane)
                img_depth_np = img_depth_np_w_kinect_noise
                img_scene_mask[img_depth_np==float('inf')] = 0
            else:
                #update scene mask based on the depth image and the near/far plane values
                img_scene_mask[img_depth_np<near_plane] = 0
                img_scene_mask[img_depth_np>far_plane] = 0
            

            inst_label_mapper = {el:idx for idx, el in enumerate(sorted(np.unique(img_instance_id)))} # e.g. {0: 0, 4: 1}
            
            img_instance_id_mapped = np.copy(img_instance_id)
            for old, new in inst_label_mapper.items():
                img_instance_id_mapped[img_instance_id == old] = new
            
            pc, rgb, label_rgb, label_id, label_instance_id = get_pointcloud_mat_scene_mask(img_depth_np, img_rgb, img_label, img_id, img_instance_id_mapped, img_scene_mask, cam_intrinsics)

            # saving the ply
            points_3d = np.zeros((pc.shape[0], 8))
            points_3d[:,0:3] = pc #(num_points, 3)
            points_3d[:,3:6] = rgb #(num_points, 3) #0-255, uint8
            points_3d[:,6] = label_instance_id #(182918,) #uint8 #orig label ids, not mapped to the valid ids yet (human is 31, and not 16)
            points_3d[:,7] = label_id #(182918,) #uint8 #orig label ids, not mapped to the valid ids yet (human is 31, and not 16)
            current_frame_out_ply_path = os.path.join(scene_write_dir, "frame_" + id_str + '.ply')

            save_point_cloud_w_inst_label(points_3d, current_frame_out_ply_path, with_label=True, binary=True, verbose=verbose)
