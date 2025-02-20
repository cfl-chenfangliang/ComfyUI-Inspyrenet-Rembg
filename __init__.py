from .Inspyrenet_Rembg import InspyrenetRembg, InspyrenetRembgAdvanced

NODE_CLASS_MAPPINGS = {
    "InspyrenetRembgOpt" : InspyrenetRembg,
    "InspyrenetRembgAdvancedOpt" : InspyrenetRembgAdvanced,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "InspyrenetRembgOpt": "Inspyrenet Rembg Opt",
    "InspyrenetRembgAdvancedOpt": "Inspyrenet Rembg Advanced Opt"
}
__all__ = ['NODE_CLASS_MAPPINGS', "NODE_DISPLAY_NAME_MAPPINGS"]
