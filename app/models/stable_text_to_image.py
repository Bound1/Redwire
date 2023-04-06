import os
import torch
from diffusers import StableDiffusionPipeline
from utils import image_grid


class TextToImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id)
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, prompt, height, width, num_inference, guidance_scale, negative_prompt
                       , save_path):
        with torch.no_grad():
            image = self.pipe(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                              ).images[0]
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image.save(save_path)
        return image

    def generate_image_grid(self, prompt, height, width, num_inference, guidance_scale, negative_prompt,
                            num_images, save_path):
        with torch.no_grad():
            prompts = [prompt] * num_images
            negative_prompt = [negative_prompt] * num_images
            images = self.pipe(prompts, height, width, num_inference, guidance_scale, negative_prompt).images
            grid = image_grid(images, rows=1, cols=num_images)
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            grid.save(save_path)
        return grid
