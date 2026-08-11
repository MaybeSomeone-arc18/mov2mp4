# Attributions

## FFmpeg

This software uses code of FFmpeg (http://ffmpeg.org) licensed under the GPLv3 and its source can be downloaded from https://github.com/FFmpeg/FFmpeg.

The bundled compiled binaries are provided by reputable third-party maintainers:

### macOS FFmpeg Binary
- **Provider**: [OSXExperts](https://www.osxexperts.net/)
- **Source URL**: https://www.osxexperts.net/ffmpeg9arm.zip
- **Architecture**: Natively compiled for Apple Silicon (arm64)
- **Version**: 9.0
- **License / Configuration**: The binary is compiled with `--enable-gpl` and is therefore **GPL-licensed**. It does not contain the `--enable-nonfree` flag.
- *Note: MOV2MP4 bundles this GPL-licensed executable in an unmodified form but is itself distributed independently.*

### Windows FFmpeg Binary
- **Provider**: [BtbN / FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds)
- **Source URL**: https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2026-08-10-13-17/ffmpeg-N-126039-g6bbc22dc09-win64-gpl.zip
- **Architecture**: Native Windows x64
- **Version/Build**: autobuild-2026-08-10-13-17 (Commit g6bbc22dc09)
- **License / Configuration**: Provided as a statically linked GPL-licensed binary (`win64-gpl`). It is compiled with `--enable-gpl` and explicitly excludes `--enable-nonfree`.

FFmpeg is a trademark of Fabrice Bellard, originator of the FFmpeg project.
