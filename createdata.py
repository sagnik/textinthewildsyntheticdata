from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageEnhance
import re, sys
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

DEBUG=False
#inputs
if DEBUG:
	imageloc="oldmain.jpg"
	boxloc=(300,300)
	rotangle=45
	perspectangle=[10,12,13,14,15,16,17,18]
	text="Hello World"
	fontloc='verdana.ttf'
	color=(255,0,0)
	alphavalue=0.5

else:
	string=open(sys.argv[1]).read()
	imageloc=re.findall('<imageloc>(.*?)</imageloc>', string, re.DOTALL)[0]
	boxloc=tuple([int(x) for x in re.findall('<boxloc>(.*?)</boxloc>', string, re.DOTALL)[0][1:-1].split(",")])
	rotangle=int(re.findall('<rotangle>(.*?)</rotangle>', string, re.DOTALL)[0])
	perspectangle=[int(x) for x in re.findall('<perspectangle>(.*?)</perspectangle>', string, re.DOTALL)[0][1:-1].split(',')]
	text=re.findall('<text>(.*?)</text>', string, re.DOTALL)[0]
	fontloc=re.findall('fontloc>(.*?)</fontloc>', string, re.DOTALL)[0]
	fontsize=int(re.findall('<fontsize>(.*?)</fontsize>', string, re.DOTALL)[0])
	color=tuple([int(x) for x in re.findall('<color>(.*?)</color>', string, re.DOTALL)[0][1:-1].split(',')])
	alphavalue=float(re.findall('<alphavalue>(.*?)</alphavalue>', string, re.DOTALL)[0])
	colorimsave=re.findall('<colorimsave>(.*?)</colorimsave>', string, re.DOTALL)[0]
	bwimsave=re.findall('<bwimsave>(.*?)</bwimsave>', string, re.DOTALL)[0]

opacity=alphavalue
transparent = (0,0,0,0)

font = ImageFont.truetype(fontloc,fontsize)
im = Image.open(imageloc).convert('RGBA') 
wm = Image.new('RGBA',im.size,transparent)
draw = ImageDraw.Draw(wm)
w,h = draw.textsize(text,font)
wm = Image.new('RGBA',(w,h),transparent)
draw = ImageDraw.Draw(wm)
draw.text((0,0),text,color,font)
wm=wm.rotate(rotangle,expand=1)
#wm.show()
#print w,h
en = ImageEnhance.Brightness(wm)
mask = en.enhance(1-opacity)
im.paste(wm,boxloc,mask)
im.show()



im.save(colorimsave)
im.save(bwimsave)


'''
boxsize, not font size, before rotation and perspective change
noise, 
engraving
embossing
letter based rotation\
'''

