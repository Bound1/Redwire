from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.models.image_generator import ImageGenerator
from app.models.prompt_input import PromptInput

router = APIRouter()
image_generator = ImageGenerator()


@router.post("/generate_image/")
async def generate_image(input: PromptInput):
    prompt = input.prompt
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        image_path = f"generated_images/{prompt}.png"
        image_generator.generate_image(prompt, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate_image_grid/")
async def generate_image_grid(input: PromptInput):
    prompt = input.prompt
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        image_path = f"generated_images/{prompt}.png"
        image_generator.generate_image_grid(prompt, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


