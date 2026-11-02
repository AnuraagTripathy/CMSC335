"""Render scenes and copy the mp4s into videos/.  Usage: python render.py [01 02 ...]  (default: all)"""
import glob, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCENES = os.path.join(HERE, "scenes")
wanted = sys.argv[1:]
MEDIA = os.environ.get("MEDIA", "media")  # separate dirs let two renders run in parallel
for path in sorted(glob.glob(os.path.join(SCENES, "[0-9][0-9]_*.py"))):
    stem = os.path.splitext(os.path.basename(path))[0]
    if wanted and stem[:2] not in wanted:
        continue
    cls = re.search(r"class (\w+)\(ExamScene\)", open(path).read()).group(1)
    r = subprocess.run(["manim", "-qm", "--media_dir", "../" + MEDIA, os.path.basename(path), cls],
                       cwd=SCENES, capture_output=True, text=True)
    src = os.path.join(HERE, MEDIA, "videos", stem, "720p30", cls + ".mp4")
    if r.returncode or not os.path.exists(src):
        print(f"FAILED {stem}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
        continue
    shutil.copy(src, os.path.join(HERE, "videos", stem + ".mp4"))
    if os.path.exists(src[:-4] + ".srt"):  # subtitles written by manim-voiceover
        shutil.copy(src[:-4] + ".srt", os.path.join(HERE, "videos", stem + ".srt"))
    print(f"ok {stem}  {os.path.getsize(src) / 1e6:.1f} MB")
