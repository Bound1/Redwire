from diffusers import StableDiffusionImageVariationPipeline
from PIL import Image
from torch.distributions import transforms

device = "cuda:0"
sd_pipe = StableDiffusionImageVariationPipeline.from_pretrained(
  "lambdalabs/sd-image-variations-diffusers",
  revision="v2.0",
  )
sd_pipe = sd_pipe.to(device)

im = Image.open("trainer.jpg")
tform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize(
        (224, 224),
        interpolation=transforms.InterpolationMode.BICUBIC,
        antialias=False,
        ),
    transforms.Normalize(
      [0.48145466, 0.4578275, 0.40821073],
      [0.26862954, 0.26130258, 0.27577711]),
])
inp = tform(im).to(device).unsqueeze(0)

out = sd_pipe(inp, guidance_scale=3)
out["images"][0].save("result.jpg")


####################"



@router.post("/image_variation/")
async def image_variation(file: UploadFile = File(...), guidance_scale: int = 3):
    # Save the uploaded image
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    # Load the image with PIL and apply the necessary transforms
    im = Image.open(file_path)
    tform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(
            (224, 224),
            interpolation=transforms.InterpolationMode.BICUBIC,
            antialias=False,
        ),
        transforms.Normalize(
            [0.48145466, 0.4578275, 0.40821073],
            [0.26862954, 0.26130258, 0.27577711]
        ),
    ])
    inp = tform(im).to(device).unsqueeze(0)

    # Apply the image variation using the StableDiffusionImageVariationPipeline
    out = sd_pipe(inp, guidance_scale=guidance_scale)

    # Save the output image to a file and return it as a response
    output_filename = f"output_{filename}"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    out["images"][0].save(output_path)
    return FileResponse(output_path, media_type="image/png")



#############

    def generate_image(self, prompt, image, strength, num_inference_steps, guidance_scale,
                       negative_prompt, num_images_per_prompt, image_path):
        with torch.no_grad():
            im = Image.open(image_path)
            tform = transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize(
                    (224, 224),
                    interpolation=transforms.InterpolationMode.BICUBIC,
                    antialias=False,
                ),
                transforms.Normalize(
                    [0.48145466, 0.4578275, 0.40821073],
                    [0.26862954, 0.26130258, 0.27577711]),
            ])
            inp = tform(im).to(self.device).unsqueeze(0)
            out = self.pipe(inp, guidance_scale=guidance_scale)
        return out["images"][0]