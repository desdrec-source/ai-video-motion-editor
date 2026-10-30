"""Make every raw recording in a project safe to cut: constant frame rate.

Screen recorders (Panda, OBS, Loom, ...) usually write VARIABLE frame rate video: the gap
between frames wanders (measured on a Panda recording: 28-139 ms, ~29.2 fps average). The
cut engine cuts on time, and Remotion composites on a fixed frame grid, so VFR footage makes
graphics drift away from the voice. This converts any VFR recording to a steady frame rate
before anything else touches it. Constant-frame-rate files (most cameras) are left alone.

Usage:
  python tools/prep_recording.py videos/video-1            # check + fix, 30 fps
  python tools/prep_recording.py videos/video-1 --fps 25   # another target rate
  python tools/prep_recording.py videos/video-1 --check    # report only, change nothing

What it does to a VFR file `recording.mp4`:
  writes   videos/video-1/recording-30fps.mp4   (the file every later step uses)
  moves    the original to videos/video-1/original/recording.mp4   (never deleted)
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from encoders import describe, hwaccel_args, video_args

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".m4v", ".webm", ".avi"}
SPREAD_LIMIT = 0.002  # seconds: frame gaps varying more than this = variable frame rate


def frame_gaps(path: Path) -> list[float]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "packet=pts_time", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True)
    pts = sorted(float(x) for x in r.stdout.split() if x and x != "N/A")
    return [b - a for a, b in zip(pts, pts[1:]) if b > a]


def check(path: Path) -> dict:
    gaps = frame_gaps(path)
    if not gaps:
        return {"vfr": False, "fps": 0.0, "min_ms": 0, "max_ms": 0}
    # ignore the odd duplicate/dropped frame at the very ends; judge the body of the file
    body = sorted(gaps)[len(gaps) // 100: len(gaps) - len(gaps) // 100 or None] or gaps
    avg = sum(gaps) / len(gaps)
    return {"vfr": (max(body) - min(body)) > SPREAD_LIMIT, "fps": 1 / avg,
            "min_ms": min(gaps) * 1000, "max_ms": max(gaps) * 1000}


def convert(src: Path, out: Path, fps: int) -> None:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *hwaccel_args(), "-i", str(src),
                    "-map", "0:v:0", "-map", "0:a:0?", "-vf", f"fps={fps}", "-fps_mode", "cfr",
                    *video_args("final"), "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
                    "-movflags", "+faststart", str(out)], check=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--check", action="store_true", help="report only, change nothing")
    args = ap.parse_args()

    project = Path(args.project)
    if not project.is_dir():
        project = Path(__file__).resolve().parent.parent / args.project
    if not project.is_dir():
        sys.exit(f"no project folder at {args.project}")

    suffix = f"-{args.fps}fps"
    files = sorted(p for p in project.iterdir()
                   if p.is_file() and p.suffix.lower() in VIDEO_EXT)
    if not files:
        sys.exit(f"no video files in {project} (put the recording directly in that folder)")

    for f in files:
        if f.stem.endswith(suffix):
            print(f"  ok        {f.name}  (already converted)")
            continue
        info = check(f)
        if not info["vfr"]:
            print(f"  ok        {f.name}  constant {info['fps']:.2f} fps")
            continue
        print(f"  VARIABLE  {f.name}  avg {info['fps']:.2f} fps, frame gaps "
              f"{info['min_ms']:.0f}-{info['max_ms']:.0f} ms")
        if args.check:
            continue
        out = f.with_name(f"{f.stem}{suffix}.mp4")
        print(f"            converting to a steady {args.fps} fps with the {describe()}...")
        convert(f, out, args.fps)
        keep = project / "original"
        keep.mkdir(exist_ok=True)
        shutil.move(str(f), str(keep / f.name))
        print(f"            wrote {out.name}; original moved to original/{f.name}")


if __name__ == "__main__":
    main()
