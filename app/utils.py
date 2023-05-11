import base64
import io
import os
import uuid
import gradio as gr
from PIL import Image
from app.models.stable_text_to_image import TextToImageGenerator
from app.models.stable_image_to_image import ImageToImageGenerator
from app.models.stable_image_variation import ImageVariationGenerator


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


def generate_image_variation(input_image, num_inference_steps, guidance_scale,
                             num_images_per_prompt):
    image_variation_generator = ImageVariationGenerator()
    try:
        output_images = []
        input_image_pil = Image.fromarray(input_image, 'RGB')
        images = image_variation_generator.generate_image(input_image_pil, input_image_pil.height, input_image_pil.width, num_inference_steps,
                                                          guidance_scale, num_images_per_prompt)
        output_images.extend(images)
        return output_images
    except Exception as e:
        raise ValueError(str(e))


def save_image_gallery(gallery_value):
    path = "output"  # Change this to the desired output directory
    os.makedirs(path, exist_ok=True)

    filenames = []
    fullfns = []

    for image_index, filedata in enumerate(gallery_value):
        print(filedata)
        image = image_from_url_text(filedata)

        # Create a unique UUID-based filename
        filename = f"image_{image_index}_{uuid.uuid4()}.png"
        fullfn = os.path.join(path, filename)
        image.save(fullfn)

        filenames.append(filename)
        fullfns.append(fullfn)
    return gr.File.update(value=fullfns, visible=True)


def send_gradio_gallery_to_image(x):
    if len(x) == 0:
        return None
    return image_from_url_text(x[0])


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


def send_selected_image_to_image2image(selected_image):
    data_url = selected_image['data']
    file_path = data_url.split('=')[1]
    im = Image.open(file_path)
    return gr.Image.update(value=im)
