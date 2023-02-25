import onnx, os, bentoml, torch
from blazeface import BlazeFace

## LOADS THE EMOTION MODEL 

modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento_emotion', 'emotion.onnx')

onnx_model = onnx.load(modelPath)

bentoml.onnx.save_model("emotion", onnx_model, signatures={   # model signatures for runner inference
                                "run": {
                                "batchable": True,
                                    }
                            }
                         )

## LOADS THE BLAZEFACE MODEL

modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento_emotion', 'blazefaceback.pth')
torch_model_back = BlazeFace(back_model=True)
torch_model_back.load_weights(modelPath)

bentoml.pytorch.save_model( "blazeface_back",
                            torch_model_back, 
                            signatures={   # model signatures for runner inference
                                "__call__": {
                                "batchable": True,
                                    }
                            }
)


# ## LOADS THE Blazeface ONNX model (useless for now because only 1 output supported by bentoml)

# modelPath = os.path.join(os.path.expanduser('~'), 'dev', 'bento_emotion', 'blazeface_back_converted.onnx')

# onnx_model = onnx.load(modelPath)

# bentoml.onnx.save_model("blazeface_back_onnx", onnx_model)