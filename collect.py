# -*- coding: utf-8 -*-
##########################################################################
#
# collect_video2mp3
#
##########################################################################

"""
This script collects video on YouTube from argument listfile written in URLs.
Also, executing in concurrent processing.(Process with 5 multiples if don't giving argument workers).
After download, convert into mp3 fortmat in the current working directory.
"""

import sys
import os
import argparse
import glob
import threading
import re
from logging import getLogger, StreamHandler, DEBUG, Formatter
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import youtube_dl

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
WORK_DIR = os.path.join(BASE_DIR, "work")

parser = argparse.ArgumentParser()
parser.add_argument("listfile", type=argparse.FileType('r'),
                    help='Download for URL text list')
parser.add_argument('-e', '--execute',
                    help='Type of execution [donwload | convert]')
parser.add_argument('-w', '--workers', default=5, type=int,
                    help='max_workers threads to execute calls asynchronously')
args = parser.parse_args()

# Set logging
logger = getLogger(__name__)
logger.setLevel(DEBUG)
stream_handler = StreamHandler()
stream_handler.setLevel(DEBUG)
handler_format = Formatter('[ %(levelname)s ] %(message)s')
stream_handler.setFormatter(handler_format)
logger.addHandler(stream_handler)

# Check if the working directory exists. If does not, create it.
if not os.path.isdir(WORK_DIR):
    os.mkdir("work")

def download(URL):
    """
    download from URL
    :param URL: URL's link of movie
    """
    logger.info("[Threading ID:{0}] Starting download --> {1}".format(threading.get_ident(), URL))
    options = {
        # 'forceurl': True,
        # 'forcetitle': True,
        'quiet': True,
        'outtmpl': os.path.join(WORK_DIR, '%(title)s.%(ext)s')
    }
    try:
        with youtube_dl.YoutubeDL(options) as ydl:
            ydl.download([URL])
    except Exception as err:
        watch = URL.split('/')
        logger.error(err, "Failed in download process:{0}".format(watch[-1]))
        return 8
    else:
        logger.info("[Threading ID:{}] Successfully downloaded.".format(threading.get_ident()))
        return

def cvt2mp3(video_file):
    """
    convert video file into mp3
    :param video_file: downloaded vide file from youtube
    """
    logger.info("[Threading ID:{0}] Starting convert --> {1}".
                format(threading.get_ident(), os.path.basename(video_file)))
    root = os.path.splitext(video_file)
    outputfile = '{}.mp3'.format(root[0])
    # generate command
    gencmd = 'ffmpeg -y -i {0} -ab 320k {1} -loglevel error'.format(video_file, outputfile)
    try:
        os.system(gencmd)
    except Exception as err:
        logger.error(err, "Failed in convert download file to mp3:{}".format(video_file))
        return 8
    else:
        logger.info("[Threading ID:{}] Successfully converted.".format(threading.get_ident()))
        os.remove(video_file)
        return

def main():
    """
    main process
    """
    # Number of max_workers threads to execute calls asynchronously.
    max_thread_process = args.workers
    # doownload URL textlist you want
    download_list = []
    for i in args.listfile:
        download_list.append(i.rstrip('\r\n'))

    if not download_list:
        logger.warning("Argument listfile is empty.")
        sys.exit(8)

    if args.execute:
        if args.execute == "download":
            with ThreadPoolExecutor(max_workers=max_thread_process,
                                    thread_name_prefix="thread") as executor:
                # Download in threading
                [executor.submit(download, dl) for dl in download_list]
                sys.exit()
        elif args.execute == "convert":
            video_list = glob.glob('{}/*.*[!*.part]'.format(WORK_DIR))
            if not video_list:
                logger.warning("Video file does not exist.")
            else:
                with ThreadPoolExecutor(max_workers=max_thread_process,
                                        thread_name_prefix="thread") as executor:
                    # Replace space to underscore in video file
                    for bfr_f in video_list:
                        os.rename(bfr_f, os.path.join(WORK_DIR, re.sub(" ", "_", bfr_f)))
                    # Convert in threading
                    [executor.submit(cvt2mp3, f) for f in
                     glob.glob('{}/*.*[!*.part]'.format(WORK_DIR))]
                    sys.exit()
        else:
            logger.warning("Arguments should be selected from ['download', convert].")
            sys.exit(8)

    # Download from list file
    with ThreadPoolExecutor(max_workers=max_thread_process,
                            thread_name_prefix="thread") as executor:
        # Download in threading
        [executor.submit(download, dl) for dl in download_list]

    # wait for download file generated
    sleep(5)

    video_list = glob.glob('{}/*.*[!*.part]'.format(WORK_DIR))
    if not video_list:
        logger.warning("Video file does not exist.")
        sys.exit(8)

    # Convert mp3 format
    with ThreadPoolExecutor(max_workers=max_thread_process,
                            thread_name_prefix="thread") as executor:
        # Replace space to underscore in video file
        for bfr_f in video_list:
            os.rename(bfr_f, os.path.join(WORK_DIR, re.sub(" ", "_", bfr_f)))
        # Convert in threading
        [executor.submit(cvt2mp3, f) for f in
         glob.glob('{}/*.*[!*.part]'.format(WORK_DIR))]

if __name__ == "__main__":
    main()
