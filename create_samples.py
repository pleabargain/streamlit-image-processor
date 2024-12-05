from PIL import Image, ImageDraw, ImageFont
import os

# Create sample_images directory if it doesn't exist
os.makedirs('sample_images', exist_ok=True)

def create_text_image(text, filename, size=(400, 200), bg_color='white', text_color='black'):
    # Create new image with white background
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a system font
    try:
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((x, y), text, fill=text_color, font=font)
    
    # Save image
    image.save(f'sample_images/{filename}.jpg', 'JPEG')

# Create sample images
create_text_image('Hello World!\nThis is a sample text\nfor OCR testing.', 'sample1')
create_text_image('Invoice #12345\nTotal: $99.99\nDate: 2024-01-01', 'sample2')
create_text_image('IMPORTANT NOTICE\nPlease read carefully\nContact: info@example.com', 'sample3')
