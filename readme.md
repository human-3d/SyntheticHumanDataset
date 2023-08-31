# Synthetic Humans in Indoor Scenes Data Generation Pipeline
This repository contains the code to generate synthetic human-scene interaction dataset used in [3D Segmentation of Humans in Point Clouds with Synthetic Data](https://arxiv.org/abs/2212.00786). Please stay tuned for the code to obtain the point clouds with the simulated Kinect noise - expected release date: September 2023!

## Prerequisites  

**Setting up the environment**  
The only dependency to run the pipeline is Open3D (which installs other libraries as dependencies), which can simply be installed by
```
pip install open3d==0.17
```
**Setting up the data**  
Configurations are done in *config/config.yaml* file.  

1. *scannet_path* should be the folder containing the scannet dataset:
```
|--scannet_path  
|  |--scene0000_00  
|    |--scene0000_00_vh_clean_2.ply  
|    |--scene0000_00_vh_clean_2.labels.ply  
|  |...  
|  |...  
|  |...  
|  |--scene0706_00  
|    |--scene0706_00_vh_clean_2.ply  
|    |--scene0706_00_vh_clean_2.labels.ply  
```
2. *synthetic_humans* should be the folder containing the synthetic human meshes (smplx) in the following structure:
```
|--synthetic_humans  
|  |--scene0000_00  
|    |--scene0000_00_00.ply  
|    |--...  
|    |--scene0000_00_k.ply  
|  |...  
|  |...  
```
where k is the number of people generated for the scene.  

3. *output_base_renders* is simply where the rendered data will be saved.
   
4. *output_base_pcds* is where the resulting scene point clouds will be saved.

5. *selected_bodies* is the path of the file describing in which scene which synthetic human bodies are placed. An example file is given in *data/selected_bodies_v3.json*. Indices can be arranged based on the desired population level and number of humans generated for each sene.

6. *camera_parameters* is the path of the file containing the intrinsics of the camera and extrinsics for each rendering in each scene. For each rendering, camera height and the angle is resampled. Refer to our [paper](https://arxiv.org/abs/2212.00786) for more details regarding the process. We provide an example file in *data/camera_parameters.json".

7. *faces_segmentation* is the path of the file which maps face indices of smplx model to body parts. It is adapted from [this](https://github.com/Meshcapade/wiki/tree/main/assets/SMPL_body_segmentation/smplx) segmentation with some processing to make mappings unique, i.e. one face is mapped to one body part only. We provide it in *data/smplx_faces_segmentation_unique.py*.

8. *samples_per_scene* determines how many renderings are done per scene. *camera_parameters* file needs to be compatible with this number.

## Running the pipeline
After setting the prerequisites, the pipeline can be run simply by:
```
python main.py
```

A known issue is that Open3D starts rendering completely black frames after some time. The code detects it and restarts itself after cleaning these broken scenes. It takes 1.5-2 days to render 40 frames for all scenes in a 2.80GHz i7 CPU. If you want to cancel running it or if the code crashes for some reason (it happens sometimes, again due to Open3D) you can run it again and it continues from where it left.
