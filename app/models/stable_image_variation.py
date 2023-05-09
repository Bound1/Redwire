import os
import torch
from diffusers import StableDiffusionImageVariationPipeline
from PIL import Image
from torch.distributions import transforms

class ImageVariationGenerator:
    def __init__(self, model_id="lambdalabs/sd-image-variations-diffusers", revision="v2.0", device="cpu"):
        self.device = torch.device(device)
        self.pipe = StableDiffusionImageVariationPipeline.from_pretrained(model_id, revision=revision)
        self.pipe = self.pipe.to(self.device)

        def dummy(images, **kwargs):
            return images, False

        self.pipe.safety_checker = dummy

    def generate_image(self, image, height:int, width:int, num_inference_steps, guidance_scale, num_images_per_prompt):
        with torch.no_grad():
            images = self.pipe(image, height, width, num_inference_steps, guidance_scale,
                               num_images_per_prompt).images
        return images
