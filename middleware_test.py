import cv2
import numpy as np
import sys

import darknet

img = cv2.resize(cv2.imread('images/frame3.jpg'), (416,416))
print(sys.getsizeof(img))
img_encoded = cv2.imencode('.jpg', img)[1]
print(sys.getsizeof(img_encoded))

img_bytes = img_encoded.tobytes()  # bytes class

img_bytes_main = img_bytes

print(sys.getsizeof(img_bytes))

# hex string
img_hex = img_bytes.hex()
print(type(img_hex))
print(sys.getsizeof(img_hex))

# reconstruction

img_bytes = bytes.fromhex(img_hex)

# sanity test
nparr = np.frombuffer(img_bytes, np.byte)
img2 = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED) # , cv2.IMREAD_REDUCED_COLOR_8)

print(sys.getsizeof(img2))
cv2.imwrite('images/out.jpg', img2) # , [cv2.IMWRITE_JPEG_PROGRESSIVE])

netc, classc, colorc = darknet.load_network("yolov4_lpv.cfg", "lp_vehicles.data", "yolov4_lpv_last.weights")

img_for_detect = darknet.make_image(416, 416, 3)

darknet.copy_image_from_bytes(img_for_detect, img2.tobytes())

r = darknet.detect_image(netc, classc, img_for_detect)

print(r)