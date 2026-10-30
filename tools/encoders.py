"""Pick the video encoder for this PC: NVIDIA's (NVENC) when it works, the CPU otherwise.

Every tool that encodes video asks this module instead of hard-coding h264_nvenc, so the
pipeline runs on any PC. NVENC is tried once with a tiny test encode (a card can be present
but unusable: old driver, no CUDA, a laptop on its integrated GPU), and the answer is cached
for the rest of the run.

Override with VIDEO_ENCODER=cpu or VIDEO_ENCODER=nvidia (env var or .env) when you need to.
"""

import os
import subprocess
from functools import lru_cache
from pathlib import Path


def _env_override() -> str:
    v = os.environ.get("VIDEO_ENCODER", "")
    if not v:
        env = Path(__file__).resolve().parent.parent / ".env"
        try:
            for line in env.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("VIDEO_ENCODER="):
                    v = line.split("=", 1)[1].strip().strip("\"'")
        except OSError:
            pass
    return v.lower()


@lru_cache(maxsize=1)
def use_nvenc() -> bool:
    forced = _env_override()
    if forced in ("cpu", "nvidia"):
        return forced == "nvidia"
    r = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "lavfi",
         "-i", "color=c=black:s=256x256:d=0.2", "-c:v", "h264_nvenc", "-f", "null", "-"],
        capture_output=True, text=True)
    return r.returncode == 0


def describe() -> str:
    return "NVIDIA encoder (NVENC)" if use_nvenc() else "CPU encoder (libx264)"


def hwaccel_args() -> list[str]:
    """Input-side decode acceleration. Only safe to request when NVENC itself works."""
    return ["-hwaccel", "cuda"] if use_nvenc() else []


def video_args(mode: str) -> list[str]:
    """Output-side video encode args.

    preview: 720p, fast, small.
    final:   source resolution, 8-bit H.264 yuv420p, high quality. Plays everywhere
             (players, browsers, the IDE preview, Remotion's decoder), so no hand-off
             transcode is needed afterwards.
    """
    if mode == "preview":
        vf = ["-vf", "scale=1280:-2,format=yuv420p"]
        if use_nvenc():
            return vf + ["-c:v", "h264_nvenc", "-preset", "p4", "-rc", "vbr", "-cq", "30", "-b:v", "0"]
        return vf + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "26"]
    if mode == "final":
        if use_nvenc():
            return ["-pix_fmt", "yuv420p", "-c:v", "h264_nvenc", "-preset", "p5", "-profile:v", "high",
                    "-rc", "vbr", "-cq", "19", "-b:v", "0"]
        return ["-pix_fmt", "yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                "-profile:v", "high"]
    if mode == "proxy":
        vf = ["-vf", "scale=1280:-2,format=yuv420p"]
        if use_nvenc():
            return vf + ["-c:v", "h264_nvenc", "-preset", "p4", "-rc", "vbr", "-cq", "29", "-b:v", "0"]
        return vf + ["-c:v", "libx264", "-preset", "veryfast", "-crf", "27"]
    raise ValueError(f"unknown encode mode: {mode}")


if __name__ == "__main__":
    print(f"video encoder: {describe()}")
