import spandrel
import torch
import cv2
import numpy as np


torch_device = "cuda" if torch.cuda.is_available() else "cpu"


class ModelBurst:
    model: spandrel.ImageModelDescriptor

    def __init__(self, model: spandrel.ImageModelDescriptor) -> None:
        self.model = model

    def __image_to_tensor(self, img: np.ndarray) -> torch.Tensor:
        img = img.astype(np.float32) / 255.0
        if img.ndim == 2:
            img = np.expand_dims(img, axis=2)
        if img.shape[2] == 1:
            pass
        else:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.transpose(img, (2, 0, 1))
        tensor = torch.from_numpy(img)
        return tensor.unsqueeze(0)

    def __tensor_to_image(self, tensor: torch.Tensor) -> np.ndarray:
        image = tensor.cpu().to(torch.float).squeeze().numpy()
        image = np.transpose(image, (1, 2, 0))
        image = np.clip((image * 255.0).round(), 0, 255)
        image = image.astype(np.uint8)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    @torch.no_grad()
    @torch.inference_mode()
    def upscale(self, img: np.ndarray) -> np.ndarray:
        tensor = self.__image_to_tensor(img).to(torch_device).to(self.model.dtype)

        return self.__tensor_to_image(self.model(tensor))
