'''
    Simple script to test our offsets
'''

import cv2

# Our Offsets
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

def loadVideo(VIDEO_FILE):
    capture = cv2.VideoCapture(VIDEO_FILE)
    # wait till video is loaded
    while not capture.isOpened():
        capture = cv2.VideoCapture(VIDEO_FILE)
        cv2.waitKey(1000)
        print("Wait for the header")
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print( "Video total frames: {}".format(length) )

    return capture 

def showImage(img):
   cv2.namedWindow('border',cv2.WINDOW_NORMAL)
   cv2.resizeWindow('border', 600, 400)
   #cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
   cv2.rectangle(img, (ocr_x1, ocr_y1), (ocr_x2, ocr_y2), (0,255,0), 2)
   cv2.imshow( 'border', img)
   cv2.waitKey( 0) # waits until a key is pressed.
   cv2.destroyAllWindows() # destroys the window showing image.
   return True

# Main if you start the strict direct
def main():
    capture = loadVideo("MVI_1301.MP4")
    flag, frame = capture.read()
    showImage(frame)

if __name__ == "__main__":
   main()

