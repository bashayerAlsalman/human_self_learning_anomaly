import os, re, shutil
import moviepy.editor as mp
import argparse
from datetime import date
import logging
import numpy as np
#Global varible
too_short = []
logger: logging.Logger

def humanSort(text):  # Sort function for strings w/ numbers
    convText = lambda seq: int(seq) if seq.isdigit() else seq.lower()
    arrayKey = lambda key: [convText(s) for s in re.split('([0-9]+)', key)]  # Split numbers and chars, base function for sorted
    return sorted(text, key=arrayKey)


def normDur(dir_path, dest_path, fileName, avg_fps, fps, erase_frames):  # Normalize duration of video, partitioning the video in smaller videos

    print(f'Normalizing video ({fileName}) duration...')
    logger.info(f'Normalizing video ({fileName}) duration...')

    size = int((len(os.listdir(dir_path)))/avg_fps)                                              # Get duration video to normalize after
    
    print(f'Total number of sub videos of ({fileName}) is {size}')
    logger.info(f'Total number of sub videos of ({fileName}) is {size}')

    for x in [x for x in os.listdir(dir_path) if x.isdigit()]:
        if not os.path.exists(os.path.join(dest_path,x)):
            os.makedirs(os.path.join(dest_path,x))

        print (f'\n HHH {x}')
        imgs = [os.path.join(dest_path,x, img) for img in humanSort(os.listdir(os.path.join(dest_path,x))) if '.png' in img]  # Get list of full path of each images in each sub seq folder

        clips = [mp.ImageClip(m).set_duration(1 / fps-0.0000001) for m in imgs]              # Create ImageClip with duration per image
        print(imgs)
        concat_clip = mp.concatenate_videoclips(clips,  method="compose")
        concat_clip.write_videofile(os.path.join(dest_path, fileName[:-4] + "_" + x + '.mp4'), fps=fps)
        shutil.rmtree(os.path.join(dest_path, x)) if erase_frames else None

    print(f'Successfully {fileName} normalized!')
    logger.info(f'Successfully {fileName} normalized!')



def read_paths(root_frames, root_dest, avg_fps, fps, erase_frames):
    for folder in humanSort(os.listdir(root_frames)):
        path_type_frames = os.path.join(root_frames, folder)
        path_dest        = os.path.join(root_dest, folder)

        for file in humanSort(os.listdir(path_type_frames)):
            dir_path  = os.path.join(path_type_frames, file)
            dest_path = os.path.join(path_dest, file)
            normDur(dir_path, dest_path, file, avg_fps, fps, erase_frames)


    print(f'These folders are to short! {too_short}')
    logger.info(f'These folders are to short! {too_short}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    #Create instance of logger to log the changes in a file
    today = date.today()
    today = today.strftime("%d_%m_%Y__%m_%h_%s")
    logging.basicConfig(filename="./logs/normalize_videos_logs_" + today + ".log",
                        format= '%(asctime)s %(message)s',
                        filemode='w')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Paths and settings
    parser.add_argument('--root_frames',     type=str, default='PATH_TO_FRAMES',          help='root_frames -> directory_to_type_video -> full_video -> frames')
    parser.add_argument('--root_sub_videos', type=str, default='DEST_PATH_TO_SUB_VIDEOS', help='Destination path to sub videos')
    parser.add_argument('--duration',        type=int, default=16,                        help='Seconds, recommended to be multiple of 8, for consistency')
    parser.add_argument('--fps',             type=int, default=30,                        help='FPS to normalize (RECOMMENDED 25~30 FOR C3D!!)')
    parser.add_argument('--erase_frames',    action='store_true',                         help='Erase directories with frames')

    opt = parser.parse_args()

    avg_fps = opt.fps * opt.duration

    read_paths(opt.root_frames, opt.root_sub_videos, avg_fps, opt.fps, opt.erase_frames)
