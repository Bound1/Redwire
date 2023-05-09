import os
import torch
from diffusers import StableDiffusionImg2ImgPipeline


class ImageToImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionImg2ImgPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        self.pipe = self.pipe.to(self.device)

        def dummy(images, **kwargs):
            return images, False

        self.pipe.safety_checker = dummy

    def generate_image(self, prompt, image, strength, num_inference_steps, guidance_scale,
                       negative_prompt, num_images_per_prompt):
        with torch.no_grad():
            images = self.pipe(prompt, image, strength, num_inference_steps, guidance_scale, negative_prompt,
                               num_images_per_prompt).images
        return images
