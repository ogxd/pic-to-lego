import math

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