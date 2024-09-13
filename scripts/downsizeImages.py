import os
from PIL import Image

# Path to your folder with images
image_folder = 'app/static/assets/img/drive/uncompressed'
output_folder = 'app/static/assets/img/drive'

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Set the desired quality (between 1 and 100, 85 is usually a good compromise)
quality = 25

# Loop through all files in the folder
for filename in os.listdir(image_folder):
    if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
        img_path = os.path.join(image_folder, filename)
        img = Image.open(img_path)
        
        # Save image with a reduced quality setting
        output_path = os.path.join(output_folder, filename)
        
        # Convert PNGs to JPEG to reduce size further (optional)
        if filename.endswith(".png"):
            img = img.convert('RGB')
            output_path = output_path.replace(".png", ".jpg")
        
        # Save the image with compression
        img.save(output_path, optimize=True, quality=quality)

        print(f"Compressed and saved: {output_path}")

print("All images compressed successfully!")
