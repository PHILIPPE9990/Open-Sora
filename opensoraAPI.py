import subprocess

cmd  = [
    "python", "scripts/inference.py", "configs/opensora-v1-2/inference/sample.py",
    "--num-frames", "2s",
    "--resolution", "144p",
    "--aspect-ratio", "9:16",
    "--prompt", "a beautiful waterfall"
]


subprocess.run(cmd)
