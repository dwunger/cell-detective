from PIL import Image
import os

def tile(file_path):
    image = Image.open(file_path)
    width, height = image.size
    file_name = os.path.basename(file_path)
    base_name, ext = os.path.splitext(file_name)

    # Divide image into quadrants and save them
    image.crop((0, 0, width//2, height//2)).save(f'{base_name}_TL{ext}')  # Top left
    image.crop((width//2, 0, width, height//2)).save(f'{base_name}_TR{ext}')  # Top right
    image.crop((0, height//2, width//2, height)).save(f'{base_name}_BL{ext}')  # Bottom left
    image.crop((width//2, height//2, width, height)).save(f'{base_name}_BR{ext}')  # Bottom right

def collate(file_path):
    file_name = os.path.basename(file_path)
    base_name, ext = os.path.splitext(file_name)
    
    # Load the four image quadrants
    tl = Image.open(f'{base_name}_TL{ext}')
    tr = Image.open(f'{base_name}_TR{ext}')
    bl = Image.open(f'{base_name}_BL{ext}')
    br = Image.open(f'{base_name}_BR{ext}')

    width, height = tl.size[0] + tr.size[0], tl.size[1] + bl.size[1]

    # Create a new, empty image with the combined size
    combined = Image.new('RGB', (width, height))

    # Paste the four images into the new image
    combined.paste(tl, (0, 0))
    combined.paste(tr, (tl.size[0], 0))
    combined.paste(bl, (0, tl.size[1]))
    combined.paste(br, (tl.size[0], tl.size[1]))

    # Save the combined image
    combined.save(f'{base_name}_collated{ext}')
tile(r"C:\Users\dento\Desktop\Python_Projects\colab\image-segmentation\testing\pos\pos\Image_07.tif")
# collate(r"C:\Users\dento\Desktop\Python_Projects\colab\image-segmentation\testing\pos\pos\split\Image_02.tif")