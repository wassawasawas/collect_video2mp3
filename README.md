collect_video2mp3
===

This script collects video on YouTube from argument listfile written in URLs.
Also, executing in concurrent processing.(Process with 5 multiples if don't giving argument workers).  
After download, convert into mp3 fortmat in the current working directory.

## Requirement
* python 3.6
* youtube-dl
* ffmpeg

## Usage

Check out the collect script for infomation about different options. 
```
python collect.py --help
usage: collect.py [-h] [-e EXECUTE] [-w WORKERS] listfile

positional arguments:
  listfile              Download for URL text list

optional arguments:
  -h, --help            show this help message and exit
  -e EXECUTE, --execute EXECUTE
                        Type of execution [donwload | convert]
  -w WORKERS, --workers WORKERS
                        max_workers threads to execute calls asynchronously
```

Here is the contents of the listfile.
listfile(Plane text)
---
Paste the URL of YouTube you want to download
```
https://www.youtube.com/watch?v=XXXX
https://www.youtube.com/watch?v=XXXX
https://www.youtube.com/watch?v=XXXX
....

```

Once you done install requirements, you can start download video and convert into mp3.

```
python collect.py listfile
```

Seeing outlog like this
```
[ INFO ] [Threading ID:10892] Starting download --> https://www.youtube.com/watch?v=xxxxxx
[ INFO ] [Threading ID:14564] Starting download --> https://www.youtube.com/watch?v=xxxxxx
[ INFO ] [Threading ID:15352] Starting download --> https://www.youtube.com/watch?v=xxxxxx
[ INFO ] [Threading ID:10892] Successfully downloaded.
[ INFO ] [Threading ID:14564] Successfully downloaded.
[ INFO ] [Threading ID:15352] Successfully downloaded.
[ INFO ] [Threading ID:16752] Starting convert --> XXXX.mp4
[ INFO ] [Threading ID:228] Starting convert --> XXXX.mp4
[ INFO ] [Threading ID:7828] Starting convert --> XXXX.webm
[ INFO ] [Threading ID:228] Successfully converted.
[ INFO ] [Threading ID:16752] Successfully converted.
[ INFO ] [Threading ID:7828] Successfully converted.

```

You can find mp3 file in current working directory.

## Only download or convert
If you pass execution type as an argument, only download or convert.

* download
```
python collect.py listfile -e download
```

* convert
convert video files under working directory to mp3 format.
```
python collect.py listfile -e convert
```