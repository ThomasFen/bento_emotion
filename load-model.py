## LOADS THE EMOTION MODEL

# import onnx, os, bentoml

# modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento', 'emotion.onnx')

# onnx_model = onnx.load(modelPath)

# bentoml.onnx.save_model("emotion", onnx_model)

## LOADS THE BLAZEFACE MODEL

# import torch, bentoml, os
# from blazeface import BlazeFace

# modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento', 'blazefaceback.pth')


# torch_model_back = BlazeFace(back_model=True)
# torch_model_back.load_weights(modelPath)

# bentoml.pytorch.save_model( "blazeface_back", torch_model_back)


## LOADS THE Blazeface ONNX model (useless for now because only 1 output supported by bentoml)

# import onnx, os, bentoml

# modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento', 'blazeface_back_converted.onnx')

# onnx_model = onnx.load(modelPath)

# bentoml.onnx.save_model("blazeface_back_onnx", onnx_model)