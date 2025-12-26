
from PIL import Image, ImageEnhance
import os
from random import randrange
import secrets
import glob

def do_the_trick(path):
	img = Image.open(path)

	rand = secrets.token_hex(16)
	basewidth = 500
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.Resampling.LANCZOS)
	img.save("./uploaded_images/"+rand+"_up.png")
	string = "backgroundremover -i " + "./uploaded_images/"+rand+"_up.png" + " -m "+ "u2net_human_seg" + " -o " + "./uploaded_images/"+rand+"_res.png"
	os.system(string)

	cropedImage = Image.open("./uploaded_images/"+rand+"_res.png")
	converter = ImageEnhance.Color(cropedImage)
	cropedImage = converter.enhance(0)
	cropedImage.save("./uploaded_images/"+rand+".png")

	files = glob.glob('./uploaded_images/*_up.png') + glob.glob('./uploaded_images/*_res.png')
	for file in files:
		os.remove(file)

	return rand
