
# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #

import ffmpeg
import os


def add_metadata(
    input_file,
    output_file,
    title="",
    author="",
    artist="",
    video="",
    audio="",
    subtitle=""
):
    try:
        probe = ffmpeg.probe(input_file)
        streams = probe.get("streams", [])

        options = {
            "map": "0",
            "c": "copy",
            "map_metadata": "-1",
        }

        if title:
            options["metadata"] = title

        if author:
            options["metadata:g:author"] = author

        if artist:
            options["metadata:g:artist"] = artist

        video_index = 0
        audio_index = 0
        subtitle_index = 0

        for stream_info in streams:
            stream_type = stream_info.get("codec_type")

            if stream_type == "video":
                if video:
                    options[f"metadata:s:v:{video_index}"] = video
                video_index += 1

            elif stream_type == "audio":
                if audio:
                    options[f"metadata:s:a:{audio_index}"] = audio
                audio_index += 1

            elif stream_type == "subtitle":
                if subtitle:
                    options[f"metadata:s:s:{subtitle_index}"] = subtitle
                subtitle_index += 1

        stream = ffmpeg.input(input_file)
        output = ffmpeg.output(stream, output_file, **options)

        ffmpeg.run(output, overwrite_output=True)

        if not os.path.exists(output_file):
            raise RuntimeError("Output file was not created")

        if os.path.getsize(output_file) < 100000:
            raise RuntimeError("Output file is too small")

        return output_file

    except Exception as e:
        print(f"❌ Metadata processing failed: {e}")

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                pass

        raise


# ------------------------- #
# Don't Remove Credit
# Ask Doubt @AU_Bot_Discussion
# Owner @Mr_Mohammed_29
# ------------------------- #