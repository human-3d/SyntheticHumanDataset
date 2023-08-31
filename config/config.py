import os
import yaml
from pathlib import Path


class Config:
    def __init__(self):
        config_file = Path(__file__).parent / "config.yaml"
        assert config_file.exists(), "Config file does not exist!"

        with open(config_file, "r") as stream:
            settings = yaml.safe_load(stream)

            # ___ paths ___
            paths = settings["paths"]
            self.scannet_path = paths["scannet_path"]
            self.synthetic_humans_path = paths["synthetic_humans"]
            self.output_base_renders = paths["output_base_renders"]
            self.output_base_pcds = paths["output_base_pcds"]
            self.selected_bodies_path = paths["selected_bodies"]
            self.camera_parameters_path = paths["camera_parameters"]
            self.faces_segmentation_path = paths["faces_segmentation"]

            # ___ camera parameters ___
            camera = settings["camera"]
            self.image_width = camera["width"]
            self.image_height = camera["height"]
            self.near_plane = camera["near_plane"]
            self.far_plane = camera["far_plane"]

            # ___ rendering ___
            rendering = settings["rendering"]
            self.valid_color_map_ids = rendering["valid_color_map_ids"]
            self.samples_per_scene = rendering["samples_per_scene"]
            self.body_segments_order = rendering["body_segments_order"]
            self.color_map = rendering["color_map"]

            # ___ point cloud computation ___
            pcd = settings["pcd_computation"]
            self.add_kinect_noise = pcd["add_kinect_noise"]
            self.verbose = pcd["verbose"]

