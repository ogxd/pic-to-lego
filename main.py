import os
import math
import sys
from color_functions import intToRgb, rgbToInt, rgbToLab, euclideanSquaredDistance, euclideanSquaredDistance, cielabSquaredDistance
from PIL import Image, ImageFilter

try:
    input = sys.argv[1]
    maxwidth = int(sys.argv[2])
    maxheight = int(sys.argv[3])
    smoothingRadius = float(sys.argv[4])
except:
    input = r"sample1\input.jpg"
    maxwidth = 64
    maxheight = 64
    smoothingRadius = 2

class LegoBlock:
    def __init__(self, rgb, id):
        self.rgb = rgb
        self.id = id
        self.count = 0

blocks = [
    LegoBlock(intToRgb(0xffcd03), 300524),
    LegoBlock(intToRgb(0xf57d20), 3005106),
    LegoBlock(intToRgb(0xdd1a21), 300521),
    LegoBlock(intToRgb(0xe95da2), 3005221),
    LegoBlock(intToRgb(0x006cb7), 300523),
    LegoBlock(intToRgb(0x00a3da), 3005321),
    LegoBlock(intToRgb(0xcce197), 3005326),
    LegoBlock(intToRgb(0x00af4d), 300537),
    LegoBlock(intToRgb(0x9aca3c), 3005119),
    LegoBlock(intToRgb(0x692e14), 3005192),
    LegoBlock(intToRgb(0x000000), 3005126),
    LegoBlock(intToRgb(0xde8b5f), 300518),
    LegoBlock(intToRgb(0xffffff), 30051),
]

input = os.getcwd()+ "\\" + input
outputFolder = os.getcwd() + "\\"

im = Image.open(input)

inratio = 1.0 * maxwidth / maxheight
ratio = 1.0 * im.size[0] / im.size[1]
maxwidth = (int)(ratio * maxheight)

im = im.filter(ImageFilter.GaussianBlur(radius=smoothingRadius))
im = im.resize((maxwidth, maxheight), Image.NEAREST)
out = Image.new('RGB', im.size, 0xffffff)

width, height = im.size
for x in range(width):
    for y in range(height):
        r,g,b = im.getpixel((x, y))
        closestBlock = LegoBlock((0, 0, 0), 0)
        idealBlock = LegoBlock((r, g, b), 0)
        smallestDistance = 100000.0
        for block in blocks:
            distance = euclideanSquaredDistance(idealBlock.rgb, block.rgb)
            if (distance < smallestDistance):
                smallestDistance = distance
                closestBlock = block
                
        closestBlock.count = closestBlock.count + 1
        out.putpixel((x,y), rgbToInt(closestBlock.rgb))

out.save(outputFolder + "one-block-per-pixel.png")
out = out.resize((4 * maxwidth, 4 * maxheight), Image.NEAREST)
out.save(outputFolder + "one-block-per-pixel-x4.png")

for block in blocks:
    if (block.count > 0):
        print ("- " + str(block.count) + " 1x1 " + str(block.rgb) + " ID: " + str(block.id))

print("done")