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
            "format": "matroska",
        }

        # -------------------------
        # Global metadata
        # -------------------------

        metadata = []

        if title:
            metadata.append(f"title={title}")

        if author:
            metadata.append(f"author={author}")

        if artist:
            metadata.append(f"artist={artist}")

        if metadata:
            options["metadata"] = metadata

        # -------------------------
        # Track metadata
        # -------------------------

        video_index = 0
        audio_index = 0
        subtitle_index = 0

        for item in streams:
            stream_type = item.get("codec_type")

            if stream_type == "video":

                if video:
                    options[
                        f"metadata:s:v:{video_index}"
                    ] = f"title={video}"

                video_index += 1

            elif stream_type == "audio":

                if audio:
                    options[
                        f"metadata:s:a:{audio_index}"
                    ] = f"title={audio}"

                audio_index += 1

            elif stream_type == "subtitle":

                if subtitle:
                    options[
                        f"metadata:s:s:{subtitle_index}"
                    ] = f"title={subtitle}"

                subtitle_index += 1

        # -------------------------
        # FFmpeg
        # -------------------------

        stream = ffmpeg.input(input_file)

        output = ffmpeg.output(
            stream,
            output_file,
            **options
        )

        command = ffmpeg.compile(output)

        print(
            "METADATA COMMAND:",
            " ".join(command)
        )

        ffmpeg.run(
            output,
            overwrite_output=True,
            capture_stdout=True,
            capture_stderr=True
        )

        # -------------------------
        # Validate output
        # -------------------------

        if not os.path.exists(output_file):
            raise RuntimeError(
                "Metadata output file was not created"
            )

        size = os.path.getsize(output_file)

        if size < 100000:
            raise RuntimeError(
                f"Metadata output is too small: {size} bytes"
            )

        print(
            f"✅ Metadata processing successful: {size} bytes"
        )

        return output_file

    except ffmpeg.Error as e:

        print(
            "❌ METADATA FFMPEG ERROR:",
            e
        )

        if e.stderr:
            print(
                "❌ METADATA FFMPEG STDERR:"
            )

            print(
                e.stderr.decode(
                    "utf-8",
                    errors="replace"
                )
            )

        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                pass

        raise

    except Exception as e:

        print(
            "❌ METADATA ERROR:",
            repr(e)
        )

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
