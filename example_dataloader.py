import pandas as pd
from plyfile import PlyData
import numpy as np
import open3d as o3d
from utils.color_maps_and_labels import COLOR_MAP_INSTANCES, MERGED_BODY_PART_COLORS

# Note: If you would like to use this dataset as a Torch dataset, simply inherit from torch.utils.data import Dataset, e.g.:
# from torch.utils.data import Dataset
# class HumanSegmentationDataset(Dataset):
class HumanSegmentationDataset():
    def __init__(self, file_list):
        # some color maps in case you need to visualize
        # we rendered the segmentation maps including scene semantic labels, 
        # but later we map all categories except for the body parts to the 'background' category
        self.file_list = file_list

        self.COLOR_MAP_INSTANCES = COLOR_MAP_INSTANCES
        self.MERGED_BODY_PART_COLORS = MERGED_BODY_PART_COLORS

        self.ORIG_BODY_PART_IDS = set(range(100,126))
                        
        self.LABEL_LIST = ["background", "rightHand", "rightUpLeg", "leftArm", "head", "leftEye", "rightEye", "leftLeg", 
                        "leftToeBase", "leftFoot", "spine1", "spine2", "leftShoulder", "rightShoulder", 
                        "rightFoot", "rightArm", "leftHandIndex1", "rightLeg", "rightHandIndex1",
                        "leftForeArm", "rightForeArm", "neck", "rightToeBase", "spine", "leftUpLeg", 
                        "leftHand", "hips"]

        self.MERGED_LABEL_LIST = {
                    0: "background",
                    1: "rightHand",
                    2: "rightUpLeg",
                    3: "leftArm",
                    4: "head",
                    5: "leftLeg",
                    6: "leftFoot",
                    7: "torso",
                    8: "rightFoot",
                    9: "rightArm",
                    10: "leftHand",
                    11: "rightLeg",
                    12: "leftForeArm",
                    13: "rightForeArm",
                    14: "leftUpLeg",
                    15: "hips"
                }

        # by use this mapping, we obtain 15 different body parts
        self.LABEL_MAPPER_FOR_BODY_PART_SEGM={
            -1: 0, 0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 
            11: 0, 12: 0, 13:0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 
            22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0, 31: 0, 32: 0, 
            33: 0, 34: 0, 35: 0, 36: 0, 37: 0, 38: 0, 39: 0, 40: 0, 41: 0, #background
            100: 1, # rightHand
            101: 2, # rightUpLeg
            102: 3, # leftArm
            103: 4, # head
            104: 4, # head
            105: 4, # head
            106: 5, # leftLeg
            107: 6, # leftFoot
            108: 6, # leftFoot
            109: 7, # torso
            110: 7, # torso
            111: 7, # torso
            112: 7, # torso
            113: 8, # rightFoot
            114: 9, # rightArm
            115: 10, # leftHand
            116: 11, # rightLeg
            117: 1, # rightHand
            118: 12, # leftForeArm
            119: 13, # rightForeArm
            120: 4, # head
            121: 8, # rightFoot
            122: 7, # torso
            123: 14, # leftUpLeg
            124: 10, # leftHand
            125: 15, # hips
        }

    def __len__(self):
        return len(self.file_list)

    def read_plyfile(self, file_path):
        """Read ply file and return it as numpy array. Returns None if emtpy."""
        with open(file_path, 'rb') as f:
            plydata = PlyData.read(f)
        if plydata.elements:
            return pd.DataFrame(plydata.elements[0].data).values

    def load_pc(self, file_path):
        pc = self.read_plyfile(file_path) # (num_points, 8)
        
        pc_coords = pc[:, 0:3] # (num_points, 8)
       
        # rgb values are in the format 0-255
        pc_rgb = pc[:, 3:6].astype(np.uint8) # (num_points, 3) - 0-255
        
        # values range from 0 to 11. 0 refers to background, 1-10 refers to instance id.
        pc_inst_labels = pc[:, 6].astype(np.uint8) # (num_points,)
        
        # this map includes object semantic categories as well. please see the keys of COLOR_MAP_W_BODY_PARTS
        # original categories for body part segmentation. 0 refers to background, 100-126 refers to body parts.
        pc_orig_segm_labels = pc[:, 7].astype(np.uint8) # (num_points,)
        
        # we map these parts to 15 body parts by merging smaller body parts.
        pc_part_segm_labels = np.asarray([self.LABEL_MAPPER_FOR_BODY_PART_SEGM[el] for el in pc_orig_segm_labels]) 

        return pc_coords, pc_rgb, pc_inst_labels, pc_orig_segm_labels, pc_part_segm_labels 

    def export_colored_pcd_inst_segm(self, coords, pc_inst_labels, write_path):
        # to visualize instance segmentation labels for debugging purposes
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(coords)
        inst_colors = np.asarray([self.COLOR_MAP_INSTANCES[int(label_idx)] for label_idx in pc_inst_labels])/255.0
        pcd.colors  = o3d.utility.Vector3dVector(inst_colors)
        pcd.estimate_normals()
        o3d.io.write_point_cloud(write_path, pcd)

    def export_colored_pcd_part_segm(self, coords, pc_part_segm_labels, write_path):
        # to visualize body part segmentation labels for debugging purposes
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(coords)

        # map labels -> get colors for body parts, map everything else to black
        part_colors = np.asarray([self.MERGED_BODY_PART_COLORS[int(label_idx)] for label_idx in pc_part_segm_labels])/255.0
        pcd.colors  = o3d.utility.Vector3dVector(part_colors)
        pcd.estimate_normals()
        o3d.io.write_point_cloud(write_path, pcd)

    def __getitem__(self, index):
        # dummy __getitem__ method, no augmentations etc. - just load and return
        return self.load_pc(self.file_list[index])


if __name__=="__main__":
    
    demo_pcd_path = 'examples/example_synthetic_scene.ply' # sample input scene

    file_list = [demo_pcd_path] # for now just the demo scene
    dataset = HumanSegmentationDataset(file_list=file_list)

    # you can also simply use the load_pc method to load the sample ply
    coords, colors, inst_labels, full_body_part_labels, merged_body_part_labels = dataset.load_pc(demo_pcd_path) # (num_points, 3), (num_points, 3), (num_points,), (num_points,), (num_points,)
    # HUMAN3D USES MERGED PARTS! -> merged_body_part_labels, you can ignore full_body_part_labels unless you want to specifically use all body parts
    # merged_body_part_labels: background has label 0, all 15 merged body part labels are in the range(1, 16). For labels, see dataset.MERGED_BODY_PART_COLORS or dataset.MERGED_LABEL_LIST
    # full_body_part_labels: background has label 0, all 26 body part labels are in the range(100, 126). For labels, see dataset.COLOR_MAP_W_BODY_PARTS or dataset.LABEL_MAP

    # to export plys with the label colors for respective tasks - instance segm. or body part segm.
    dataset.export_colored_pcd_inst_segm(coords, inst_labels, write_path = 'examples/demo_scene_inst_visualization.ply')
    dataset.export_colored_pcd_part_segm(coords, merged_body_part_labels, write_path = 'examples/demo_scene_merged_part_visualization.ply')
