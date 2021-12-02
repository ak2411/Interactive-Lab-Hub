import numpy as np
import cv2
import sys
import imutils
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

img=None

webCam = False
print("hi")
if(len(sys.argv)>1):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True

   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")
print("Is Webcam running? "+ str(webCam))

ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
# csv = open(args["output"], "w")
found = set()

while(True):
   if webCam:
        ret, img = cap.read()
        frame = imutils.resize(img, width=400)
        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            text = "{}".format(barcodeData)
            print (text)
            cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # if the barcode text is currently not in our CSV file, write
        # the timestamp + barcode to disk and update the set
            # if barcodeData not in found:
            #     csv.write("{},{}\n".format(datetime.datetime.now(),
            #     barcodeData))
            #     csv.flush()
            #     found.add(barcodeData)
        # cv2.imshow("Barcode Reader", frame)
        key = cv2.waitKey(1) & 0xFF
        # print("hi")
        # # if the `s` key is pressed, break from the loop
        if key == ord("s"):
            break
        # csv.close()
cv2.destroyAllWindows()
