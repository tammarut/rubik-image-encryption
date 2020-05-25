from PIL import Image
from helper import *
import keys
import os


def decrypt(enc_image_name):
    # Config image path
    enc_path = "./encrypted_images/"
    im = Image.open(enc_path + os.path.splitext(enc_image_name)[0] + ".png")
    pix = im.load()

    # Image size (m x n)
    m = im.size[0]
    n = im.size[1]

    # Obtaining the RGB matrices
    r = []
    g = []
    b = []

    # Add pixel value into row and column
    # Row
    for i in range(im.size[0]):
        r.append([])
        g.append([])
        b.append([])
        for j in range(im.size[1]):
            rgbPerPixel = pix[i, j]
            r[i].append(rgbPerPixel[0])
            g[i].append(rgbPerPixel[1])
            b[i].append(rgbPerPixel[2])

    # Read 3 keys from .json
    keys_dict = keys.read_keys()
    Kr = keys_dict['Kr']
    Kc = keys_dict['Kc']
    ITER_MAX = keys_dict['ITER_MAX']
    # These are my 3 keys
    print('Vector Kr:', Kr)
    print('Vector Kc:', Kc)
    print('Iter max:', ITER_MAX)

    # Apply bitwise XOR operator
    # Using vector Kr to bitwise XOR for each column
    for iterations in range(ITER_MAX):
        # For each column
        for j in range(n):
            for i in range(m):
                # If even column, then bitwise XOR with Kr
                # Otherwise bitwise XOR with flipped Kr
                if j % 2 == 0:
                    r[i][j] = r[i][j] ^ Kr[i]
                    g[i][j] = g[i][j] ^ Kr[i]
                    b[i][j] = b[i][j] ^ Kr[i]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kr[i])
                    g[i][j] = g[i][j] ^ rotate180(Kr[i])
                    b[i][j] = b[i][j] ^ rotate180(Kr[i])
        # Using vector Kc, bitwise XOR for each row
        for i in range(m):
            for j in range(n):
                # If Odd row, then bitwise XOR with Kc
                # Otherwise bitwise XOR with flipped Kc
                if (i % 2 == 1):
                    r[i][j] = r[i][j] ^ Kc[j]
                    g[i][j] = g[i][j] ^ Kc[j]
                    b[i][j] = b[i][j] ^ Kc[j]
                else:
                    r[i][j] = r[i][j] ^ rotate180(Kc[j])
                    g[i][j] = g[i][j] ^ rotate180(Kc[j])
                    b[i][j] = b[i][j] ^ rotate180(Kc[j])
        # Reverse Permute Rubik(scrambled image)
        # For each column
        for i in range(n):
            rTotalSum = 0
            gTotalSum = 0
            bTotalSum = 0
            for j in range(m):
                rTotalSum += r[j][i]
                gTotalSum += g[j][i]
                bTotalSum += b[j][i]
            rModulus = rTotalSum % 2
            gModulus = gTotalSum % 2
            bModulus = bTotalSum % 2
            # After mod 2, if equal 0 then shift down(circular)
            # Otherwise shift up(circular)
            if (rModulus == 0):
                downshift(r, i, Kc[i])
            else:
                upshift(r, i, Kc[i])
            if (gModulus == 0):
                downshift(g, i, Kc[i])
            else:
                upshift(g, i, Kc[i])
            if (bModulus == 0):
                downshift(b, i, Kc[i])
            else:
                upshift(b, i, Kc[i])

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
            if (rModulus == 0):
                r[i] = numpy.roll(r[i], -Kr[i])
            else:
                r[i] = numpy.roll(r[i], Kr[i])
            if (gModulus == 0):
                g[i] = numpy.roll(g[i], -Kr[i])
            else:
                g[i] = numpy.roll(g[i], Kr[i])
            if (bModulus == 0):
                b[i] = numpy.roll(b[i], -Kr[i])
            else:
                b[i] = numpy.roll(b[i], Kr[i])

    # Fill decrypted image in pix(pointer of original image)
    for i in range(m):
        for j in range(n):
            pix[i, j] = (r[i][j], g[i][j], b[i][j])

    # Save decrypted image
    im.save("decrypted_images/" + enc_image_name)
