from PIL import Image
import torch
import numpy as np
from transparent_background import Remover
from tqdm import tqdm
import folder_paths
import os

# set the models directory
if "transparent_background" not in folder_paths.folder_names_and_paths:
    print('111')
    current_paths = [os.path.join(folder_paths.models_dir, "transparent_background")]
else:
    current_paths, _ = folder_paths.folder_names_and_paths["transparent_background"]
print('folder_paths.models_dir:', folder_paths.models_dir)
print('current_paths:', current_paths)
folder_paths.folder_names_and_paths["transparent_background"] = (current_paths, folder_paths.supported_pt_extensions)


# Tensor to PIL
def tensor2pil(image):
    return Image.fromarray(np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8))

# Convert PIL to Tensor
def pil2tensor(image):
    return torch.from_numpy(np.array(image).astype(np.float32) / 255.0).unsqueeze(0)

class InspyrenetRembg:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "torchscript_jit": (["default", "on"],),
                "model": (folder_paths.get_filename_list("transparent_background"), {"tooltip": "The name of the transparent-background (model) to load."}),
            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "remove_background"
    CATEGORY = "image"

    def remove_background(self, image, torchscript_jit, model):
        model_path = folder_paths.get_full_path_or_raise("transparent_background", model)
        if (torchscript_jit == "default"):
            remover = Remover(ckpt=model_path)
        else:
            remover = Remover(ckpt=model_path, jit=True)
        img_list = []
        for img in tqdm(image, "Inspyrenet Rembg"):
            mid = remover.process(tensor2pil(img), type='rgba')
            out =  pil2tensor(mid)
            img_list.append(out)
        img_stack = torch.cat(img_list, dim=0)
        mask = img_stack[:, :, :, 3]
        return (img_stack, mask)
        
class InspyrenetRembgAdvanced:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "threshold": ("FLOAT", {"default": 0.5, "min": 0.0, "max": 1.0, "step": 0.01}),
                "torchscript_jit": (["default", "on"],),
                "model": (folder_paths.get_filename_list("transparent_background"), {"tooltip": "The name of the transparent-background (model) to load."}),

            },
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "remove_background"
    CATEGORY = "image"

    def remove_background(self, image, torchscript_jit, threshold, model):
        model_path = folder_paths.get_full_path_or_raise("transparent_background", model)

        if (torchscript_jit == "default"):
            remover = Remover(ckpt=model_path)
        else:
            remover = Remover(ckpt=model_path, jit=True)
        img_list = []
        for img in tqdm(image, "Inspyrenet Rembg"):
            mid = remover.process(tensor2pil(img), type='rgba', threshold=threshold)
            out =  pil2tensor(mid)
            img_list.append(out)
        img_stack = torch.cat(img_list, dim=0)
        mask = img_stack[:, :, :, 3]
        return (img_stack, mask)
