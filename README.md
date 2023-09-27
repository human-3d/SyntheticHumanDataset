# Synthetic Humans in Indoor Scenes Data Generation Pipeline
This repository contains the code to generate synthetic human-scene interaction dataset used in [3D Segmentation of Humans in Point Clouds with Synthetic Data](https://arxiv.org/abs/2212.00786), accepted at ICCV 2023. 

```
@inproceedings{human3d,
    title     = {{3D Segmentation of Humans in Point Clouds with Synthetic Data}},
    author    = {Takmaz, Ay\c{c}a and Schult, Jonas and Kaftan, Irem and Ak\c{c}ay, Mertcan 
                  and Leibe, Bastian and Sumner, Robert and Engelmann, Francis and Tang, Siyu},
    booktitle = {{International Conference on Computer Vision}},
    year      = {2023}
  }
```


## Prerequisites  

**Setting up the environment**  
To run the pipeline, you can create a new environment and install the dependencies as follows:
```
conda create --name synthetichuman3d
conda activate synthetichuman3d
pip install -r requirements.txt
```

**Setting up the data**  
Configurations are made in [*config/config.yaml*](config/config.yaml) file.  

1. *scannet_path* should be the folder containing the ScanNet dataset:
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
where k is the number of people generated for the scene. Synthetic humans that were placed for the Human3D project can be downloaded from [here](https://drive.google.com/file/d/1YP7SJtaAT9lIC85q3wf0X6Iaxkw_fncc/view?usp=sharing).

3. *output_base_renders* is simply where the rendered data will be saved.
   
4. *output_base_pcds* is where the resulting scene point clouds will be saved.

5. *selected_bodies* is the path of the file describing in which scene which synthetic human bodies are placed. An example file is given in [*data/selected_bodies_v3.json*](data/selected_bodies_v3.json). Indices can be arranged based on the desired population level and number of humans generated for each sene.

6. *camera_parameters* is the path of the file containing the intrinsics of the camera and extrinsics for each rendering in each scene. For each rendering, camera height and the angle is resampled. Please refer to our [paper](https://arxiv.org/abs/2212.00786) for more details regarding the process. We provide an example file in [*data/camera_parameters.json*](data/camera_parameters.json).

7. *faces_segmentation* is the path of the file which maps face indices of smplx model to body parts. It is adapted from [this](https://github.com/Meshcapade/wiki/tree/main/assets/SMPL_body_segmentation/smplx) segmentation with some processing to make mappings unique, i.e. one face is mapped to one body part only. We provide it in [*data/smplx_faces_segmentation_unique.npy*](data/smplx_faces_segmentation_unique.npy).

8. *kinect_dot_pattern* is the path to the dot pattern image for Kinect noise simulation, based on [this repo](https://github.com/ankurhanda/simkinect). We provide this file in [*data/kinect-pattern_3x3.png*](data/kinect-pattern_3x3.png). 

9. *samples_per_scene* determines how many renderings are done per scene. *camera_parameters* file needs to be compatible with this number.

10. *pcd_computation* has two parameters. Set *add_kinect_noise* to *True* if you would like to simulate Kinect noise on the rendered depth images before extracting the point cloud. If you would like to suppress the logs during the point cloud generation, set *verbose* to *False*.

## Running the pipeline
After setting the prerequisites, the pipeline can be run simply by:
```
python main.py
```
This script first renders images from the scenes populated with synthetic humans via the `render_synthetic_humans` function from [`render_synthetic_humans.py`](render_synthetic_humans.py).

A known issue is that Open3D starts rendering completely black frames after some time. The code detects it and restarts itself after cleaning these broken scenes. It takes 1.5-2 days to render 40 frames for all scenes in a 2.80GHz i7 CPU. If you want to cancel running it or if the code crashes for some reason (it happens sometimes, again due to Open3D) you can run it again and it continues from where it left.

Once the rendering is done, this script continues with extracting the point clouds by (optionally) simulating Kinect noise on the depth images, and then backprojecting the images to 3D, using the `extract_scene_pcds` function from [`render_convert_to_pcd.py`](render_convert_to_pcd.py). The output of this stage is a dataset consisting of *.ply* files where there are additional two channels for instance labels, and body-part labels.

To load the data (e.g. for training a model), we provide a simplified dataloader: [`example_dataloader.py`](example_dataloader.py). We also provide functions to **visualize the labels**. In this example script, you can simply specify the path to the point cloud you wish to visualize, and automatically export *.ply* files where each point is colored with its respective instance or body-part label color. Please note that for training with the synthetic data, we filtered out scenes that have fewer than 20k points. You can also implement a similar filtering logic within your dataloader depending on your needs.



## BibTeX :pray:

If you find this work helpful and use it in your project, we would be very grateful if you could cite our work **Human3D**:

```
@inproceedings{human3d,
    title     = {{3D Segmentation of Humans in Point Clouds with Synthetic Data}},
    author    = {Takmaz, Ay\c{c}a and Schult, Jonas and Kaftan, Irem and Ak\c{c}ay, Mertcan 
                  and Leibe, Bastian and Sumner, Robert and Engelmann, Francis and Tang, Siyu},
    booktitle = {{International Conference on Computer Vision}},
    year      = {2023}
  }
```


If you use Kinect simulation, please also consider citing the following work:
```
@article{handa:etal:2014,
  title   = {A benchmark for RGB-D visual odometry, 3D reconstruction and SLAM},
  author  = {Handa, Ankur and Whelan, Thomas and McDonald, John and Davison, Andrew J},
  journal = {ICRA},
  year    = {2014},
}
```
