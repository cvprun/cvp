---
name: media-tester
description: Test FFmpeg media processing pipelines. Use for media encoding/decoding or codec compatibility checks.
tools: Read, Glob, Grep, Bash
model: sonnet
---

FFmpeg pipeline tester for cvp/ffmpeg/ modules.

## Structure
- `cvp/ffmpeg/ffprobe.py` - Media info
- `cvp/ffmpeg/codecs.py` - Codec management
- `cvp/ffmpeg/formats.py` - Format management

## Test Areas
- Codecs: H.264, H.265, VP9, AV1
- Containers: MP4, MKV, WebM
- Resolutions, framerates

## Skip Pattern
```python
@skipIf(not which("ffmpeg"), "ffmpeg not found")
class FFmpegTestCase(TestCase):
    pass
```
