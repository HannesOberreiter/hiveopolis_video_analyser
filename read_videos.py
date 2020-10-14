import numpy as np
import os
import glob
import csv
import cv2 
import re
# Our Libs
import custom_ocr as ocr

# Definitions
def init():
    global VIDEO_FILE, NAME, JUMP_FRAMES, ADJUST_GAMMA, TRHESHOLD
    VIDEO_FILE = "MVI_1301.MP4"
    NAME = "Pulse test II"
    JUMP_FRAMES = 12000 # If we want to jump the beginning
    ADJUST_GAMMA = True # adjust Gamma
    TRHESHOLD = 7

    # ROI
    global x1, x2, y1, y2, ocr_x1, ocr_x2, ocr_y1, ocr_y2
    offset_x = -150
    offset_y = -170
    x1 = 1300 + offset_x
    x2 = 1800 + offset_x
    y1 = 400  + offset_y
    y2 = 900  + offset_y

    ocr_offset_x = 0
    ocr_offset_y = 0
    ocr_x1 = 45 + ocr_offset_x
    ocr_x2 = 750 + ocr_offset_x
    ocr_y1 = 925  + ocr_offset_y
    ocr_y2 = 1080  + ocr_offset_x

    # Check if video file exists
    if(os.path.isfile(VIDEO_FILE) == False):
        print("Error: No video file found")
        exit()

    return True

def loadVideo():
    global VIDEO_FILE, JUMP_FRAMES
    capture = cv2.VideoCapture(VIDEO_FILE)
    # wait till video is loaded
    while not capture.isOpened():
        capture = cv2.VideoCapture(VIDEO_FILE)
        cv2.waitKey(1000)
        print("Wait for the header")
    # jump forward in frames
    capture.set(cv2.CAP_PROP_POS_FRAMES, JUMP_FRAMES)
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video total frames: {}".format(length) )

    return capture 


def gammaTable():
    global LTABLE
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    global LTABLE
    # Somehow I found the value of `gamma=1.2` to be the best in my case
    invGamma = 1.0 / 1.2
    LTABLE = np.array([((i / 255.0) ** invGamma) * 255
        for i in np.arange(0, 256)]).astype("uint8")
    return True


def adjustGamma(image):
    # apply gamma correction using the lookup table
    return cv2.LUT(image, LTABLE)

def exportData(position, time, values, t_ocr):
    global NAME
    data = zip(time, values, t_ocr)
    print(data)
    with open('results{}_{}.csv'.format(position, NAME), mode='w') as result:
        result = csv.writer(result, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i in data: result.writerow(i)

def frameReader(capture):
    global ADJUST_GAMMA, TRHESHOLD, x1, x2, y1, y2, ocr_x1, ocr_x2, ocr_y1, ocr_y2
    
    # Helper
    w_pixel_array = []
    x_vec = []
    y_vec = []
    t_ocr_temp = []
    t_orc_int_temp = []

    time, values, t_ocr, t_orc_int = [], [], [], []

    second_count = 0        # used to count frames
    n_white_pix_sum = 0     # helper variable to sum white pixel in n amount of frames
    try:
        while True:
            # read video
            flag, frame = capture.read()

            # Break if Video is not ready or Key Click
            if flag != True:
                #print "Frame is not ready"
                cv2.waitKey(1000)
                exportData(1, time, values, t_ocr)
                break
            if 0xFF & cv2.waitKey(10) == 27:
                exportData(2, time, values, t_ocr)
                break

            # Grab Region of Interest (+1 for failsafe reasons)
            roi = frame[y1:y2+1, x1:x2+1]
            text_roi = frame[ocr_y1:ocr_y2+1, ocr_x1:ocr_x2+1]
            text_roi = ocr.convertImage(text_roi)
            text_roi = ocr.readImage(text_roi)
            t_ocr_temp.append(text_roi)
            
            pos_frame = capture.get(1)
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY) # change to grayscale
            
            if (ADJUST_GAMMA == True):
                roi = adjustGamma(roi)

            # check if it was the first run otherwise img_history is same as input for first round
            try:
                img_history
            except:
                img_history = roi
            
            # calculate absdiff
            img_output = cv2.absdiff(roi, img_history)
            img_history = roi # set new history

            # Converting
            img_output = cv2.medianBlur(img_output, 1)
            _, img_output = cv2.threshold(img_output, TRHESHOLD, 255, cv2.THRESH_BINARY)

            # all pixels of image
            n_all_px = img_output.size
            # get all white pixels == changed pixels
            n_white_pix = np.sum(img_output == 255)
            # save into our helper variable
            n_white_pix_sum = n_white_pix_sum + n_white_pix
            # set our frame counter forward
            second_count = second_count + 1

            # if 10 Frames we calculate the difference
            if (second_count == 10):
                # mean and relative value to all pixels of the cropped frame
                relative_white = (n_white_pix_sum / second_count) /  n_all_px * 100

                # add value our vector
                y_vec.extend([relative_white])
                x_vec.extend([pos_frame])

                # move our vector forward
                if (len(x_vec) > 250):
                    y_vec.pop(0)
                    x_vec.pop(0)

                # reset helper
                n_white_pix_sum = 0
                second_count = 0
                
                time.append(pos_frame)
                values.append(relative_white)
                t_ocr_temp = [word.translate ({ord(c): "" for c in "\"'‘!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) for word in t_ocr_temp]
                t_ocr_temp = [word.replace('\r', '').replace('\n', '') for word in t_ocr_temp]
                #t_ocr_temp = t_ocr_temp.replace('\r', '').replace('\n', '')
                #t_ocr_temp = t_ocr_temp.translate ({ord(c): "" for c in "\"'‘!@#$%^&*()[]{};:,./<>?\|`~-=_+"})
                #t_ocr_temp = t_ocr_temp.replace('\r', '').replace('\n', '')
                t_ocr.append(t_ocr_temp)
                print('Number of mean white pixels: {0:.2f}%'.format(relative_white))
                #print('Text: ', t_ocr_temp)
                t_ocr_temp = []


    except KeyboardInterrupt:
        exportData(3, time, values, t_ocr)
        pass


def main():
    global ADJUST_GAMMA
    init()
    capture = loadVideo()
    if(ADJUST_GAMMA == True):
        gammaTable()

    frameReader(capture)


if __name__ == "__main__":
   main()