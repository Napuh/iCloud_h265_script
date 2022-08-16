# iCloud_h265_script
Python script to convert iCloud videos to h265 codec in order to save space in iCloud photos storage

iCloud videos recorded with iPhones take up a lot of space in the cloud storage. I've found that the best way to reduce the size of the videos is to convert them to h265 codec and upload them to iCloud later on. However, Apple is a bit finnicky with how they manage video and metadata.

To compress your video library, I would recommend using the following steps, as I found they are the most efficient:

1. Enter the iCloud Photos webapp, in iCloud.com
2. Select the video library
3. Download videos in batches no larger than 100 videos. If you download a batch larger than 100 videos, the download is likely to fail.
4. Place all videos in a folder. Extensions should be .mov or .mp4
5. Run the script, setting the input folder to the folder containing the videos and the output folder to the folder you want to store the h265 videos. If you do not set a output folder, the script will create a new folder in the same location as the input folder.
6. Wait for the script to finish.
(Optional) Filter all videos with wrong date metadata, you can see what videos have the wrong metadata with the following command:
```bash
exiftool *.mp4 | grep 'Media\ Create\ Date\|File\ Name' | grep 'File\ Name\| 0000:00:00'
```
7. Upload the h265 videos to your iCloud *drive* storage, preferably in a batches and in different folders.
8. Now in your phone, download the h265 videos in the iCloud Drive app and import them to the gallery via the share menu.
9. In your gallery app you will have the original video next to the h265 one, the only difference between them is the location metadata. To solve this, you can long press the location of the original file to copy it, and then long press on the location of the h265 video and paste it. Then, you can safely delete the original video. Repeat this for all videos in the library. (This could take a while, but the cloud space saving is worth it.)



### Warnings
Currently, some videos cannot be converted as ffmpeg throws an error.

Apple handles video metadata in a weird way, and location metadata is not detected right although ffmpeg copies it correctly. To fix this, you can copy and paste each video location in the iPhone's gallery app.

As part of this weird metadata handling, some videos are downloaded from iCloud with no date metadata whatsoever. I recommend filter out these videos using exiftool and removing them before running the script.

To stop the script you have to press Ctrl+C repeatedly, as the SIGINT signal will be caught by the ffmpeg processes, not the script. This is a work in progress.
