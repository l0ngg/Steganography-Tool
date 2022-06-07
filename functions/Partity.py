from PIL import Image

im = Image.open(r"D:\Steganography\Code\Steganography-Tool\result.png")
im_2 = Image.open(r"D:\Steganography\Code\Steganography-Tool\new_result.png")

def steganalyse(img: im) -> Image.Image:
    """
    Steganlysis of the LSB technique.
    """
    encoded = Image.new(img.mode, (img.size))
    width, height = img.size
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))[0:3]
            if r % 2 == 0:
                r = 0
            else:
                r = 255
            if g % 2 == 0:
                g = 0
            else:
                g = 255
            if b % 2 == 0:
                b = 0
            else:
                b = 255
            encoded.putpixel((col, row), (r, g, b))
    return encoded


new_im = steganalyse(im)
new_im.show()

new_im_2 = steganalyse(im_2)
new_im_2.show()



