#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI Video Producer - Tutorial Video Synthesizer and Audio Assembler
Supports screen recording audio replacement, TTS synthesis, and automated FFmpeg muxing.
"""

import os
import sys
import shutil
import argparse
import subprocess
from pathlib import Path

FFMPEG_CANDIDATES = [
    r"C:\Users\12830\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe",
    shutil.which("ffmpeg"),
    shutil.which("ffmpeg.exe")
]

def get_ffmpeg():
    for c in FFMPEG_CANDIDATES:
        if c and Path(c).is_file():
            return str(c)
    return "ffmpeg"

def mux_video_audio(video_path: Path, audio_path: Path, output_path: Path):
    ffmpeg = get_ffmpeg()
    print(f"[*] Muxing video '{video_path}' with audio '{audio_path}'...")
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(output_path)
    ]
    subprocess.run(cmd, check=True)
    print(f"[+] Final tutorial video generated: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="AI Video Producer Workflow Engine")
    parser.add_argument("--video", "-v", help="Screen recording video file (.mp4/.mkv)")
    parser.add_argument("--audio", "-a", help="Voiceover audio file (.wav/.mp3)")
    parser.add_argument("--output", "-o", help="Output video path")
    args = parser.parse_args()

    if args.video and args.audio:
        video_p = Path(args.video).resolve()
        audio_p = Path(args.audio).resolve()
        out_p = Path(args.output).resolve() if args.output else video_p.with_name(f"{video_p.stem}_with_voiceover.mp4")
        mux_video_audio(video_p, audio_p, out_p)
    else:
        print("[!] Please provide --video and --audio to assemble tutorial video.")

if __name__ == "__main__":
    main()
