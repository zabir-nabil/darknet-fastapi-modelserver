# list of models to be loaded in runtime
# provide the path for cfg, data, and weights file

models = {
    0: {
        "cfg": "yolov4_lpv.cfg",
        "data": "lp_vehicles.data",
        "weights": "yolov4_lpv_last.weights"
    },

    1: {
        "cfg": "yolov3-tiny_lp.cfg",
        "data": "lp.data",
        "weights": "yolov3-tiny_lp_800000.weights"
    }
}