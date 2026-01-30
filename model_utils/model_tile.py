import torch.nn.functional as F
import math
import spandrel
import torch
import numpy as np
import cv2
import tqdm

torch_device = "cuda" if torch.cuda.is_available() else "cpu"

"""
    The tiling code is taken from realesrgan github
    https://github.com/xinntao/Real-ESRGAN/blob/master/realesrgan/utils.py
"""


class ModelTile:
    scale: int
    tile_size: int
    tile_pad: int
    pre_pad: int
    model: spandrel.ImageModelDescriptor
    img: torch.Tensor
    output: torch.Tensor
    mod_scale: int

    def __init__(self, model: spandrel.ImageModelDescriptor, scale: int = 2) -> None:
        self.scale = scale
        self.tile_size = 192
        self.tile_pad = 10
        self.pre_pad = 0
        self.mod_scale = scale

        self.model = model

    def __preprocess(self, img: np.ndarray) -> None:
        img_tensor = torch.from_numpy(np.transpose(img, (2, 0, 1))).to(self.model.dtype)
        self.img = img_tensor.unsqueeze(0).to(torch_device)

        if self.pre_pad != 0:
            self.img = F.pad(self.img, (0, self.pre_pad, 0, self.pre_pad), "reflect")

        if self.scale == 2:
            self.mod_scale = 2
        elif self.scale == 1:
            self.mod_scale = 4

        if self.mod_scale is not None:
            self.mod_pad_h, self.mod_pad_w = 0, 0
            _, _, h, w = self.img.size()

            if h % self.mod_scale != 0:
                self.mod_pad_h = self.mod_scale - h % self.mod_scale

            if w % self.mod_scale != 0:
                self.mod_pad_w = self.mod_scale - w % self.mod_scale

            self.img = F.pad(
                self.img, (0, self.mod_pad_w, 0, self.mod_pad_h), "reflect"
            )

    def __tile_process(self):
        batch, channel, height, width = self.img.shape

        output_height = height * self.scale
        output_width = width * self.scale
        output_shape = (batch, channel, output_height, output_width)

        self.output = self.img.new_zeros(output_shape)
        tiles_x = math.ceil(width / self.tile_size)
        tiles_y = math.ceil(height / self.tile_size)

        tqdm_bar = tqdm.tqdm(total=tiles_y * tiles_x, desc="Processing Tiles")
        for y in range(tiles_y):
            for x in range(tiles_x):
                ofs_x = x * self.tile_size
                ofs_y = y * self.tile_size

                input_start_x = ofs_x
                input_end_x = min(ofs_x + self.tile_size, width)

                input_start_y = ofs_y
                input_end_y = min(ofs_y + self.tile_size, height)

                # input tile area on total image with padding
                input_start_x_pad = max(input_start_x - self.tile_pad, 0)
                input_end_x_pad = min(input_end_x + self.tile_pad, width)
                input_start_y_pad = max(input_start_y - self.tile_pad, 0)
                input_end_y_pad = min(input_end_y + self.tile_pad, height)

                # input tile dimensions
                input_tile_width = input_end_x - input_start_x
                input_tile_height = input_end_y - input_start_y
                input_tile = self.img[
                    :,
                    :,
                    input_start_y_pad:input_end_y_pad,
                    input_start_x_pad:input_end_x_pad,
                ]

                # upscale tile
                try:
                    with torch.no_grad():
                        output_tile = self.model(input_tile)
                except RuntimeError as error:
                    print("Error", error)

                # output tile area on total image
                output_start_x = input_start_x * self.scale
                output_end_x = input_end_x * self.scale
                output_start_y = input_start_y * self.scale
                output_end_y = input_end_y * self.scale

                # output tile area without padding
                output_start_x_tile = (input_start_x - input_start_x_pad) * self.scale
                output_end_x_tile = output_start_x_tile + input_tile_width * self.scale
                output_start_y_tile = (input_start_y - input_start_y_pad) * self.scale
                output_end_y_tile = output_start_y_tile + input_tile_height * self.scale

                # put tile into output image
                self.output[
                    :, :, output_start_y:output_end_y, output_start_x:output_end_x
                ] = output_tile[
                    :,
                    :,
                    output_start_y_tile:output_end_y_tile,
                    output_start_x_tile:output_end_x_tile,
                ]
                tqdm_bar.update(1)
        tqdm_bar.close()

    def __postprocess(self) -> torch.Tensor:
        if self.mod_scale is not None:
            _, _, h, w = self.output.size()
            self.output = self.output[
                :,
                :,
                0 : h - self.mod_pad_h * self.scale,
                0 : w - self.mod_pad_w * self.scale,
            ]
        # remove prepad
        if self.pre_pad != 0:
            _, _, h, w = self.output.size()
            self.output = self.output[
                :,
                :,
                0 : h - self.pre_pad * self.scale,
                0 : w - self.pre_pad * self.scale,
            ]
        return self.output

    @torch.no_grad()
    @torch.inference_mode()
    def upscale(self, img: np.ndarray) -> np.ndarray:
        # h_input, w_input = img.shape[0:2]
        # img: numpy
        img = img.astype(np.float32)
        if np.max(img) > 256:  # 16-bit image
            max_range = 65535
        else:
            max_range = 255
        img = img / max_range
        if len(img.shape) == 2:  # gray image
            img_mode = "L"
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4:  # RGBA image with alpha channel
            img_mode = "RGBA"
            alpha = img[:, :, 3]
            img = img[:, :, 0:3]
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        else:
            img_mode = "RGB"
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # ------------------- process image (without the alpha channel) ------------------- #
        self.__preprocess(img)
        self.__tile_process()
        output_img = self.__postprocess()
        output_img = output_img.data.squeeze().float().cpu().clamp_(0, 1).numpy()
        output_img = np.transpose(output_img[[2, 1, 0], :, :], (1, 2, 0))
        if img_mode == "L":
            output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2GRAY)

        # ------------------- process the alpha channel if necessary ------------------- #
        if img_mode == "RGBA":
            h, w = alpha.shape[0:2]
            output_alpha = cv2.resize(
                alpha,
                (w * self.scale, h * self.scale),
                interpolation=cv2.INTER_LINEAR,
            )

            # merge the alpha channel
            output_img = cv2.cvtColor(output_img, cv2.COLOR_BGR2BGRA)
            output_img[:, :, 3] = output_alpha

        # ------------------------------ return ------------------------------ #
        if max_range == 65535:  # 16-bit image
            output = (output_img * 65535.0).round().astype(np.uint16)
        else:
            output = (output_img * 255.0).round().astype(np.uint8)

        """
        if outscale is not None and outscale != float(self.scale):
            output = cv2.resize(
                output,
                (
                    int(w_input * outscale),
                    int(h_input * outscale),
                ),
                interpolation=cv2.INTER_LANCZOS4,
            )
        """

        return output
