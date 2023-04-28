import base64
import io
from PIL import Image
from app.models.stable_text_to_image import TextToImageGenerator


def generate_text_to_image(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                           num_images_per_prompt):
    text_to_image_generator = TextToImageGenerator()
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    try:
        output_images = []
        images = text_to_image_generator.generate_image(prompt, height, width, num_inference, guidance_scale,
                                                        negative_prompt, num_images_per_prompt)
        output_images.extend(images)
        return output_images
    except Exception as e:
        raise ValueError(str(e))


def generate_image_to_image(prompt, input_image, strength, num_inference_steps, guidance_scale, negative_prompt,
                            num_images_per_prompt):
    from app.models.stable_image_to_image import ImageToImageGenerator
    image_to_image_generator = ImageToImageGenerator()
    if not prompt:
        raise ValueError("Prompt cannot be empty")
    try:
        output_images = []
        input_image_pil = Image.fromarray(input_image, 'RGB')
        images = image_to_image_generator.generate_image(prompt, input_image_pil, strength, num_inference_steps,
                                                         guidance_scale, negative_prompt, num_images_per_prompt)
        output_images.extend(images)
        return output_images
    except Exception as e:
        raise ValueError(str(e))


def plaintext_to_html(text: str) -> str:
    return f"<p style='font-family: monospace;'>{text}</p>"

def image_from_url_text(filedata):
    if filedata is None:
        return None

    if type(filedata) == list and len(filedata) > 0 and type(filedata[0]) == dict and filedata[0].get("is_file", False):
        filedata = filedata[0]

    if type(filedata) == dict and filedata.get("is_file", False):
        filename = filedata["name"]
        return Image.open(filename)

    if type(filedata) == list:
        if len(filedata) == 0:
            return None

        filedata = filedata[0]

    if filedata.startswith("data:image/png;base64,"):
        filedata = filedata[len("data:image/png;base64,"):]

    filedata = base64.decodebytes(filedata.encode('utf-8'))
    image = Image.open(io.BytesIO(filedata))
    return image




