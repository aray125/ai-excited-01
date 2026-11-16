import os, struct, zlib, random, math

W=H=1024; random.seed(17)
bg=(12,25,58); pix=bytearray(bg*(W*H))
def setp(x,y,c):
    x=int(x); y=int(y)
    if 0<=x<W and 0<=y<H:
        i=(y*W+x)*3; pix[i:i+3]=bytes(c)
def line(x0,y0,x1,y1,c,w=3):
    dx=x1-x0; dy=y1-y0; n=max(1,int(max(abs(dx),abs(dy))))
    r=max(1,w//2)
    for k in range(n+1):
        x=x0+dx*k/n; y=y0+dy*k/n
        for yy in range(int(y-r),int(y+r+1)):
            for xx in range(int(x-r),int(x+r+1)):
                if (xx-x)**2+(yy-y)**2<=r*r: setp(xx,yy,c)
def poly(points,c,outline=None,ow=3):
    ys=[p[1] for p in points]; y0=max(0,int(min(ys))); y1=min(H-1,int(max(ys)))
    for y in range(y0,y1+1):
        xs=[]
        for (x1,yy1),(x2,yy2) in zip(points,points[1:]+points[:1]):
            if (yy1<=y<yy2) or (yy2<=y<yy1): xs.append(x1+(y-yy1)*(x2-x1)/(yy2-yy1))
        xs.sort()
        for a,b in zip(xs[::2],xs[1::2]):
            for x in range(int(a),int(b)+1): setp(x,y,c)
    if outline:
        for a,b in zip(points,points[1:]+points[:1]): line(*a,*b,outline,ow)
def circle(cx,cy,r,c):
    for y in range(int(cy-r),int(cy+r+1)):
        for x in range(int(cx-r),int(cx+r+1)):
            if (x-cx)**2+(y-cy)**2<=r*r:setp(x,y,c)
def rot(p,ang,ctr=(512,500)):
    x,y=p; cx,cy=ctr; q=math.radians(ang); return (cx+(x-cx)*math.cos(q)-(y-cy)*math.sin(q),cy+(x-cx)*math.sin(q)+(y-cy)*math.cos(q))
ink=(9,16,39); gold=(244,187,44); teal=(16,177,177); foam=(220,255,245); mag=(238,42,139); cyan=(63,224,244); yellow=(255,221,57); silver=(190,204,214)
# directional rays
for a in range(0,360,15):
    r=730; x=512+math.cos(math.radians(a))*r; y=485+math.sin(math.radians(a))*r
    line(512,485,x,y,(28,53,105),7)
# colored directional light shards
for points,col in [([(510,540),(65,340),(130,305)],mag), ([(510,540),(920,390),(950,430)],cyan), ([(510,540),(310,75),(370,105)],yellow), ([(510,540),(840,970),(795,950)],mag)]:
    poly(points,col)
# tilted golden frame
outer=[rot(p, -8) for p in [(185,210),(850,210),(850,790),(185,790)]]; inner=[rot(p,-8) for p in [(245,270),(790,270),(790,720),(245,720)]]
poly(outer,gold,ink,12); poly(inner,ink,ink,8); poly([rot(p,-8) for p in [(260,285),(775,285),(775,700),(260,700)]],(39,117,151),ink,5)
# seascape inside
poly([rot(p,-8) for p in [(260,570),(775,570),(775,700),(260,700)]],(20,120,168),None)
circle(*rot((650,360),-8),58,(255,216,72))
for off in [0,42,86]:
    pts=[rot((270,560+off),-8)]+[rot((350+i*70,545+off+18*math.sin(i)), -8) for i in range(7)]+[rot((775,590+off),-8)]
    line(*pts[0],*pts[1],foam,6)
    for a,b in zip(pts[1:],pts[2:]): line(*a,*b,foam,6)
# rivets
for p in [(220,245),(810,245),(220,755),(810,755)]: circle(*rot(p,-8),12,(255,220,92)); circle(*rot(p,-8),5,ink)
# giant wave bursting out
wave=[(170,770),(245,590),(360,500),(510,470),(650,505),(810,620),(900,790),(790,850),(580,810),(400,850)]
poly(wave,teal,ink,14)
poly([(360,545),(470,475),(585,490),(670,550),(600,560),(500,530),(420,585)],foam,ink,8)
for i in range(22):
    x=260+random.randrange(560); y=560+random.randrange(240); line(x,y,x+random.randrange(-35,35),y-random.randrange(20,90),foam,random.randrange(3,8))
# curling lip: the darker hollow makes the breaking crest read at thumbnail size
poly([(190,724),(260,591),(350,514),(410,497),(465,511),(479,545),(457,576),(418,581),(394,565),(411,544),(438,548),(421,529),(387,539),(334,593),(302,662),(280,708)],foam,ink,7)
line(321,620,285,708,cyan,8)
# spray
for i in range(35):
    x=300+random.randrange(430); y=430+random.randrange(170); circle(x,y,random.randrange(3,10),foam)
# rocket board
board=[(300,760),(720,760),(820,800),(720,835),(300,820),(245,790)]
poly(board,yellow,ink,12); line(320,780,720,780,mag,8); line(370,810,700,810,cyan,7)
poly([(510,785),(560,785),(540,820),(520,820)],mag,ink,4)
for x in [330,380,680,730]: line(x,770,x+25,820,ink,5)
# flame
poly([(285,800),(180,825),(245,850),(205,900),(330,840)],mag,ink,9); poly([(270,815),(210,835),(260,845)],yellow,ink,5)
for i in range(16): circle(170+random.randrange(150),820+random.randrange(100),random.randrange(3,8),yellow)
# robot legs/body
line(470,700,450,770,ink,22); line(560,700,585,770,ink,22); line(470,700,450,770,silver,12); line(560,700,585,770,silver,12)
poly([(430,550),(585,550),(610,700),(450,700)],mag,ink,12); circle(510,520,88,silver); circle(510,520,62,cyan); line(455,520,565,520,ink,8)
for x in [470,550]: circle(x,510,9,ink)
# raised arms, articulated hands, antenna and chest badge
line(445,590,390,540,ink,25); line(390,540,365,485,ink,25)
line(445,590,390,540,silver,14); line(390,540,365,485,silver,14)
circle(365,480,18,ink); circle(365,480,11,silver)
line(585,590,640,560,ink,25); line(640,560,665,505,ink,25)
line(585,590,640,560,silver,14); line(640,560,665,505,silver,14)
circle(665,500,18,ink); circle(665,500,11,silver)
line(510,435,510,412,ink,9); circle(510,405,12,mag)
circle(520,642,24,ink); poly([(524,619),(506,644),(521,644),(513,664),(536,637),(522,637)],yellow)
# scarf fluttering
poly([(450,580),(350,555),(250,610),(360,650),(470,620)],mag,ink,10); line(430,585,350,615,cyan,8)
# speech bubble
bub=[(585,170),(910,170),(950,230),(920,350),(720,370),(650,440),(660,350),(575,330)]
poly(bub,(250,250,235),ink,10)
# 5x7 font
FONT={'W':['10001','10001','10101','10101','10101','11011','10001'],'O':['01110','10001','10001','10001','10001','10001','01110'],'J':['00111','00010','00010','00010','10010','10010','01100'],'D':['11110','10001','10001','10001','10001','10001','11110'],'G':['01110','10001','10000','10111','10001','10001','01110'],'E':['11111','10000','10000','11110','10000','10000','11111'],'!':['00100','00100','00100','00100','00100','00000','00100'],',':['00000','00000','00000','00000','00110','00100','01000'],' ':['00000']*7}
def text(s,x,y,scale=12,c=ink):
    for ch in s:
        pat=FONT.get(ch,FONT[' '])
        for yy,row in enumerate(pat):
            for xx,v in enumerate(row):
                if v=='1':
                    for dy in range(scale):
                        for dx in range(scale): setp(x+xx*scale+dx,y+yy*scale+dy,c)
        x+=6*scale
text('WOW,',625,200,12,mag); text('JUDGE!',630,282,8,ink)
# confetti and sparkles
for i in range(55):
    x=random.randrange(40,980); y=random.randrange(40,960); col=random.choice([mag,yellow,cyan,foam]); line(x,y,x+random.randrange(-10,11),y+random.randrange(8,24),col,4)
for x,y in [(90,180),(930,120),(110,880),(900,900),(760,460)]:
    poly([(x,y-25),(x+6,y-6),(x+25,y),(x+6,y+6),(x,y+25),(x-6,y+6),(x-25,y),(x-6,y-6)],yellow); circle(x,y,4,foam)
def png(path):
    raw=b''.join(b'\0'+bytes(pix[y*W*3:(y+1)*W*3]) for y in range(H))
    def chunk(t,d): return struct.pack('>I',len(d))+t+d+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
    data=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',W,H,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
    open(path,'wb').write(data)
out=os.environ.get('MAKEFUN_OUTPUT_DIR','/output'); os.makedirs(out,exist_ok=True); png(os.path.join(out,'ai-excited-01.png'))
