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

        # General metadata
        if title:
            options["metadata"] = f"title={title}"

        if author:
            options["metadata:g"] = f"author={author}"

        if artist:
            options["metadata:g"] = f"artist={artist}"

        # Track metadata
        video_index = 0
        audio_index = 0
        subtitle_index = 0

        for item in streams:
            stream_type = item.get("codec_type")

            if stream_type == "video":
                if video:
                    options[f"metadata:s:v:{video_index}"] = f"title={video}"
                video_index += 1

            elif stream_type == "audio":
                if audio:
                    options[f"metadata:s:a:{audio_index}"] = f"title={audio}"
                audio_index += 1

            elif stream_type == "subtitle":
                if subtitle:
                    options[f"metadata:s:s:{subtitle_index}"] = f"title={subtitle}"
                subtitle_index += 1

        stream = ffmpeg.input(input_file)

        output = ffmpeg.output(
            stream,
            output_file,
            format="matroska",
            **options
        )

        print("METADATA COMMAND:", " ".join(ffmpeg.compile(output)))

        ffmpeg.run(
            output,
            overwrite_output=True,
            capture_stderr=True
        )

        if not os.path.exists(output_file):
            raise RuntimeError("Output file was not created")

        if os.path.getsize(output_file) < 100000:
            raise RuntimeError("Output file is too small")

        return output_file

    except ffmpeg.Error as e:
        print("METADATA FFMPEG ERROR:", e)

        if e.stderr:
            print(
                "METADATA FFMPEG STDERR:",
                e.stderr.decode("utf-8", errors="replace")
            )

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                pass

        raise

    except Exception as e:
        print("METADATA ERROR:", repr(e))

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
