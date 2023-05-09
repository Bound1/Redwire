from pydantic import BaseModel


class InputVariation(BaseModel):
    prompt: str
    strength: float
    num_inference_steps: int
    guidance_scale: float
    negative_prompt: str
    num_images_per_prompt: int
