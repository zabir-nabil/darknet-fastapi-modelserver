import requests
import cv2
import numpy as np
import sys

import cProfile, pstats, io
from pstats import SortKey

import time

# pr = cProfile.Profile()
# pr.enable()

# actual code for profiling

t1 = time.process_time()
img = cv2.resize(cv2.imread('images/frame4.jpg'), (416,416))
print(sys.getsizeof(img))
img_encoded = cv2.imencode('.jpg', img)[1]
print(sys.getsizeof(img_encoded))

img_bytes = img_encoded.tobytes()  # bytes class

print(sys.getsizeof(img_bytes))

# hex string
img_hex = img_bytes.hex()
print(type(img_hex))
print(sys.getsizeof(img_hex))

r = requests.post('http://127.0.0.1:8000/predict/', json={"img": img_hex, "dim": (416,416,3), "model_id" : 0, "save_predictions_on_server": True})

t2 = time.process_time()

# pr.disable()
# s = io.StringIO()
# sortby = SortKey.CUMULATIVE
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())
print(t2-t1)
print(r.content)