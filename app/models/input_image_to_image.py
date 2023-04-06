import PIL.Image
from pydantic import BaseModel


class InputImage(BaseModel):
    prompt: str
    strength: float
    num_inference: int
    guidance_scale: float
    negative_prompt: str
    num_images_per_prompt: int
    num_images: int
