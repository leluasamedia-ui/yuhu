import sys
from PIL import Image, ImageDraw
out=sys.argv[1]; SS=4; N=256*SS
def hx(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)
LINE=hx('#0A0D14'); LIGHT=hx('#6C7A92'); MID=hx('#444F63'); DARK=hx('#2A3140')
YEL=hx('#F5C21B'); BLK=hx('#15171C')
im=Image.new('RGBA',(N,N),DARK); d=ImageDraw.Draw(im)
# beveled steel plate, full bleed (no transparent corners -> continuous wall)
b=22*SS
d.polygon([(0,0),(N,0),(N-b,b),(b,b)],fill=LIGHT)
d.polygon([(0,0),(b,b),(b,N-b),(0,N)],fill=LIGHT)
d.polygon([(N,0),(N,N),(N-b,N-b),(N-b,b)],fill=DARK)
d.polygon([(0,N),(b,N-b),(N-b,N-b),(N,N)],fill=DARK)
d.rectangle([b,b,N-b,N-b],fill=MID)
# hazard stripe window
w0,w1=60*SS,N-60*SS
win=Image.new('RGBA',(N,N),(0,0,0,0)); wd=ImageDraw.Draw(win)
wd.rectangle([w0,w0,w1,w1],fill=YEL)
per=44*SS
for k in range(-12,14):
    x=w0+k*per
    wd.polygon([(x,w1),(x+per//2,w1),(x+per//2+(w1-w0),w0),(x+(w1-w0),w0)],fill=BLK)
mask=Image.new('L',(N,N),0); ImageDraw.Draw(mask).rectangle([w0,w0,w1,w1],fill=255)
im.paste(win,(0,0),mask)
d.rectangle([w0,w0,w1,w1],outline=LINE,width=7*SS)
d.line([(w0,w1+3*SS),(w1,w1+3*SS)],fill=hx('#1B2130'),width=3*SS)
# rivets
for cx,cy in [(41,41),(215,41),(41,215),(215,215)]:
    r=9*SS; x,y=cx*SS,cy*SS
    d.ellipse([x-r-2*SS,y-r-2*SS,x+r+2*SS,y+r+2*SS],fill=LINE)
    d.ellipse([x-r,y-r,x+r,y+r],fill=hx('#9AA6BA'))
    d.ellipse([x-r//2-SS,y-r//2-SS,x+r//2-SS,y+r//2-SS],fill=hx('#D5DDEA'))
# outer outline
d.rectangle([0,0,N-1,N-1],outline=LINE,width=5*SS)
im.resize((256,256),Image.LANCZOS).save(f'{out}/border_barrier.png')
