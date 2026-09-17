---
name: ai-video-producer
description: End-to-end AI video creation pipeline for academic & tech tutorials. Integrates voice cloning (CosyVoice2/F5-TTS/Edge-TTS), automated script alignment, screen recording compilation, Whisper subtitle synchronization, and video assembly.
---

# AI Video Producer Skill

This skill automates the full production workflow of tech and academic tutorial videos:
1. **Script Drafting**: Structuring crisp, high-retention tutorial scripts with hook, step-by-step demonstration, and key takeaway.
2. **Voice Cloning & TTS**: Synthesize voiceover using your cloned personal timbre (CosyVoice 2 / F5-TTS / GPT-SoVITS) or zero-latency edge voice.
3. **Screen Recording & B-Roll Assembly**: Concatenate screen recordings, diagrams, code blocks, and slide highlights.
4. **Subtitle Sync**: Generate perfectly timed `.srt` subtitles using Whisper and burn/softcode into the final video.

## Quick CLI Usage

Run with Python (`py -3.11`):

```powershell
# 1. Synthesize audio from script
py -3.11 skills/ai-video-producer/scripts/build_tutorial_video.py --script "tutorial.txt" --audio-out "voiceover.wav"

# 2. Assemble video (screen recording + voiceover + subtitles)
py -3.11 skills/ai-video-producer/scripts/build_tutorial_video.py --video "recording.mp4" --audio "voiceover.wav" --output "final_video.mp4"
```
