import bentoml
import numpy as np
import cv2
import torch

class preprocessBlazefaceRunnable(bentoml.Runnable):
    SUPPORTED_RESOURCES = ("cpu",)
    SUPPORTS_CPU_MULTI_THREADING = False

    @bentoml.Runnable.method(batchable=False)
    def processImage(self, pilImage, height):
        """ 
        Resize a rectangular image to a padded square (letterbox)
        """ 
        img = pilImage.convert('RGB')
        img = np.array(pilImage)

        """ 
        Remove transparency layer if existent
        """
        if(img.shape[2] == 4):
            img = img[:,:,:3]

        color = (127.5, 127.5, 127.5)
        shape = img.shape[:2]

        ratio = float(height) / max(shape)
        newShape = (int(round(shape[1] * ratio)), int(round(shape[0] * ratio)))

        dw = (height - newShape[0]) / 2
        dh = (height - newShape[1]) / 2
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

        img = cv2.resize(img, newShape, interpolation=cv2.INTER_LINEAR)
        img = cv2.copyMakeBorder(img, top, bottom, left,
                                right, cv2.BORDER_CONSTANT, value=color)
        img = np.asarray(img, dtype=np.float32)

        img = torch.from_numpy(img).permute((2, 0, 1))
        img = img.unsqueeze(0)
        # TODO add device support: img = img.to(device) 
        img = img.float() / 127.5 - 1.0
        return img
