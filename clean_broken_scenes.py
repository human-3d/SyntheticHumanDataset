from pathlib import Path
import shutil


def clean_broken_scenes(cfg):
    """
    Look through the output folder and remove the folder(s) where rendering failed
    """
    output_path = Path(cfg.output_base_renders)
    scenes = [f for f in output_path.glob("scene*")]

    # The code just started, simply return
    if not scenes:
        return

    broken_scenes = list()
    # Count the label images (could be depth, color etc.) and remove the folder if the count is not the intended
    for scene in sorted(scenes):
        label_images = [f for f in (scene / "label_image").glob("*.png")]
        if len(label_images) != cfg.samples_per_scene:
            broken_scenes.append(scene)
    
    if len(broken_scenes)>0:
        print(f"[INFO] Following broken scenes are getting removed:")
        for s in broken_scenes:
            print(s.stem)
            shutil.rmtree(s)
    else:
        print("[INFO] No broken scenes found!")
