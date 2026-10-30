"""Make every raw recording in a project safe to cut: constant frame rate, normal voice level.

Screen recorders (Panda, OBS, Loom, ...) usually write VARIABLE frame rate video: the gap
between frames wanders (measured on a Panda recording: 28-139 ms, ~29.2 fps average). The
cut engine cuts on time, and Remotion composites on a fixed frame grid, so VFR footage makes
graphics drift away from the voice. This converts any VFR recording to a steady frame rate
before anything else touches it. Constant-frame-rate files (most cameras) are left alone.

It also checks the voice level. Every later gain (SFX cues, the music bed) is set against a
voice at about -14 LUFS AS PLAYED (a mono voice is duplicated to both speakers by the cut, so
it is measured that way: -17 LUFS mono reads -14 in stereo). That is what a clip-on mic gives
and what YouTube normalises to. Webcam and laptop mics often come in far quieter (measured on
a webcam screen recording: -36 LUFS as played), so the music and effects would bury the voice.
A recording outside -17..-11 LUFS gets a flat gain to -14, with a limiter so the loudest
words cannot clip. Nothing else about the sound is changed.

Usage:
  python tools/prep_recording.py videos/video-1            # check + fix, 30 fps
  python tools/prep_recording.py videos/video-1 --fps 25   # another target rate
  python tools/prep_recording.py videos/video-1 --check    # report only, change nothing

What it does to a VFR file `recording.mp4`:
  writes   videos/video-1/recording-30fps.mp4   (the file every later step uses)
  moves    the original to videos/video-1/original/recording.mp4   (never deleted)
A steady-frame-rate file that only needs the level fix becomes recording-level.mp4 (picture
copied untouched), with the original moved the same way.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

from encoders import describe, hwaccel_args, video_args

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".m4v", ".webm", ".avi"}
SPREAD_LIMIT = 0.002  # seconds: frame gaps varying more than this = variable frame rate
VOICE_LUFS = -14.0    # voice level AS PLAYED that every SFX/music gain in this repo assumes
LEVEL_RANGE = (-17.0, -11.0)  # inside this, leave the sound alone


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


def loudness(path: Path) -> float | None:
    """Integrated loudness (LUFS) of the first audio stream AS PLAYED: a mono track is measured
    duplicated to both channels, the way render_cuts.py delivers it. None if there is no audio."""
    ch = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                         "stream=channels", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    if not ch.stdout.strip():
        return None
    af = ("pan=stereo|c0=c0|c1=c0," if ch.stdout.strip() == "1" else "") + "ebur128"
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(path), "-map", "0:a:0", "-af", af,
                        "-f", "null", "-"], capture_output=True, text=True)
    found = re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", r.stderr, re.M)
    return float(found[-1]) if found and float(found[-1]) > -70 else None


def convert(src: Path, out: Path, fps: int | None, gain_db: float) -> None:
    """fps=None copies the picture; gain_db=0 leaves the sound's level alone."""
    video = (["-vf", f"fps={fps}", "-fps_mode", "cfr", *video_args("final")] if fps
             else ["-c:v", "copy"])
    audio = (["-af", f"volume={gain_db:.1f}dB,alimiter=limit=0.89:level=disabled"] if gain_db else [])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *(hwaccel_args() if fps else []),
                    "-i", str(src), "-map", "0:v:0", "-map", "0:a:0?", *video, *audio,
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
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
        done_fps = f.stem.endswith(suffix)
        info = {"vfr": False} if done_fps else check(f)
        if done_fps:
            print(f"  ok        {f.name}  (already a steady {args.fps} fps)")
        elif info["vfr"]:
            print(f"  VARIABLE  {f.name}  avg {info['fps']:.2f} fps, frame gaps "
                  f"{info['min_ms']:.0f}-{info['max_ms']:.0f} ms")
        else:
            print(f"  ok        {f.name}  constant {info['fps']:.2f} fps")

        lufs = None if f.stem.endswith("-level") else loudness(f)
        gain = 0.0
        if lufs is not None and not LEVEL_RANGE[0] <= lufs <= LEVEL_RANGE[1]:
            gain = VOICE_LUFS - lufs
            print(f"  {'QUIET' if gain > 0 else 'LOUD':<8}  voice at {lufs:.1f} LUFS: "
                  f"{gain:+.1f} dB brings it to {VOICE_LUFS:.0f}")
        elif lufs is not None:
            print(f"  ok        voice at {lufs:.1f} LUFS")

        if args.check or not (info["vfr"] or gain):
            continue
        out = f.with_name(f"{f.stem}{suffix if info['vfr'] else '-level'}.mp4")
        what = [f"a steady {args.fps} fps with the {describe()}"] if info["vfr"] else []
        what += [f"the voice level {gain:+.1f} dB"] if gain else []
        print(f"            fixing {' and '.join(what)}...")
        convert(f, out, args.fps if info["vfr"] else None, gain)
        keep = project / "original"
        keep.mkdir(exist_ok=True)
        shutil.move(str(f), str(keep / f.name))
        print(f"            wrote {out.name}; original moved to original/{f.name}")


if __name__ == "__main__":
    main()
