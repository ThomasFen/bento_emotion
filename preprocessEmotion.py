import bentoml
import numpy as np
import cv2

class preprocessEmotionRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = False

    def process_cropped_image(self, img):
        # A grayscale image is required.
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Width and height have to be 224.
        img = cv2.resize(img, (224,224), interpolation = cv2.INTER_AREA)
        img = np.asarray(img, dtype=np.float32)
        # Normalize
        img=img/255
        # Input dimensions wll be (<Nr. of faces>,224,224,1)
        img = np.expand_dims(img, axis=-1)

        return img

    @bentoml.Runnable.method(batchable=False)
    def is_positive(self,  scriptOutput, pilImage):
        boxes = []
        wholePadding = max(pilImage.width, pilImage.height) - min(pilImage.width, pilImage.height)
        sidePadding = wholePadding / 2
        isWide = pilImage.width == max(pilImage.width, pilImage.height)

        '''
        Iterate boxes 
        '''
        for box in scriptOutput:
            '''
            Remove zero-confidence detections 
            '''
            if box[-1] == 0.0:
                continue
            '''
            Descale bounding box coordinates back to original image size
            ''' 
            if isWide:
                y1 = (pilImage.height + wholePadding) * box[0] - sidePadding
                y2 = (pilImage.height + wholePadding) * box[2] - sidePadding
                x1 = pilImage.width * box[1]
                x2 = pilImage.width * box[3]

            else:
                x1 = (pilImage.height + wholePadding) * box[1] - sidePadding
                x2 = (pilImage.height + wholePadding) * box[3] - sidePadding
                y1 = pilImage.height * box[0]
                y2 = pilImage.height * box[2]   

            rescaledBox = (x1, y1, x2, y2)
            boxes.append(rescaledBox)
        """ Extract the faces from the frame and convert them to the input format required for the emotion model."""
        faces =  []
        for box in boxes:
            face = pilImage.crop(box)
            face = np.asarray(face)
            face_np = self.process_cropped_image(face)
            faces.append(face_np)

        return np.asarray(faces)