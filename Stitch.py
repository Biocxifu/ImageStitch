import os
from PIL import Image


# Read image files and save them in a list
def load_images(path,sort=False):
    # Read all image files in the directory
    files = [f for f in os.listdir(path) if f.endswith('.png') or f.endswith('.jpg') or f.endswith('.jpeg')]
    if sort:
        files.sort() #ascending order
        # files.sort(reverse=True) #descending order
    images = []
    print("Splicing images：")
    for file in files:
        if "horizontal" not in os.path.basename(file) and "vertical" not in os.path.basename(file):
            print(os.path.basename(file))
            img = Image.open(os.path.join(path,file))
            images.append(img)
    return images

def get_max_dimensions(images):
    max_width = 0
    max_height = 0

    for image in images:
        width, height = image.size
        if width > max_width:
            max_width = width
        if height > max_height:
            max_height = height

    return (max_width, max_height)


# Enlarge the image proportionally to the given width
def resize_image_w(img, width):
    # 计算等比例放大后图片的高度
    height = int(width * img.height / img.width)
    # 按照给定高度等比例放大图片
    img = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    return img

# Enlarge the image proportionally to the given height
def resize_image_h(img, height):
    width = int(height * img.width / img.height)
    img = img.resize((width, height), resample=Image.Resampling.LANCZOS)
    return img


# direction:  "horizontal"、"vertical"
# height: The height of the long image

direction: "horizontal"

def combine_images(images, direction):

    # Find the maximum width and height in the original image
    max_width,max_height = get_max_dimensions(images)
    a,b=[],[]
    # After the original image is enlarged, the width and height may change, so the maximum width and height may also change
    for img in images:
        t1 = resize_image_h(img,max_height)
        t2 = resize_image_w(img, max_width)
        a.append(t1.width)
        a.append(t2.width)
        b.append(t1.height)
        b.append(t2.height)

    if direction == "vertical":
        # Calculate the width and height of the stitched image
        width = max_width
        # For simplicity, simply taking the maximum value of all values will result in a blank canvas at the end of the long image, which will be removed later
        height = max(b)*len(images)
        # create a new picture
        combined = Image.new('RGB', (width, height))
        # Splice each image
        y_offset = 0
        for img in images:
            img = resize_image_w(img,width)
            combined.paste(img, (0, y_offset))
            y_offset += img.height

    elif direction == "horizontal":
        # Calculate the width and height of the stitched image
        width = max(a)*len(images)
        height = max_height
        # create a new picture
        combined = Image.new('RGB', (width, height))
        # Splice each image
        x_offset = 0
        for img in images:
            img = resize_image_h(img, height)
            combined.paste(img, (x_offset, 0))
            x_offset += img.width
    # Remove blank canvas
    combined = combined.crop(combined.getbbox())
    return combined

# save the spliced image
def save_image(image, path):
    # Non-destructive preservation
    image.save(path,quality=100)
    print("Image stitching successful!")

# 
if __name__ == '__main__':
    path = os.getcwd()
    print(path)
    images = load_images(path)
    #vertical = combine_images(images, "vertical")
    #save_image(vertical, os.path.join(path, 'vertical.jpg'))
    horizontal = combine_images(images, "horizontal")
    save_image(horizontal, os.path.join(path, 'horizontal.jpg'))