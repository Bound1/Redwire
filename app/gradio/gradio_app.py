import gradio
import gradio as gr
from utils import generate_text_to_image, generate_image_to_image


def text_to_image_wrapper(prompt, num_inference, num_images_per_prompt, height, width, guidance_scale, negative_prompt):
    if height % 8 != 0 or width % 8 != 0:
        raise ValueError("Height and width must be divisible by 8.")
    image = generate_text_to_image(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                                   num_images_per_prompt)
    return image


def image_to_image_wrapper(prompt, num_images_per_prompt, num_inference_steps, image, strength, guidance_scale,
                           negative_prompt):
    if image.shape[0] % 8 != 0 or image.shape[1] % 8 != 0:
        raise ValueError("Height and width must be divisible by 8.")
    images = generate_image_to_image(prompt, image, strength, num_inference_steps, guidance_scale, negative_prompt,
                                     num_images_per_prompt)
    return images


custom_css = """
.gradio-container {
    background-color: #3b195d;
    color: #ffffff;
}
.gradio-input, .gradio-output {
    background-color: rgba(0, 0, 0, 0.1);
}
"""

text_to_image_inputs = [
    gr.inputs.Textbox(lines=2, label="Prompt"),
    gr.inputs.Slider(minimum=1, maximum=50, step=1, default=10, label="Num Inference Steps"),
    gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1, label="Num Images Per Prompt"),
    gr.inputs.Slider(minimum=1, maximum=1024, step=8, default=512, label="Height"),
    gr.inputs.Slider(minimum=1, maximum=1024, step=8, default=512, label="Width"),
    gr.inputs.Slider(minimum=0, maximum=12, step=0.5, default=7.5, label="Guidance Scale"),
    gr.inputs.Textbox(lines=2, label="Negative Prompt"),
]

# Image to Image Interface
image_to_image_inputs = [
    gr.inputs.Textbox(lines=2, label="Prompt"),
    gr.inputs.Slider(minimum=1, maximum=10, step=1, default=10, label="Num Images Per Prompt"),
    gr.inputs.Slider(minimum=1, maximum=50, step=1, default=10, label="Num Inference Steps"),
    gr.inputs.Image(shape=(512, 512), label="Input Image"),
    gr.inputs.Slider(minimum=0, maximum=1.0, step=0.1, default=1.0, label="Strength"),
    gr.inputs.Slider(minimum=0, maximum=12, step=0.5, default=7.5, label="Guidance Scale"),
    gr.inputs.Textbox(lines=2, label="Negative Prompt"),
]

text_to_image_iface = gr.Interface(fn=text_to_image_wrapper,
                                   inputs=text_to_image_inputs,
                                   outputs=gr.Gallery(),
                                   title="Text to Image Generator",
                                   description="Generate images from textual prompts using an AI model.",
                                   css=custom_css)

image_to_image_iface = gr.Interface(fn=image_to_image_wrapper,
                                    inputs=image_to_image_inputs,
                                    outputs=gr.Gallery(), title="Image to Image Generator",
                                    description="Modify images based on textual prompts using an AI model.",
                                    css=custom_css,
                                    )

demo = gr.TabbedInterface([text_to_image_iface, image_to_image_iface], ["Text to Image", "Image to Image"])

demo.launch(server_name="0.0.0.0", server_port=8000)