import ImageFont
import Image
import ImageDraw
import logging

# Grab Logger
logger = logging.getLogger('mainlog')

'''
the rotated text function draws text rotated at an angle at a center coordinate pair
INPUTS:
    imageObject: the image object to draw on
    string: the text to write
    angle: the angle to rotate 
    fontSize: fontsize of the text 
    x: center x-coordinate
    y: center y-coordinate
'''
def rotatedText(imageObject, string, angle, fontSize, x, y):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fontSize)
    imtmp = Image.new('1', (font.getsize(string)[0], fontSize), 255)
    drawtmp = ImageDraw.Draw(imtmp)
    drawtmp.text((0, 0), string, font=font, fill=0)
    rotated = imtmp.rotate(angle, expand=1)
    width, height = rotated.size
    imageObject.paste(rotated, (x-(width/2), y-(height/2)))


'''
The center text function draws text with the center coordinate provided
INPUTS:
    drawObject: the object to draw on
    string: the text to write
    x: x-coordinate of center
    y: y-coordinate of center
'''
def centerText(drawObject, string, fontSize, x, y):
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', fontSize)
    width = font.getsize(string)[0]
    drawObject.text((x-(width/2), y-(fontSize/2)), string, font=font, fill=0)


'''
The centerRectangle function draws a rectangle given a size and center coordinates
INPUTS:
	drawObject: object to draw on
	size: size of the rectangle to make (side length)
	x: center x-coordinate
	y: center y-coordinate
'''
def centerRectangle(drawObject, size, x, y):
	drawObject.rectangle((x-(size/2), y+(size/2), x+(size/2), y-(size/2)), fill=0)
