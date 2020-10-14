'''
   Extact text from display to get currently playing frequencies and frame.
   Uses opensource cv2 and pytesseract OCR
'''

# Import Libraries
import cv2 
import pytesseract
import numpy as np

# Load Image from File
# f = Filename as string
def loadImage(f):
   img = cv2.imread(f)
   return img

# Not used, maye good idea before converting
def isGray(img):
    if len(img.shape) < 3: return True
    if img.shape[2]  == 1: return True
    b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
    if (b==g).all() and (b==r).all(): return True
    return False

def unsharp_mask(image, kernel_size=(5, 5), sigma=1.0, amount=1.0, threshold=0):
    """Return a sharpened version of the image, using an unsharp mask."""
    blurred = cv2.GaussianBlur(image, kernel_size, sigma)
    sharpened = float(amount + 1) * image - float(amount) * blurred
    sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
    sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
    sharpened = sharpened.round().astype(np.uint8)
    if threshold > 0:
        low_contrast_mask = np.absolute(image - blurred) < threshold
        np.copyto(sharpened, image, where=low_contrast_mask)
    return sharpened

# Convert Image to Grayscale for better Reading, takes image from cv2.imread
def convertImage(img):
   img = unsharp_mask(img)
   img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   img = cv2.fastNlMeansDenoising(img)
   img = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)[1]
   img = cv2.bitwise_not(img)
   return img

def showImage(img):
   cv2.imshow( 'sample image', img)
   cv2.waitKey( 0) # waits until a key is pressed.
   cv2.destroyAllWindows() # destroys the window showing image.
   return True

# Read the Image, takes Grayscale cv2 Object, returns string of text
def readImage(img):
   #configuring parameters for tesseract
   custom_config = r'--oem 3 --psm 6'
   t_string = pytesseract.image_to_string(img, config=custom_config, lang="eng")
   #print(t_string)
   return t_string

# Main if you start the strict direct
def main():
   x = "unknown.png"
   img = loadImage(x)
   img = convertImage(img)
   x = readImage(img)
   print(x)
   return()

if __name__ == "__main__":
   main()