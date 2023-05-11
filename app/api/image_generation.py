from PIL import Image
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from models.stable_text_to_image import TextToImageGenerator
from models.input_text_to_image import InputText
from models.stable_image_to_image import ImageToImageGenerator
from models.input_image_to_image import InputImage
from models.stable_image_variation import ImageVariationGenerator
from models.input_image_variation import InputVariation
from fastapi.responses import StreamingResponse


router = APIRouter()
text_to_image_generator = TextToImageGenerator()
image_to_image_generator = ImageToImageGenerator()
image_variation_generator = ImageVariationGenerator()


@router.post("/text_to_image/")
async def text_to_image(input: InputText):
    params = {
        "prompt": input.prompt,
        "height": input.height,
        "width": input.width,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
    }
    # Unpack the dictionary into separate variables
    prompt, height, width, num_inference, guidance_scale, negative_prompt = params.values()

    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        image_path = f"generated_images/{prompt}.png"
        text_to_image_generator.generate_image(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                                               save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/text_to_image_grid/")
async def text_to_image_grid(input: InputText):
    params = {
        "prompt": input.prompt,
        "height": input.height,
        "width": input.width,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images": input.num_images
    }
    # Unpack the dictionary into separate variables
    prompt, height, width, num_inference, guidance_scale, negative_prompt, num_images = params.values()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        image_path = f"generated_images/{prompt}.png"
        text_to_image_generator.generate_image_grid(prompt, height, width, num_inference, guidance_scale,
                                                    negative_prompt, num_images, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image_to_image/")
async def image_to_image(input: InputImage):
    params = {
        "prompt": input.prompt,
        "strength": input.strength,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images": input.num_images
    }
    # Unpack the dictionary into separate variables
    prompt, strength, num_inference, guidance_scale, negative_prompt, num_images = params.values()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        img_name = "13-256x256"
        init_img_path = f"input_images/{img_name}.jpg"
        init_img = Image.open(init_img_path).convert("RGB")
        image_path = f"generated_images/{prompt}.png"
        image_to_image_generator.generate_image(prompt, init_img, strength, num_inference, guidance_scale,
                                                negative_prompt, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image_to_image_grid/")
async def image_to_image_grid(input: InputImage):
    params = {
        "prompt": input.prompt,
        "strength": input.strength,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images": input.num_images
    }
    # Unpack the dictionary into separate variables
    prompt, strength, num_inference, guidance_scale, negative_prompt, num_images = params.values()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        img_name = "13-256x256"
        init_img_path = f"input_images/{img_name}.jpg"
        init_img = Image.open(init_img_path).convert("RGB")
        image_path = f"generated_images/{prompt}.png"
        image_to_image_generator.generate_image_grid(prompt, init_img, strength, num_inference, guidance_scale,
                                                     negative_prompt, num_images, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/image_variation/")
async def image_variation(input: InputVariation):
    params = {
        "prompt": input.prompt,
        "strength": input.strength,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images": input.num_images
    }
    # Unpack the dictionary into separate variables
    prompt, strength, num_inference, guidance_scale, negative_prompt, num_images = params.values()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        img_name = "13-256x256"
        init_img_path = f"input_images/{img_name}.jpg"
        init_img = Image.open(init_img_path).convert("RGB")
        image_path = f"generated_images/{prompt}.png"
        image_variation_generator.generate_image(prompt, init_img, strength, num_inference, guidance_scale,
                                                negative_prompt, save_path=image_path)
        return FileResponse(image_path, media_type="image/png")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
