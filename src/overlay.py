from PIL import Image, ImageEnhance
import os
import secrets
import subprocess


def do_the_trick(path, output_dir):
	os.makedirs(output_dir, exist_ok=True)

	img = Image.open(path)

	rand = secrets.token_hex(16)
	basewidth = 500
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), Image.ANTIALIAS)

	up_path = os.path.join(output_dir, f"{rand}_up.png")
	res_path = os.path.join(output_dir, f"{rand}_res.png")
	final_path = os.path.join(output_dir, f"{rand}.png")

	img.save(up_path)

	# Remove background
	subprocess.run(
		[
			"backgroundremover",
			"-i",
			up_path,
			"-m",
			"u2net_human_seg",
			"-o",
			res_path,
		],
		check=True,
	)

	cropedImage = Image.open(res_path)
	converter = ImageEnhance.Color(cropedImage)
	cropedImage = converter.enhance(0)
	cropedImage.save(final_path)

	for tmp_path in (up_path, res_path):
		try:
			os.remove(tmp_path)
		except FileNotFoundError:
			pass

	return rand
