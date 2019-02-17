import os
import math
from PIL import Image, ImageFilter

input = r"sample1\input.jpg"
maxwidth = 64
maxheight = 64
smoothingRadius = 2

def rgbToLab(inputColor) :

   num = 0
   RGB = [0, 0, 0]

   for value in inputColor :
       value = float(value) / 255

       if value > 0.04045 :
           value = ((value + 0.055) / 1.055) ** 2.4
       else :
           value = value / 12.92

       RGB[num] = value * 100
       num = num + 1

   XYZ = [0, 0, 0,]

   X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
   Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
   Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
   XYZ[0] = round(X, 4)
   XYZ[1] = round(Y, 4)
   XYZ[2] = round(Z, 4)

   XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
   XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
   XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

   num = 0
   for value in XYZ :

       if value > 0.008856 :
           value = value ** (0.3333333333333333)
       else :
           value = (7.787 * value) + (16 / 116)

       XYZ[num] = value
       num = num + 1

   Lab = [0, 0, 0]

   L = (116 * XYZ[1]) - 16
   a = 500 * (XYZ[0] - XYZ[1])
   b = 200 * (XYZ[1] - XYZ[2])

   Lab[0] = round(L, 4)
   Lab[1] = round(a, 4)
   Lab[2] = round(b, 4)

   return Lab

def rgbToInt(rgb):
    red = rgb[2]
    green = rgb[1]
    blue = rgb[0]
    int = (red << 16) + (green << 8) + blue
    return int

def intToRgb(int):
    blue = int & 255
    green = (int >> 8) & 255
    red = (int >> 16) & 255
    return red, green, blue

# https://en.wikipedia.org/wiki/Color_difference#Euclidean
def euclideanSquaredDistance(rgb1, rgb2):
    return (rgb1[0] - rgb2[0])**2 + (rgb1[1] - rgb2[1])**2 + (rgb1[2] - rgb2[2])**2

# https://en.wikipedia.org/wiki/Color_difference#Euclidean
def euclideanWeightedSquaredDistance(rgb1, rgb2):
    return 2*(rgb1[0] - rgb2[0])**2 + 4*(rgb1[1] - rgb2[1])**2 + 3*(rgb1[2] - rgb2[2])**2

# https://en.wikipedia.org/wiki/Color_difference#CIELAB_%CE%94E*
def cielabSquaredDistance(rgb1, rgb2):
    lab1 = rgbToLab(rgb1)
    lab2 = rgbToLab(rgb2)
    return 2*(lab1[0] - lab2[0])**2 + 4*(lab1[1] - lab2[1])**2 + 3*(lab1[2] - lab2[2])**2

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

input = os.path.dirname(__file__) + "\\" + input
outputFolder = os.path.dirname(input) + "\\"

im = Image.open(input)

inratio = 1.0 * maxwidth / maxheight
ratio = 1.0 * im.size[0] / im.size[1]
if (ratio > inratio):
    maxwidth = (int)(ratio * maxheight)
else:
    maxheight = (int)(ratio * maxwidth)

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