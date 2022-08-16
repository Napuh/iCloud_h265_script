import argparse
from time import sleep
import click
from pathlib import Path
from subprocess import call, check_output
import os
from tqdm import tqdm


def compress_folder(input, output):

    print(f"Compressing {input} videos to {output} folder")

    file_extensions = ["mp4", "MP4", "mov", "MOV"]

    for file_ext in file_extensions:
        print(f"Scanning for files with extension {file_ext}")
        video_files = [fp.absolute() for fp in Path(input).glob(f"*.{file_ext}")]
        check_codec_cmd = 'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{fp}"'
        codecs = []
        for fp in video_files:
            codecs.append(
                check_output(check_codec_cmd.format(fp=fp), shell=True)
                .strip()
                .decode("UTF-8")
            )
        files_to_process = [
            fp for fp, codec in zip(video_files, codecs) if codec != "hevc"
        ]
        print(
            f"\nFound ({len(video_files)}) files with {file_ext} extension to process"
        )
        if len(video_files) > 0:
            print("Processing files...")
            for fp in tqdm(
                files_to_process, desc=f"Converting {file_ext} files", unit="video"
            ):
                new_fp = f"{output}/{fp.name}"
                convert_cmd = f'ffmpeg -loglevel error -nostats -hide_banner -y -i "{fp}" -map_metadata 0 -tag:v hvc1 -vcodec libx265 -x265-params log-level=error -crf 28 "{new_fp}"'
                os.system(convert_cmd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        help="input folder in which the videos are located",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        help="output folder to save videos. If left blank, a new folder will be created in the same directory as the input",
        type=str,
        required=False,
    )

    args = parser.parse_args()

    if not args.output:
        args.output = args.input + "_compressed"

    if not Path(args.input).exists():
        print("Error: input folder does not exist")
        exit()

    if not Path(args.output).exists():
        Path(args.output).mkdir(parents=True)

    compress_folder(args.input, args.output)
