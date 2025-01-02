import torch
import random
from diffusers import StableDiffusionPipeline
import os
from PIL import Image

# Set a fixed seed for reproducibility
random.seed(42)
torch.manual_seed(42)

# Step 1: Load a pretrained GAN model
model_name = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_name)

# Move the model to the correct device (use "cuda" for GPU or "cpu" for CPU)
pipe.to("cuda")  # Use GPU for faster generation

# Step 2: Generate synthetic images
output_dir = "bone_fracture_images"
os.makedirs(output_dir, exist_ok=True)

num_images = 100  # Number of images to generate
prompt = "X-ray of a human bone with visible fractures, realistic, medical imaging style"

def is_black_image(image: Image) -> bool:
    """Check if an image is mostly black."""
    grayscale_image = image.convert("L")  # Convert to grayscale
    histogram = grayscale_image.histogram()
    black_pixels = histogram[0]  # Count of black pixels
    total_pixels = sum(histogram)
    return black_pixels / total_pixels > 0.9  # Threshold for "mostly black"

generated_images = 0
attempts = 0

while generated_images < num_images and attempts < num_images * 10:
    image = pipe(prompt).images[0]  # Generate an image
    attempts += 1

    if not is_black_image(image):  # Check if the image is not mostly black
        image.save(os.path.join(output_dir, f"bone_fracture_{generated_images+1}.png"))
        print(f"Generated image {generated_images+1}/{num_images}")
        generated_images += 1
    else:
        print(f"Discarded black image. Attempt {attempts}")

print(f"Bone fracture dataset created with {generated_images} images in: {output_dir}")