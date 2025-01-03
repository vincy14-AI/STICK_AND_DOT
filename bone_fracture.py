import os
import requests
from bs4 import BeautifulSoup
import zipfile

# URL of the website hosting bone fracture images (replace with actual URL)
url = "https://www.kaggle.com/datasets/ahmedashrafahmed/bone-fracture"

# Directory to save the images
output_dir = "bone_fracture_images"
os.makedirs(output_dir, exist_ok=True)

# Function to download an image
def download_image(image_url, save_path):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(save_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download {image_url}")
    except Exception as e:
        print(f"Error downloading {image_url}: {e}")

# Scrape images from the website
def scrape_images(url, output_dir):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to access {url}: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all image tags
        img_tags = soup.find_all("img")
        for i, img_tag in enumerate(img_tags):
            # Get the image URL (ensure it's absolute)
            img_url = img_tag.get("src")
            if not img_url.startswith("http"):
                img_url = requests.compat.urljoin(url, img_url)

            # Save the image locally
            save_path = os.path.join(output_dir, f"image_{i+1}.jpg")
            download_image(img_url, save_path)
    except Exception as e:
        print(f"Error scraping images from {url}: {e}")

# Create a ZIP file of the downloaded images
def create_zip(output_dir, zip_filename):
    zip_path = os.path.join(output_dir, zip_filename)
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".jpg"):
                    zipf.write(os.path.join(root, file), file)
    print(f"ZIP file created: {zip_path}")

# Run the scraper
scrape_images(url, output_dir)

# Create the ZIP file of the downloaded images
create_zip(output_dir, "bone_fracture_images1.zip")

print(f"All images have been downloaded and saved in a ZIP file: {os.path.join(output_dir, 'bone_fracture_images.zip')}")
