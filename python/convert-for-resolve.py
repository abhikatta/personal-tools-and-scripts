"""Convert H.264/H.265 clips to DNxHR so DaVinci Resolve (free, Linux) can play them."""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

EXTS = {".mp4", ".mov"}

EXAMPLES = """\
examples:
  %(prog)s                          all mp4/mov in the current folder
  %(prog)s ~/Videos/trip            all mp4/mov in that folder
  %(prog)s DJI_0012.MP4             one file
  %(prog)s DJI_0012.MP4 DJI_0015.MP4 ~/Videos/other
                                    a mix of files and folders
  %(prog)s DJI_00*.MP4              a pattern (the shell expands it, and it
                                    is case-sensitive, so *.mp4 will not
                                    match .MP4)
  %(prog)s -r ~/Videos/trip         include subfolders
  %(prog)s --10bit D-Log_clip.MP4   10-bit output for D-Log M footage

notes:
  Output goes to a 'converted/' folder next to each source file.
  Files that are already converted are skipped.
  Default is 8-bit DNxHR LB (small, light). Use --10bit for D-Log M clips;
  those files are huge (roughly 10-20 GB per minute at 4K60).
  Conversion does not repair damaged footage, it only re-encodes it.
"""


def collect(paths, recursive):
    files = []
    for arg in paths:
        p = Path(arg).expanduser()
        if p.is_dir():
            it = p.rglob("*") if recursive else p.iterdir()
            for f in sorted(it):
                if (
                    f.is_file()
                    and f.suffix.lower() in EXTS
                    and "converted" not in f.parent.parts
                ):
                    files.append(f)
        elif p.is_file():
            files.append(p)
        else:
            print(f"Skipping, not found: {arg}", file=sys.stderr)
    return files


def convert(src, tenbit):
    out_dir = src.parent / "converted"
    out = out_dir / f"{src.stem}_edit.mov"
    part = out.with_name(out.name + ".part")

    if out.exists():
        print(f"Already done: {src.name}")
        return True

    out_dir.mkdir(exist_ok=True)
    profile, pix_fmt = (
        ("dnxhr_hqx", "yuv422p10le") if tenbit else ("dnxhr_lb", "yuv422p")
    )
    cmd = [
        "ffmpeg",
        "-nostdin",
        "-y",
        "-i",
        str(src),
        "-c:v",
        "dnxhd",
        "-profile:v",
        profile,
        "-pix_fmt",
        pix_fmt,
        "-c:a",
        "pcm_s16le",
        "-f",
        "mov",
        str(part),
    ]

    print(f"Converting: {src.name} ({profile})")
    try:
        result = subprocess.run(cmd)
    except KeyboardInterrupt:
        part.unlink(missing_ok=True)
        raise

    if result.returncode != 0:
        part.unlink(missing_ok=True)
        return False
    part.replace(out)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Convert mp4/mov clips to DNxHR .mov files for DaVinci Resolve.",
        epilog=EXAMPLES,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="files and/or folders (default: current folder)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="search folders recursively",
    )
    parser.add_argument(
        "--10bit",
        dest="tenbit",
        action="store_true",
        help="use 10-bit DNxHR HQX instead of 8-bit LB (for D-Log M)",
    )
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found. Install it with: sudo apt install ffmpeg")

    files = collect(args.paths, args.recursive)
    if not files:
        sys.exit("No mp4/mov files found.")

    failed = []
    try:
        for f in files:
            if not convert(f, args.tenbit):
                failed.append(f)
    except KeyboardInterrupt:
        sys.exit("\nStopped.")

    print(f"\nDone. {len(files) - len(failed)} ok, {len(failed)} failed.")
    for f in failed:
        print(f"  failed: {f}", file=sys.stderr)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
