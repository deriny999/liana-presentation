import fitz, os
src='presentation.pdf'
out='presentation-new.pdf'
d=fitz.open(src)
p=d[3]
imgs=p.get_images(full=True)
if not imgs:
    raise SystemExit('No image on page 4')
xref=imgs[0][0]
p.replace_image(xref, filename='slide4-updated.jpg')
d.save(out, garbage=4, deflate=True)
d.close()
os.replace(out,src)
print('updated', os.path.getsize(src))
