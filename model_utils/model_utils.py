import torch
import dataclasses
import spandrel


@dataclasses.dataclass
class UpscaleInfo:
    model_path: str
    input_path: str
    output_path: str
    data_type: str


def get_torch_device() -> str:
    return "cuda" if torch.cuda.is_available() else "cpu"


def set_model_dtype(
    model: spandrel.ImageModelDescriptor, data_type: str
) -> spandrel.ImageModelDescriptor:
    torch_dev = get_torch_device()

    if torch_dev == "cpu":
        model.float().cpu()
        return model

    is_bf16 = (
        torch.cuda.is_bf16_supported()
        and model.supports_bfloat16
        and data_type == "bfloat16"
    )

    is_fp16 = (
        torch.cuda.is_bf16_supported()
        and model.supports_bfloat16
        and data_type == "float16"
    )

    if is_bf16:
        model.bfloat16()
    elif is_fp16:
        model.half()
    else:
        model.float()

    model.cuda()

    return model


def load_model(
    info: UpscaleInfo, supported_scale: int
) -> tuple[spandrel.ImageModelDescriptor | None, str, bool]:
    try:
        model = spandrel.ModelLoader().load_from_file(info.model_path)
    except ValueError:
        extension = info.model_path.split(".")[1]
        return (None, f"{extension} is not supported", False)
    except spandrel.UnsupportedModelError:
        return (None, f"{info.model_path} architecture is not supported", False)

    assert isinstance(model, spandrel.ImageModelDescriptor)

    model.scale = supported_scale
    model = set_model_dtype(model, info.data_type)

    try:
        torch.compile(model, fullgraph=True, mode="default")
    except:
        torch.compile(model)

    model.eval()

    return (model, "", True)
