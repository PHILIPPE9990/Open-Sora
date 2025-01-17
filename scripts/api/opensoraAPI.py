import os
import subprocess

def runTerminalCommand(desc, videoLength, resolution):

    current_dir = os.getcwd()
    
    # Navigate two levels up
    two_levels_up = os.path.abspath(os.path.join(current_dir, '..'))
    os.chdir(two_levels_up)

    cmd  = [
        "python", "scripts/inference.py", "configs/opensora-v1-2/inference/sample.py",
        "--num-frames", videoLength,
        "--resolution", resolution,
        "--aspect-ratio", "9:16",
        "--prompt", desc
    ]
    
    print(cmd)
    subprocess.run(cmd)

