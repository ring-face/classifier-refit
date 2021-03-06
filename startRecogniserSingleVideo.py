#!/usr/bin/env python3

import logging
import sys
from ringFace.recogniser.singleVideo import recognition
import multiprocessing as mp



logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)


if __name__ == '__main__':

    if len(sys.argv) == 1:
        logging.error(f"usage: python3 {str(sys.argv[0])} /path/video.mp4")
        sys.exit(1)

    logging.debug(f"Argument List: {str(sys.argv)}")
    videoFile = sys.argv[1]

    ringEvent = {
        'eventName':'_commandline'
    }



    # unify the parallelism setup as spaws on both mac and linux
    mp.set_start_method('spawn')

    result = recognition(videoFile, ringEvent=ringEvent)

    logging.info(result)