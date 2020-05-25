from PIL import Image
from random import randint
from helper import *
import keys
import os


def encrypt(image_name):
	# Config image path
	input_path = "./input/"
	name, ext = os.path.splitext(image_name)

	# Open image as grayscale and parse to numpy array
	im = Image.open(input_path + name + ext)
	pix = im.load()

	# Image size (m x n)
	m = im.size[0]
	n = im.size[1]

	# Obtaining the RGB matrices
	r = []
	g = []
	b = []
	# Add pixel value into row, column
	# Row
	for i in range(im.size[0]):
		r.append([])
		g.append([])
		b.append([])
		# Column
		for j in range(im.size[1]):
			rgbPerPixel = pix[i,j]
			r[i].append(rgbPerPixel[0])
			g[i].append(rgbPerPixel[1])
			b[i].append(rgbPerPixel[2])

	# Vectors Kr and Kc
	alpha = 8
	Kr = [randint(0,pow(2,alpha)-1) for i in range(m)]
	Kc = [randint(0,pow(2,alpha)-1) for i in range(n)]
	ITER_MAX = 1

	# These are my 3 keys
	print('Vector Kr:', Kr)
	print('Vector Kc:', Kc)
	print('Iter max:', ITER_MAX)
	# Save 3 keys(Kr, Kc, ITER_MAX) as .json
	keys.save_keys(Kr, Kc, ITER_MAX)

	# Permute Rubik(scrambled image)
	for iterations in range(ITER_MAX):
		# For each row
		for i in range(m):
			# Sum of all elements in row
			rTotalSum = sum(r[i])
			gTotalSum = sum(g[i])
			bTotalSum = sum(b[i])
			# Modulo 2
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			# After mod 2, if equal 0 then shift right(circular)
			# Otherwise shift left(circular)
			if(rModulus==0):
				r[i] = numpy.roll(r[i],Kr[i])
			else:
				r[i] = numpy.roll(r[i],-Kr[i])
			if(gModulus==0):
				g[i] = numpy.roll(g[i],Kr[i])
			else:
				g[i] = numpy.roll(g[i],-Kr[i])
			if(bModulus==0):
				b[i] = numpy.roll(b[i],Kr[i])
			else:
				b[i] = numpy.roll(b[i],-Kr[i])

		# For each column
		for i in range(n):
			rTotalSum = 0
			gTotalSum = 0
			bTotalSum = 0
			# Sum of all elements in column
			for j in range(m):
				rTotalSum += r[j][i]
				gTotalSum += g[j][i]
				bTotalSum += b[j][i]
			# Modulo 2
			rModulus = rTotalSum % 2
			gModulus = gTotalSum % 2
			bModulus = bTotalSum % 2
			# After mod 2, if equal 0 then shift up(circular)
			# Otherwise shift down(circular)
			if(rModulus==0):
				upshift(r,i,Kc[i])
			else:
				downshift(r,i,Kc[i])
			if(gModulus==0):
				upshift(g,i,Kc[i])
			else:
				downshift(g,i,Kc[i])
			if(bModulus==0):
				upshift(b,i,Kc[i])
			else:
				downshift(b,i,Kc[i])
		# Apply bitwise XOR operator
		# Using vector Kc, bitwise XOR for each row
		for i in range(m):
			for j in range(n):
				# If Odd row, then bitwise XOR with Kc
				# Otherwise bitwise XOR with flipped Kc
				if(i%2==1):
					r[i][j] = r[i][j] ^ Kc[j]
					g[i][j] = g[i][j] ^ Kc[j]
					b[i][j] = b[i][j] ^ Kc[j]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kc[j])
					g[i][j] = g[i][j] ^ rotate180(Kc[j])
					b[i][j] = b[i][j] ^ rotate180(Kc[j])
		# Using vector Kr to bitwise XOR for each column
		for j in range(n):
			for i in range(m):
				# If even column, then bitwise XOR with Kr
				# Otherwise bitwise XOR with flipped Kr
				if(j%2==0):
					r[i][j] = r[i][j] ^ Kr[i]
					g[i][j] = g[i][j] ^ Kr[i]
					b[i][j] = b[i][j] ^ Kr[i]
				else:
					r[i][j] = r[i][j] ^ rotate180(Kr[i])
					g[i][j] = g[i][j] ^ rotate180(Kr[i])
					b[i][j] = b[i][j] ^ rotate180(Kr[i])

	# Fill encrypt image in pix(pointer of original image)
	for i in range(m):
		for j in range(n):
			pix[i,j] = (r[i][j],g[i][j],b[i][j])

	# Save encrypted image
	im.save('encrypted_images/' + name + ".png")



