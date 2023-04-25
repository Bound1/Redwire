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
