import uuid
from PIL import Image
from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile
from app.models.stable_text_to_image import TextToImageGenerator
from app.models.input_text_to_image import InputText
from app.models.stable_image_to_image import ImageToImageGenerator
from app.models.input_image_to_image import InputImage
from app.utils import generate_text_to_image, generate_image_to_image

router = APIRouter()
text_to_image_generator = TextToImageGenerator()
image_to_image_generator = ImageToImageGenerator()


@router.post("/text_to_image/")
async def text_to_image(input: InputText):
    params = {
        "prompt": input.prompt,
        "height": input.height,
        "width": input.width,
        "num_inference": input.num_inference,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images_per_prompt": input.num_images_per_prompt
    }
    prompt, height, width, num_inference, guidance_scale, negative_prompt, num_images_per_prompt = params.values()

    try:
        output_images = generate_text_to_image(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                                               num_images_per_prompt)

        image_urls = []
        for i, img in enumerate(output_images):
            output_image_path = f"generated_images/{str(uuid.uuid4())}_{i}.png"
            img.save(output_image_path, "PNG")
            image_url = f"generated_images/{str(uuid.uuid4())}_{i}.png"  # Replace with the correct URL
            image_urls.append(image_url)

        return {"images": image_urls}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/image_to_image/")
async def image_to_image(input: InputImage, image_file: UploadFile = File(...)):
    params = {
        "prompt": input.prompt,
        "strength": input.strength,
        "num_inference_steps": input.num_inference_steps,
        "guidance_scale": input.guidance_scale,
        "negative_prompt": input.negative_prompt,
        "num_images_per_prompt": input.num_images_per_prompt
    }
    prompt, strength, num_inference_steps, guidance_scale, negative_prompt, num_images_per_prompt = params.values()

    # Read the uploaded image and convert it to a PIL Image
    input_image = Image.open(image_file.file)

    try:
        output_images = generate_image_to_image(prompt, input_image, strength, num_inference_steps, guidance_scale,
                                                negative_prompt, num_images_per_prompt)

        image_urls = []
        for i, img in enumerate(output_images):
            output_image_path = f"generated_images/{str(uuid.uuid4())}_{i}.png"
            img.save(output_image_path, "PNG")
            image_url = f"generated_images/{str(uuid.uuid4())}_{i}.png"  # Replace with the correct URL
            image_urls.append(image_url)

        return {"images": image_urls}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))