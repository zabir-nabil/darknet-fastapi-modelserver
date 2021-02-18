from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from model_config import models
import numpy as np
import cv2
import darknet


app = FastAPI()

class ModelServer():
    def __init__(self):
        self.nets = {}
        self.class_map = {}
        self.color_map = {}

        for model_id in models:
            try:
                print(model_id)
                cfg = models[model_id]['cfg']
                data = models[model_id]['data']
                weights = models[model_id]['weights']


                netc, classc, colorc = darknet.load_network(cfg, data, weights)


                self.nets[model_id] = netc
                self.class_map[model_id] = classc
                self.color_map[model_id] = colorc

            except Exception as e:
                print(e)
                print(f"Error: model {model_id} loading failed.")
    
    def predict(self, model_id, img_np, img_dim, save_predictions_on_server = False, threshold = 10.):
        if len(img_dim) == 3:
            img_for_detect = darknet.make_image(img_dim[0], img_dim[1], img_dim[2])
        elif len(img_dim) == 2:
            img_for_detect = darknet.make_image(img_dim[0], img_dim[1], 1)
        else:
            raise Exception(f"The image shape is not supported. shape = {img_dim}") 
        
        darknet.copy_image_from_bytes(img_for_detect, img_np.tobytes()) 

        try:
            r = darknet.detect_image(self.nets[model_id], self.class_map[model_id], img_for_detect)

            class_labels = []
            xc = []
            yc = []
            w = []
            h = []

            for ri in r:
                p = float(ri[1])
                if p >= threshold:
                    class_labels.append( self.class_map[model_id].index(ri[0]) )
                    xc.append( int(ri[2][0])  )
                    yc.append( int(ri[2][1])  )
                    w.append( int(ri[2][2])  )
                    h.append( int(ri[2][3])  )

            if save_predictions_on_server:
                pred = darknet.draw_boxes(r, img_np, self.color_map[model_id])
                cv2.imwrite(f"predictions/prediction_{model_id}.jpg", pred)

            
            return {"class_labels": class_labels, "xc": xc, "yc": yc, "w": w, "h": h}
        except Exception as e:
            print(e)
            print(f"Error: model {model_id} loading failed.")
            return {"class_labels": [], "xc": [], "yc": [], "w": [], "h": []}
        



app.modelserver = ModelServer()



class Image(BaseModel):
    img: bytes
    dim: tuple
    model_id: int
    save_predictions_on_server: Optional[bool] = False


@app.get("/")
def is_live():
    return {"msg": "Model server is live."}




@app.post("/predict/")
def predict(img_model: Image):
    img_bytes = bytes.fromhex(img_model.img.decode()) # hex to bytes
    nparr = np.frombuffer(img_bytes, np.byte)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED) # decoding this is mendatory, we need a tensor, not a JPEG compressed image file

    response = app.modelserver.predict(img_model.model_id, img_np, img_model.dim, img_model.save_predictions_on_server)

    return response
