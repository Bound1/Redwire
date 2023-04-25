from fastapi import FastAPI
from api.image_generation import *
import gradio as gr
from models.input_text_to_image import InputText
import requests
adresse_ip="127.0.0.1"
parametres=["prompt","height","width","num_inference","guidance_scale","negative_prompt","num_images"]
def fonction_envoi(prompt,height,width,num_inference,guidance_scale,negative_prompt,num_images):
    dict_to_json={
    "prompt":prompt,
    "height":height,
    "width":width,
    "num_inference":num_inference,
    "guidance_scale":guidance_scale,
    "negative_prompt":negative_prompt,
    "num_images":num_images}
    url=f"http://{adresse_ip}:8000/api/text_to_image"
    requests.post(url, json = dict_to_json)
    return f"generated_images/{prompt}.png"
app = FastAPI()
app.include_router(router, prefix="/api")
io = gr.Interface(fonction_envoi, [gr.Textbox(placeholder=_,label=_) for _ in parametres], "image")
app = gr.mount_gradio_app(app, io, path="/gradio")