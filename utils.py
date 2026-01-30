import cv2
from model_utils import load_model, UpscaleInfo, ModelBurst, ModelTile
import spandrel
from collections import namedtuple
import os.path
import requests
import tqdm
import json
import pathlib
import customtkinter as ctk

UpscalerInfo = namedtuple(
    "UpscalerInfo", ["download_path", "supported_scaling", "filetype"]
)

upscaler_infos: dict[str, UpscalerInfo] = {}


def get_upscaler_names() -> list[str]:
    set_upscaler_infos()
    return [*upscaler_infos.keys()]


def set_upscaler_infos() -> None:
    if len(upscaler_infos) != 0:
        return

    with open("model_infos.json") as file:
        json_obj = json.load(file)

    models = json_obj["models"]

    for model in models:
        url = str(model["download_url"])
        scale = int(model["supported_scale"])

        infos = url.split("/")[-1].split(".")
        model_name = infos[0]
        extension = infos[1]

        upscaler_infos[model_name] = UpscalerInfo(url, scale, extension)


def check_and_install_model(model_name: str) -> None:
    set_upscaler_infos()
    info = upscaler_infos[model_name]

    output_path = os.path.join("models", f"{model_name}.{info.filetype}")

    if os.path.exists(output_path):
        print(f"{output_path} exists, continue ...")
        return

    print(f"Downloading {model_name} to models folder")

    rsp = requests.get(info.download_path, stream=True)
    file_size = int(rsp.headers.get("content-length", 0))

    with (
        open(output_path, "wb") as file,
        tqdm.tqdm(
            desc=model_name,
            total=file_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar,
    ):
        for data in rsp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def upscale_image(info: UpscaleInfo) -> tuple[str, bool]:
    model_info = upscaler_infos[info.model_path]

    info.model_path = f"{os.path.join('models', info.model_path)}.{model_info.filetype}"

    model, error, is_success = load_model(info, model_info.supported_scaling)

    if not is_success or model is None:
        return (error, is_success)

    input_image = cv2.imread(info.input_path, cv2.IMREAD_COLOR)

    if input_image is None:
        return (f"Cannot read {info.input_path} image", False)

    if model.tiling == spandrel.ModelTiling.SUPPORTED:
        upscaler = ModelTile(model, model_info.supported_scaling)
    else:
        upscaler = ModelBurst(model)

    output_image = upscaler.upscale(input_image)

    cv2.imwrite(info.output_path, output_image)

    return ("", True)


def upscale_images(input_folder: str, info: UpscaleInfo, label: ctk.CTkLabel) -> None:
    path = pathlib.Path(input_folder)
    files: list[pathlib.Path] = []

    files.extend(path.glob("*.jpeg"))
    files.extend(path.glob("*.jpg"))
    files.extend(path.glob("*.png"))
    files.extend(path.glob("*.webp"))

    total_files = len(files)

    bar = tqdm.tqdm(total=total_files, desc="Upscaling Images")
    for index, file in enumerate(files):
        label.configure(text=f"Upscaling {index} / {total_files}")

        info.input_path = str(file.absolute().resolve())
        info.output_path = os.path.join(info.output_path, file.name)
        ret_val = upscale_image(info)

        if not ret_val[1]:
            print(ret_val[0])

        bar.update()
    bar.close()
