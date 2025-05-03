import os
import subprocess

def runTerminalCommand(desc, videoLength, resolution, model):

    current_dir = os.getcwd()
    
    # Navigate two levels up
    two_levels_up = os.path.abspath(os.path.join(current_dir, '..'))
    os.chdir(two_levels_up)

    # cmd  = [
    #     "python", "scripts/inference.py", "configs/opensora-v1-2/inference/sample.py",
    #     "--num-frames", videoLength,
    #     "--resolution", resolution,
    #     "--aspect-ratio", "9:16",
    #     "--prompt", desc
    # ]

    cmd = [
       "python", "scripts/inference.py", "configs/opensora-vA-B/inference/sample.py",
       "--prompt", desc,
       "--num-frames", "2",
       "--image-size", "144", "256"
    ]
    #video length remove s and resolution seperate to two arguments manually
    
    
    print(cmd)
    result = subprocess.run(cmd)

    if result.returncode != 0:
        raise Exception(f"Video Generation Error: an error occur during video generation, please try again.")

