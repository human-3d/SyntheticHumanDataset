# adapted from https://github.com/ankurhanda/simkinect

import numpy as np
from utils.simkinect_camera_utils import add_gaussian_shifts, filterDisp

def add_kinect_noise_to_depth(depth_orig, 
                            dot_pattern,
                            scale_factor=100, 
                            baseline_m=0.075, 
                            std=0.5,
                            size_filt=6,
                            focal_length = 554.0,
                            invalid_disp = 99999999.9,
                            a_min = 0.01, #near_plane
                            a_max = 20, #far_plane
                            a_max_tight_bound = 17.0,
                            w = 640,
                            h = 480):

        depth_invalid_exch = depth_orig.copy()
        depth_invalid_exch[depth_invalid_exch==float('inf')] = invalid_disp
        depth_clipped = depth_invalid_exch
        depth_clipped = np.clip(depth_orig, a_min=a_min, a_max=a_max)
        depth_interp = add_gaussian_shifts(depth_clipped, std=std)
        disp_= focal_length * baseline_m / (depth_interp + 1e-10)
        depth_f = np.round(disp_ * 8.0)/8.0
        out_disp = filterDisp(depth_f, dot_pattern, invalid_disp, size_filt_=size_filt)
        depth = focal_length * baseline_m / (out_disp + 1e-10)
        depth[out_disp == invalid_disp] = 0
        
        # The depth here needs to be converted to cms so scale factor is introduced 
        # though often this can be tuned from [100, 200] to get the desired banding / quantisation effects 
        noisy_depth = (35130/np.round((35130/(np.round(depth*scale_factor) + 1e-10)) + np.random.normal(size=(h, w))*(1.0/6.0) + 0.5))/scale_factor 

        noisy_depth[noisy_depth<a_min] = float('inf')
        noisy_depth[noisy_depth>=a_max_tight_bound] = float('inf')
        
        return noisy_depth


def get_pointcloud_mat_scene_mask(depth, rgb, label_rgb, label_id, label_instance_id, scene_mask, cam_intrinsics):
    
    filt_mask = np.where(scene_mask)
    x = filt_mask[1]
    y = filt_mask[0]
    
    K_inv = np.linalg.inv(cam_intrinsics)
    res = np.vstack((x, y, np.ones(x.shape)))
    res = K_inv @ res
    res = depth[y,x] * res
    res = res.T
    
    return res, rgb[y, x], label_rgb[y, x], label_id[y, x], label_instance_id[y, x]
