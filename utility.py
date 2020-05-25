from PIL import Image
from matplotlib import pyplot as plt

im = Image.open('input/stone.png')
new_image = im.resize((32, 32))
print(im.size)
print(new_image.size)
print(new_image.mode)

new_image.save("./input/stone32.png")
plt.imshow(new_image)
plt.show()
