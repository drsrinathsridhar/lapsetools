import random
import cv2
import sys
import os
import argparse
import glob
import numpy as np
from tqdm import tqdm

Parser = argparse.ArgumentParser(description='Create star trails.')
Parser.add_argument('-i', '--input-dir', help='Input directory with JPG files.', required=True)
Parser.add_argument('-o', '--output-dir', help='Output directory.', required=False, default='./output')
Parser.add_argument('-r', '--fg-replace-frame', help='Replace final foreground with foreground from this frame.', required=False, default=0, type=int)
Parser.add_argument('-l', '--limit', help='Limit number of stacked frames. Maximum supported is 10000.', required=False, default=10000, type=int)
Parser.add_argument('-v', '--visualize', help='Visualize trails.', action='store_true')
Parser.set_defaults(visualize=False)

if __name__ == '__main__':
    Args, _ = Parser.parse_known_args()
    if len(sys.argv) <= 1:
        Parser.print_help()
        exit()

    BasePath = Args.input_dir
    AllFiles = glob.glob(BasePath + '/*.jpg')
    AllFiles.sort()
    # random.shuffle(AllFiles)
    assert len(AllFiles) > 0
    FrameLimit = min(Args.limit, len(AllFiles))
    if os.path.exists(Args.output_dir) is False:
        os.makedirs(Args.output_dir)

    print('[ INFO ]: Using foreground replace frame:', AllFiles[Args.fg_replace_frame])
    ReplaceFrame = cv2.imread(AllFiles[Args.fg_replace_frame])
    DarkFrame = cv2.imread(AllFiles[0])
    print('[ INFO ]: Generating dark frame...')
    for i in tqdm(range(1, FrameLimit)):
        Image = cv2.imread(AllFiles[i], -1)
        # Darken blend formula: https://en.wikipedia.org/wiki/Blend_modes
        DarkFrame = np.minimum(DarkFrame, Image)
    # DarkFrame = np.maximum(DarkFrame, ReplaceFrame)

    THRESHOLD = 10 # PARAM
    DarkFrameGray = cv2.cvtColor(DarkFrame, cv2.COLOR_BGR2GRAY)
    DarkMask = np.zeros_like(DarkFrameGray)
    FGMask = DarkFrameGray > THRESHOLD
    DarkMask[FGMask] = 255
    cv2.imwrite(os.path.join(Args.output_dir, 'DarkFrame.jpg'), DarkFrame)
    cv2.imwrite(os.path.join(Args.output_dir, 'DarkMask.jpg'), DarkMask)

    if Args.visualize:
        cv2.namedWindow('Trail', cv2.WINDOW_AUTOSIZE)
    TrailImage = np.zeros_like(DarkFrame)
    print('[ INFO ]: Generating trails...')
    for i in tqdm(range(0, FrameLimit)):
        Image = cv2.imread(AllFiles[i], -1)
        # Lighten blend formula: https://en.wikipedia.org/wiki/Blend_modes
        TrailImage = np.maximum(TrailImage, Image)
        MaskedTrail = TrailImage
        MaskedTrail[FGMask] = ReplaceFrame[FGMask]

        cv2.imwrite(os.path.join(Args.output_dir, 'frame'+str(i).zfill(6)+'.jpg'), MaskedTrail)

        if Args.visualize:
            FlattenedImageViz = cv2.resize(TrailImage, (600, 400), cv2.INTER_CUBIC)
            cv2.imshow('Trail', FlattenedImageViz)

            Key = cv2.waitKey(1)
            if Key == 27:
                break
            else:
                continue
