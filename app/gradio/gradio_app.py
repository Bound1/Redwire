import os
import uuid
import gradio as gr
from utils import generate_text_to_image, generate_image_to_image, image_from_url_text


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


def text_to_image_wrapper(prompt, negative_prompt, num_inference, num_images_per_prompt, height, width, guidance_scale):
    if height % 8 != 0 or width % 8 != 0:
        raise ValueError("Height and width must be divisible by 8.")
    image = generate_text_to_image(prompt, height, width, num_inference, guidance_scale, negative_prompt,
                                   num_images_per_prompt)
    return image


def image_to_image_wrapper(prompt, negative_prompt, num_images_per_prompt, num_inference_steps, image, strength,
                           guidance_scale):
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

with gr.Blocks() as demo:
    gr.Markdown("Text/Image to Image Generator"),
    with gr.Tab("Generate images from textual prompts using an AI model"):
        with gr.Row():
            with gr.Column():
                text2image_prompt = gr.inputs.Textbox(lines=2, label="Prompt")
                text2image_negative_prompt = gr.inputs.Textbox(lines=2, label="Negative Prompt")
                text2image_sampling_steps = gr.inputs.Slider(minimum=1, maximum=50, step=1, default=50,
                                                             label="Sampling Steps")
                text2image_images_per_prompt = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1,
                                                                label="Images Per "
                                                                      "Prompt")
                text2image_height = gr.inputs.Slider(minimum=1, maximum=1024, step=8, default=512, label="Height")
                text2image_width = gr.inputs.Slider(minimum=1, maximum=1024, step=8, default=512, label="Width")
                text2image_guidance_scale = gr.inputs.Slider(minimum=0, maximum=12, step=0.5, default=7.5,
                                                             label="Guidance Scale")
            with gr.Row():
                with gr.Column():
                    text2image_output = gr.Gallery(label='Output').style(grid=4)
                    text2image_save = gr.Button('Save Image', elem_id='save_text2image')
                    text2image_button = gr.Button("Generate Image from Text")
                    text2image_download_files = gr.Files(None, file_count="multiple", interactive=False,file_types=["png"],
                                                         show_label=False,
                                                         visible=False, elem_id='download_files}')
    with gr.Tab("Generate images from an input image using an AI model"):
        with gr.Row():
            with gr.Column():
                image2image_prompt = gr.inputs.Textbox(lines=2, label="Prompt")
                image2image_negative_prompt = gr.inputs.Textbox(lines=2, label="Negative Prompt")
                image2image_sampling_steps = gr.inputs.Slider(minimum=1, maximum=50, step=1, default=50,
                                                              label="Sampling Steps")
                image2image_images_per_prompt = gr.inputs.Slider(minimum=1, maximum=10, step=1, default=1,
                                                                 label="Images Per Prompt")
                image2image_image = gr.inputs.Image(shape=(512, 512), label="Input Image")
                image2image_strength = gr.inputs.Slider(minimum=0, maximum=1.0, step=0.1, default=1.0, label="Strength")
                image2image_guidance_scale = gr.inputs.Slider(minimum=0, maximum=12, step=0.5, default=7.5,
                                                              label="Guidance Scale")
            with gr.Row():
                with gr.Column():
                    image2image_output = gr.Gallery(label='Output', show_label=False,
                                                    elem_id="image_to_image_gallery").style(grid=4)
                    image_2_image_button = gr.Button("Generate Image from Image")

    text2image_button.click(text_to_image_wrapper, inputs=
    [text2image_prompt, text2image_negative_prompt, text2image_sampling_steps, text2image_images_per_prompt,
     text2image_height, text2image_width, text2image_guidance_scale],
                            outputs=text2image_output)

    image_2_image_button.click(image_to_image_wrapper,
                               inputs=[image2image_prompt, image2image_negative_prompt, image2image_images_per_prompt,
                                       image2image_sampling_steps, image2image_image, image2image_strength,
                                       image2image_guidance_scale],
                               outputs=image2image_output)

    text2image_save.click(fn=save_image_gallery, inputs=[text2image_output], outputs=text2image_download_files)

demo.launch()
