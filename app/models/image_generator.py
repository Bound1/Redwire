import os

import torch
from diffusers import StableDiffusionPipeline


class ImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, prompt, save_path=None):
        with torch.no_grad():
            image = self.pipe(prompt, num_inference_steps=50).images[0]
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image.save(save_path)
        return image
