import bentoml
from bentoml.io import NumpyNdarray
from bentoml.io import Image
from bentoml.io import JSON
from bentoml.io import NumpyNdarray
from bentoml.io import Multipart
from typing import TYPE_CHECKING
from typing import Any
from time import time
from datetime import datetime, timezone
from preprocessBlazeface import preprocessBlazefaceRunnable
from postprocessBlazeface import postprocessBlazefaceRunnable
from preprocessEmotion import preprocessEmotionRunnable
from numpy.typing import NDArray
if TYPE_CHECKING:
    from PIL.Image import Image

preprocess_blazeface_runner = bentoml.Runner(preprocessBlazefaceRunnable, name="preprocess_blazeface")
blazeface_runner = bentoml.pytorch.get("blazeface_back:latest").to_runner()
postprocess_blazeface_runner = bentoml.Runner(postprocessBlazefaceRunnable, name="postprocess_blazeface")
preprocess_emotion_runner = bentoml.Runner(preprocessEmotionRunnable, name="preprocess_emotion")
emotion_runner = bentoml.onnx.get("emotion:latest").to_runner()

svc = bentoml.Service("emotion_recognition", runners=[preprocess_blazeface_runner, blazeface_runner, postprocess_blazeface_runner, preprocess_emotion_runner, emotion_runner])

input_spec = Multipart(image=Image(), annotations=JSON())

# Create new API and add it to "svc"
@svc.api(input=input_spec, output=JSON())  # define IO spec
async def predict_async(image: Image, annotations: "dict[str, Any]"):
    """ Prepare the image for Blazeface. """
    imageSize = 256 # Front model would be 128 in size.
    blazeface_input = await preprocess_blazeface_runner.async_run(image, imageSize)

    """ Run the Blazeface back model. """
    blazeface_model_result = await blazeface_runner.async_run(blazeface_input) 

    """ Postprocess the raw predictions and use Non-maximum suppression to remove overlapping detection. """
    blazeface_script_result = await postprocess_blazeface_runner.async_run(blazeface_model_result)
    if len(blazeface_script_result[0]) == 0:   # Stop when no faces in photo exist.
        return dict(annotations, emotions=[], boxes=[])

    """ Get the face(s) of the image with help of the bounding boxes. """
    emotion_input = await preprocess_emotion_runner.async_run(blazeface_script_result[0], image)
    
    """ Run the emotion model. """
    emotion_result = await emotion_runner.async_run(emotion_input)

    """ Result time stamp """
    date = datetime.now(timezone.utc).isoformat(timespec='milliseconds')
    
    """ Format output. """
    emotions_per_face_dicts = []
    emotion_result = emotion_result.tolist()
    for faceIndx, emotions in enumerate(emotion_result):
            emotions_per_face_dicts.append({'raw':{}, 'dominantEmotion':{}})
            # Find name of most likely emotion.
            dominant = index_to_emotion(emotions.index(max(emotions)))
            # Add the name for the emotion that was determined to be predominant.
            emotions_per_face_dicts[faceIndx]['dominantEmotion'] = dominant 
            # Add box coordinates.
            emotions_per_face_dicts[faceIndx]['box'] = blazeface_script_result[0][faceIndx]
            # Add the numeric value of every emotion type. They lie between 0 and 1.
            for i, emotion in enumerate(emotions):
                emotion_type = index_to_emotion(i)
                emotions_per_face_dicts[faceIndx]['raw'][emotion_type] = {"date": date, "value": emotion}

    return  dict(annotations, emotions=emotions_per_face_dicts)


def index_to_emotion(index):
    emotions =  {0:
                'neutral',
                1:
                'happy',
                2:
                'sad',
                3:
                'surprise',
                4:
                'fear',
                5:
                'disgust',
                6:
                'anger',
                7:
             'contempt'    }

    return emotions[index]