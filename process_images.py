import os
import requests
from PIL import Image
from io import BytesIO

def download_image(url, filename):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def process_image(image, size, output_path):
    # Calculate dimensions maintaining aspect ratio
    target_width, target_height = size
    ratio = min(target_width/image.width, target_height/image.height)
    new_size = (int(image.width * ratio), int(image.height * ratio))
    
    # Resize image
    resized = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Create new image with target size and paste resized image centered
    new_image = Image.new('RGB', size, (0, 0, 0))
    paste_x = (target_width - new_size[0]) // 2
    paste_y = (target_height - new_size[1]) // 2
    new_image.paste(resized, (paste_x, paste_y))
    
    # Save with optimization
    new_image.save(output_path, 'JPEG', quality=85, optimize=True)

# Image URLs from Unsplash (free commercial use)
images = {
    'index': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab',  # Modern city skyline
    'about': 'https://images.unsplash.com/photo-1497366811353-6870744d04b2',  # Modern office meeting
    'contact': 'https://images.unsplash.com/photo-1497366216548-37526070297c',  # Corporate office
    'presence': 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e'  # World map
}

# Size configurations for new design
sizes = {
    'desktop': {
        'home': (1920, 1080),    # 16:9 for homepage
        'page': (1920, 800)      # Wider but shorter for other pages
    },
    'tablet': {
        'home': (1024, 768),     # 4:3 for better tablet view
        'page': (1024, 600)      # Proportional reduction
    },
    'mobile': {
        'home': (640, 960),      # Portrait orientation for mobile
        'page': (640, 400)       # Compact header for inner pages
    }
}

# Process each image
for page, url in images.items():
    print(f"Processing {page} images...")
    img = download_image(url, f"{page}.jpg")
    
    for device in sizes.keys():
        size = sizes[device]['home'] if page == 'index' else sizes[device]['page']
        output_path = f"images/headers/{device}/{page}-header.jpg"
        process_image(img, size, output_path)
        print(f"Created {output_path}")

print("All images processed successfully!") 