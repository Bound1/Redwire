from pydantic import BaseModel


class InputText(BaseModel):
    prompt: str
    height: int
    width: int
    num_inference: int
    guidance_scale: float
    negative_prompt: str
    num_images: int

