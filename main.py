from config.config import Config
from render_synthetic_humans import main
from clean_broken_scenes import clean_broken_scenes

if __name__ == "__main__":
    # Load args
    args = Config()

    # Start by checking broken scenes in the output directory
    clean_broken_scenes(args)

    # Start the pipeline
    # Run until pipeline fails -> clear the scenes where it failed -> start again
    pipeline_broke = not main(args)
    while pipeline_broke:
        pipeline_broke = not main(args)
        clean_broken_scenes(args)

    print("[INFO] Dataset generation is complete!")
