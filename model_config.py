# list of models to be loaded in runtime
# provide the path for cfg, data, and weights file

models = {
    0: {
        "cfg": "model_data/yolov4_lpv.cfg",
        "data": "model_data/lp_vehicles.data",
        "weights": "model_data/yolov4_lpv_last.weights"
    },

    1: {
        "cfg": "model_data/yolov3-tiny_lp.cfg",
        "data": "model_data/lp.data",
        "weights": "model_data/yolov3-tiny_lp_800000.weights"
    }
}