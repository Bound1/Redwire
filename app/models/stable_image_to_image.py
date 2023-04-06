import os
import torch
from diffusers import StableDiffusionImg2ImgPipeline
from utils import image_grid


class ImageToImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id)
        self.pipe = self.pipe.to(self.device)

    def generate_image(self, init_img, strength, prompt, num_inference, guidance_scale, negative_prompt,
                       num_images_per_prompt,
                       save_path=None):
        with torch.no_grad():
            image = init_img.convert("RGB")
            image = self.pipe(init_img, strength, prompt, num_inference, guidance_scale, negative_prompt,
                              num_images_per_prompt).images[0]
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            image.save(save_path)
        return image

    def generate_image_grid(self, init_img, strength, prompt, num_inference, guidance_scale, negative_prompt,
                            num_images,
                            save_path=None):
        with torch.no_grad():
            prompts = [prompt] * num_images
            images = self.pipe(init_img, strength, prompts, num_inference, guidance_scale, negative_prompt,
                               num_images).images
            grid = image_grid(images, rows=1, cols=num_images)
        if save_path is not None:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            grid.save(save_path)
        return grid
