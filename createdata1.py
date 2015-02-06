'''
1) Takes as input and image, box location, box size, a rotation angle, a
perspective angle, a piece of text, font information (name, bold/italic,
color/color gradient, alpha value)

2) Creates text in the specified font, color, alpha level, etc and fits
it into the box size then performs the rotation and perspective on the
text then sticks that on top of the input image at the specified location.

3) Any other image transforms (like embossing, light source, etc) would
be good to include as parameters.

4) outputs 3 things: the modified image, the text, and an image of the
text (black color, no alpha), with the location of where this text is in
the image.
'''

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
import re, sys
import xml.etree.ElementTree as ET

im=None
wm=None
transparent = (0,0,0,0)

def iniateImage(imageloc):
	global im
	global wm
	im = Image.open(imageloc).convert('RGBA') 
	wm = Image.new('RGBA',im.size,transparent)
	
def processImage(xmltext,imageloc):
	#get the parameters
	global im
	global wm
	boxloc=tuple([int(x) for x in xmltext.find('boxloc').text[1:-1].split(",")])
	rotangle=int(xmltext.find('rotangle').text)
	perspectangle=[int(x) for x in xmltext.find('perspectangle').text[1:-1].split(',')]
	text=xmltext.find('text').text
	fontloc=xmltext.find('fontloc').text
	fontsize=int(xmltext.find('fontsize').text)
	color=tuple([int(x) for x in xmltext.find('color').text[1:-1].split(',')])
	alphavalue=float(xmltext.find('alphavalue').text)

	#use the parameters for creating a new image	
	opacity=alphavalue	
	font = ImageFont.truetype(fontloc,fontsize)
	draw = ImageDraw.Draw(wm)
	w,h = draw.textsize(text,font)
	wm = Image.new('RGBA',(w,h),transparent)
	draw = ImageDraw.Draw(wm)
	draw.text((0,0),text,color,font)
	wm=wm.rotate(rotangle,expand=1)		
	en = ImageEnhance.Brightness(wm)
	mask = en.enhance(1-opacity)
	im.paste(wm,boxloc,mask)
	im.show()

	#print boxloc,rotangle,perspectangle,text,fontloc,fontsize,color,alphavalue


		
def processXML():
	tree = ET.parse('config.xml')
	root = tree.getroot()
	global im
	global wm
	for child in root:
		imageloc=child.find('imageloc').text
		texts=child.findall('text')
		iniateImage(imageloc)
		for text in texts:
			processImage(text,imageloc)
		#saveImage(imageloc)
		im=None
		wm=None
		print "image",imageloc,"processed" 
		
def main():
	processXML()
	
if __name__=='__main__':
	main()
			

