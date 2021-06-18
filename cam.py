from PIL import Image
from picamera import PiCamera
from datetime import datetime
from fractions import Fraction
import statistics
import matplotlib.colors
import numpy
import time
import numpy
import os

def get_hsv(pixels):							# Fá meðaltal af lit, litadýpt og birtustigi (HSV) myndpunktanna
	i_h = matplotlib.colors.rgb_to_hsv(pixels/255)
	h = int(numpy.average(i_h[:,:,0]) * 360)
	s = int(numpy.average(i_h[:,:,1]) * 100)
	v = int(numpy.average(i_h[:,:,2]) * 100)
	std_h = int(numpy.std(i_h[:,:,0]) * 360)
	std_s = int(numpy.std(i_h[:,:,1]) * 100)
	std_v = int(numpy.std(i_h[:,:,2]) * 100)
	return [h,s,v]

def get_stds(pixels): # Fá staðalfrávik af HSV-gildum myndpunktanna
	i_h = matplotlib.colors.rgb_to_hsv(pixels/255)
	std_h = int(numpy.std(i_h[:,:,0]) * 360)
	std_s = int(numpy.std(i_h[:,:,1]) * 100)
	std_v = int(numpy.std(i_h[:,:,2]) * 100)
	return std_h,std_s,std_v

def get_edginess(img):							# Setja síu á myndina sem sýnir bara brúnir, tel magn brúnanna yfir alla myndina
	# Apply gray scale
	gray_img = numpy.round(0.299 * img[:, :, 0] +
						0.587 * img[:, :, 1] +
						0.114 * img[:, :, 2]).astype(numpy.uint8)

	# Sobel Operator
	h, w = gray_img.shape
	# define filters
	horizontal = numpy.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])  # s2
	vertical = numpy.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])  # s1

	# define images with 0s
	newhorizontalImage = numpy.zeros((h, w))
	newverticalImage = numpy.zeros((h, w))
	newgradientImage = numpy.zeros((h, w))

	# offset by 1
	for i in range(1, h - 1):
		for j in range(1, w - 1):
			horizontalGrad = (horizontal[0, 0] * gray_img[i - 1, j - 1]) + \
							 (horizontal[0, 1] * gray_img[i - 1, j]) + \
							 (horizontal[0, 2] * gray_img[i - 1, j + 1]) + \
							 (horizontal[1, 0] * gray_img[i, j - 1]) + \
							 (horizontal[1, 1] * gray_img[i, j]) + \
							 (horizontal[1, 2] * gray_img[i, j + 1]) + \
							 (horizontal[2, 0] * gray_img[i + 1, j - 1]) + \
							 (horizontal[2, 1] * gray_img[i + 1, j]) + \
							 (horizontal[2, 2] * gray_img[i + 1, j + 1])

			newhorizontalImage[i - 1, j - 1] = abs(horizontalGrad)

			verticalGrad = (vertical[0, 0] * gray_img[i - 1, j - 1]) + \
						   (vertical[0, 1] * gray_img[i - 1, j]) + \
						   (vertical[0, 2] * gray_img[i - 1, j + 1]) + \
						   (vertical[1, 0] * gray_img[i, j - 1]) + \
						   (vertical[1, 1] * gray_img[i, j]) + \
						   (vertical[1, 2] * gray_img[i, j + 1]) + \
						   (vertical[2, 0] * gray_img[i + 1, j - 1]) + \
						   (vertical[2, 1] * gray_img[i + 1, j]) + \
						   (vertical[2, 2] * gray_img[i + 1, j + 1])

			newverticalImage[i - 1, j - 1] = abs(verticalGrad)

			# Edge Magnitude
			mag = numpy.sqrt(pow(horizontalGrad, 2.0) + pow(verticalGrad, 2.0))
			newgradientImage[i - 1, j - 1] = mag

	return int(numpy.average(newgradientImage))

def get_contrast(pixels):						# Fá staðalfrávik í birtustigi myndpunktanna
	p = getgrays(pixels)
	return int(numpy.std(p))

def getgrays(rgb): # Prenta myndina í gráu
	return numpy.dot(rgb[...,:3], [0.2989, 0.5870, 0.1140])

col_data_path = "data/image_data.csv"

if not os.path.isfile(col_data_path): 					# Ef gagnaskráin er ekki til staðar er hún búin til og haus prentaður
	f = open(col_data_path, "w")
	f.write("time,shutter,gain,h,s,v,std_h,std_s,std_v,edges,contrast\n")
	f.close()

camera = PiCamera()							# Ræsi myndavélina. Þessar stillingar reyndust bestar eftir einhverja prófun:
camera.exposure_mode = 'backlight'
camera.awb_mode = 'sunlight'
camera.iso = 100

while True:
	now = datetime.now()
	filename = "imgdump/" + now.strftime("%Y%m%dT%H%M%S.jpg")	# Lokaútgáfa myndarinnar verður vistuð hér
	camera.capture("processing.jpg")				# Vinnslumyndin er vistuð hér - gæti þurft að taka aðra
	speed = str(int(camera.exposure_speed))
	gain = str(float(camera.analog_gain))
	i = Image.open("processing.jpg")
	p = numpy.array(i)
	i_r = int(numpy.average(p[:,:,0]))
	i_g = int(numpy.average(p[:,:,1]))
	i_b = int(numpy.average(p[:,:,2]))
	a_r = str(i_r)
	a_g = str(i_g)
	a_b = str(i_b)
	print('iso: ' + str(camera.iso) + ', spd: ' + str(camera.exposure_speed), end="\r")
	if (i_r + i_g + i_b) < 100:					# Athugar hvort myndin sé of dimm (min=0, max=3*255)...
		if camera.iso < 800:					# ...og hækkar þá næmni myndavélarinnar ef það er hægt
			camera.iso = camera.iso * 2
			continue					# og sleppir myndgreiningunni -- tekur aðra mynd á nýjum stillingum
	elif (i_r + i_g + i_b) > 600:					# Athugar hvort myndin sé of björt...
		if int(camera.exposure_speed) == 0:			# ...og ef hægt er að stytta lokatímann er það gert
			pass
		else:
			camera.shutter_speed = int(camera.exposure_speed * 0.5)
			continue
	try:
		print('iso: ' + str(camera.iso) + ', spd: ' + str(camera.exposure_speed) + " at " + now.strftime("%H:%M:%S"))
		speed = str(int(camera.exposure_speed))
		gain = str(float(camera.analog_gain))
		i.save("latest.jpg")					# Vista myndina einu sinni sem nýjustu mynd...
		i.save(filename)					# ...og einu sinni fyrir gagnabankann
		p = numpy.asarray(i)
		hsv = get_hsv(p)
		contrast = get_contrast(p)
		stds = get_stds(p)
		edges = get_edginess(p)
		f = open(col_data_path, "a")				# Skrifa alla kvarða myndarinnar í CSV skrána
		f.write(now.strftime("%Y-%m-%dT%H:%M:%SZ,"))
		f.write(speed + "," + gain + ",")
		f.write(",".join(str(x) for x in get_hsv(p)) + ",")
		f.write(",".join(str(x) for x in get_stds(p)) + ",")
		f.write(str(edges) + ",")
		f.write(str(contrast) + "\n")
		f.close()
		camera.iso = 100					# Núllstilli myndavélina
		camera.shutter_speed = 0
	except Exception as e:
		print('Villa: ' + str(e))
	time.sleep(10*60)						# Næstum óþarft því útreikningarnir taka heila eilífð
