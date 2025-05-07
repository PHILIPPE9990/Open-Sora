import os
import subprocess

def parse_resolution(resolution_str):
    resolution_map = {
        "144p": ("144", "256"),
        "240p": ("240", "426"),
        "360p": ("360", "640"),
        "480p": ("480", "854"),  
        "720p": ("720", "1280")
    }
    return resolution_map.get(resolution_str, ("144", "256"))

def runTerminalCommand(desc, videoLength, resolution, model, seed):

    current_dir = os.getcwd()
    try:
        # Navigate two levels up
        two_levels_up = os.path.abspath(os.path.join(current_dir, '..'))
        os.chdir(two_levels_up)

        cmd = []
        if(model == "opensora-v1-2"):
            cmd  = [
                "python", "scripts/inference.py", "configs/opensora-v1-2/inference/sample.py",
                "--num-frames", videoLength,
                "--resolution", resolution,
                "--aspect-ratio", "9:16",
                "--prompt", desc,
                "--seed", str(seed)
            ]
        elif(model == "opensora-v1-1"):
            #video length remove s and resolution seperate to two arguments manually
            width, height = parse_resolution(resolution)
            #print(videoLength.rstrip('s'))
            cmd = [
                "python", "scripts/inference.py", "configs/opensora-v1-1/inference/sample.py",
                "--prompt", desc,
                "--seed", str(seed),
                "--num-frames", videoLength.rstrip('s'),
                "--image-size", width, height
            ]
        elif(model == "opensora-vA-B"):
            width, height = parse_resolution(resolution)
            cmd = [
                "python", "scripts/inference.py", "configs/opensora-vA-B/inference/sample.py",
                "--prompt", desc,
                "--seed", str(seed),
                "--num-frames", videoLength.rstrip('s'),
                "--image-size", width, height
            ]
        print(cmd)
        result = subprocess.run(cmd)

        if result.returncode != 0:
            raise Exception(f"Video Generation Error: an error occur during video generation, please try again.")
    finally:
        os.chdir(current_dir)

