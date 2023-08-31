from config.config import Config
from render_synthetic_humans import render_synthetic_humans
from clean_broken_scenes import clean_broken_scenes
from render_convert_to_pcd import extract_scene_pcds

if __name__ == "__main__":
    # Load config
    config_path = "config/config.yaml"
    cfg = Config(config_path)

    # Start by checking broken scenes in the output directory
    clean_broken_scenes(cfg)

    # Start the pipeline
    # Run until pipeline fails -> clear the scenes where it failed -> start again
    pipeline_broke = not render_synthetic_humans(cfg)
    while pipeline_broke:
        pipeline_broke = not render_synthetic_humans(cfg)
        clean_broken_scenes(cfg)

    print("[INFO] Scene rendering is complete!")

    # obtain point clouds
    extract_scene_pcds(cfg)

    print("[INFO] Dataset generation is complete!")

