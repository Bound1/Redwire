from typing import List
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline


class TextToImageGenerator:
    def __init__(self, model_id="runwayml/stable-diffusion-v1-5", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
        self.pipe = self.pipe.to(self.device)

        def dummy(images, **kwargs):
            return images, False

        self.pipe.safety_checker = dummy

    def generate_image(self, prompt, height, width, num_inference, guidance_scale, negative_prompt,
                       num_images_per_prompt) -> List[Image.Image]:
        with torch.no_grad():
            images = self.pipe(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                               num_images_per_prompt).images
        return images


def dummy_checker(images, **kwargs): return images, False
