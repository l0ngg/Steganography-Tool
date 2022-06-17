# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from imp import new_module
from PIL import Image

# Pixels are modified according to the
# 8-bit binary data and finally returned
def mod_pixel(pix, data):

	# Convert encoding data into 8-bit binary
	# form using ASCII value of characters
	datalist = []
	for i in data:
		datalist.append(format(ord(i), '08b'))

	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1

		# Last pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in mod_pixel(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode text data into image
def encode_lsb(img, msg, res):
	image = Image.open(img, 'r')

	if (len(msg) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, msg)

	newimg.save(res, str(res.split(".")[1].upper()))

# Decode the text data in the image
def decode_lsb(img):
	image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] + imgdata.__next__()[:3] + imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

def main():
	a = int(input(
    ":: Welcome to my LSB tool, what do you want to do ::\n"
	"1. Encode\n2. Decode\n"))
	if (a == 1):
		img = input('Enter the file path(with extension):\n')
		msg = input('Enter the message:\n')
		new_img_name = input("Enter the name of new image(with extension) :\n")
		encode_lsb(img, msg, new_img_name)

	elif (a == 2):
		img = input("Enter image name(with extension) : ")
		print("Decoded Word : " + decode_lsb(img))
	else:
		raise Exception("Enter correct input")

if __name__ == '__main__' :
	main()