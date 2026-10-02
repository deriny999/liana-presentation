from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
im=Image.open('slide4-source.jpeg').convert('RGB')
a=np.array(im).astype(np.float32)
x1,y1,x2,y2=192,532,510,646
# Bilinear reconstruction from clean card colors sampled near the four corners.
c00=np.array(im.getpixel((192,535)),float); c10=np.array(im.getpixel((510,535)),float)
c01=np.array(im.getpixel((192,642)),float); c11=np.array(im.getpixel((510,642)),float)
H,W=y2-y1,x2-x1
patch=np.zeros((H,W,3),np.float32)
for yy in range(H):
    v=yy/max(1,H-1)
    left=c00*(1-v)+c01*v; right=c10*(1-v)+c11*v
    for xx in range(W):
        u=xx/max(1,W-1)
        patch[yy,xx]=left*(1-u)+right*u
base=Image.fromarray(np.clip(a,0,255).astype(np.uint8))
pat=Image.fromarray(np.clip(patch,0,255).astype(np.uint8))
mask=Image.new('L',(W,H),255)
# Feather only rectangle edges for a seamless blend.
md=ImageDraw.Draw(mask); md.rectangle((0,0,W-1,H-1),fill=255)
mask=mask.filter(ImageFilter.GaussianBlur(6))
base.paste(pat,(x1,y1),mask)
d=ImageDraw.Draw(base)
color=(137,55,42)
fb=ImageFont.truetype(r'C:\Windows\Fonts\times.ttf',96)
fs=ImageFont.truetype(r'C:\Windows\Fonts\times.ttf',69)
x,y=202,548
d.text((x,y),'-39',font=fb,fill=color)
b=d.textbbox((x,y),'-39',font=fb)
d.text((b[2]+12,571),'кг',font=fs,fill=color)
base.save('slide4-updated.jpg',quality=97,subsampling=0)
base.crop((150,500,540,690)).save('slide4-updated-crop.png')
