import os
import torch
from diffusers import StableDiffusionPipeline
from utils import image_grid


class ImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, prompt, save_path=None):
        with torch.no_grad():
            image = self.pipe(prompt, guidance_scale=7.5).images[0]
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image.save(save_path)
        return image

    def generate_image_grid(self, prompt, num_images=3, save_path=None):
        with torch.no_grad():
            prompts = [prompt] * num_images
            images = self.pipe(prompts, guidance_scale=7.5).images
            grid = image_grid(images, rows=1, cols=num_images)
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            grid.save(save_path)
        return grid


