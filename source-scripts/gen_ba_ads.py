#!/usr/bin/env python3
"""Before/after aligner ads + full suite contact sheet."""
from PIL import Image, ImageDraw, ImageFont, ImageOps

W = H = 1080
GREEN=(40,96,80); INK=(18,51,43); SALM=(221,160,144); SALMD=(206,130,112)
CREAM=(250,246,241); LINE=(229,222,213); WHITE=(255,255,255); MUT=(95,114,104)
FR='/home/claude/fonts/Fraunces.ttf'; IN='/home/claude/fonts/Inter.ttf'
IMG='/home/claude/happy-teeth-landing/images/'; OUT='/home/claude/happy-teeth-landing/ads/'

def fraunces(size,wght=560):
    f=ImageFont.truetype(FR,size)
    try: f.set_variation_by_axes([0.0,0.0,144.0,wght])
    except Exception: pass
    return f
def inter(size,wght=500):
    f=ImageFont.truetype(IN,size)
    try: f.set_variation_by_axes([28.0,wght])
    except Exception: pass
    return f
def rrect(d,xy,r,fill=None,outline=None,width=1): d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=width)
def tw(d,t,f): return d.textlength(t,font=f)
def ct(d,cx,y,t,f,fill): d.text((cx-tw(d,t,f)/2,y),t,font=f,fill=fill)
def pill(d,cx,cy,t,f,fg,bg,padx=44,pady=26):
    w=tw(d,t,f); asc,desc=f.getmetrics(); th=asc+desc
    rrect(d,(cx-w/2-padx,cy-th/2-pady,cx+w/2+padx,cy+th/2+pady),(th+2*pady)/2,fill=bg)
    d.text((cx-w/2,cy-th/2+2),t,font=f,fill=fg)
def photo(cv,path,box,r=30,cy=0.5,cx=0.5,zoom=1.0):
    x0,y0,x1,y1=box; bw,bh=x1-x0,y1-y0
    im=ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    if zoom>1.0:
        iw,ih=im.size; cw,chh=iw/zoom,ih/zoom
        left=max(0,min(iw-cw,cx*iw-cw/2)); top=max(0,min(ih-chh,cy*ih-chh/2))
        im=im.crop((int(left),int(top),int(left+cw),int(top+chh)))
    im=ImageOps.fit(im,(bw,bh),Image.LANCZOS,centering=(cx,cy))
    m=Image.new('L',(bw,bh),0); ImageDraw.Draw(m).rounded_rectangle((0,0,bw,bh),r,fill=255)
    cv.paste(im,(x0,y0),m)
def tagpill(cv,d,x,y,t,after=False):
    f=inter(24,800); w=tw(d,t,f)
    ov=Image.new('RGBA',cv.size,(0,0,0,0)); od=ImageDraw.Draw(ov)
    bg=(206,130,112,240) if after else (18,51,43,225)
    rrect(od,(x,y,x+w+40,y+52),26,fill=bg)
    od.text((x+20,y+11),t,font=f,fill=WHITE)
    cv.alpha_composite(ov)
def base(bg):
    im=Image.new('RGBA',(W,H),bg+(255,)); return im,ImageDraw.Draw(im)

D1="*Equivalent weekly cost via MediPay payment plan; repayments fortnightly. Approval, eligibility & T&Cs apply."
D2="Genuine patient treated with clear aligners by Dr Mary Liu, AHPRA Reg. DEN0000958393; individual results vary."

def disc2(d,y,fill,size=19):
    ct(d,W/2,y,D1,inter(size,500),fill); ct(d,W/2,y+28,D2,inter(size,500),fill)

# ---- ALIGNERS 6: smile-only before/after (cream)
def results_featured():
    im,d=base(CREAM)
    ct(d,W/2,46,'R E A L   A L I G N E R   R E S U L T S',inter(24,700),SALMD)
    ct(d,W/2,84,'Real smiles by',fraunces(68,560),GREEN)
    ct(d,W/2,164,'Dr Mary Liu.',fraunces(68,480),SALMD)
    photo(im,IMG+'wide-displaced-before.jpg',(140,278,530,782),r=28)
    photo(im,IMG+'wide-displaced-after.jpg',(550,278,940,782),r=28)
    tagpill(im,d,160,298,'BEFORE'); tagpill(im,d,570,298,'AFTER',after=True)
    d=ImageDraw.Draw(im)
    ct(d,W/2,818,'A displaced side tooth guided into line with clear aligners.',inter(30,600),(33,61,51))
    ct(d,W/2,862,'From $59 per week* with MediPay.',inter(28,500),MUT)
    pill(d,W/2,942,'Book Your FREE Consultation',inter(35,800),WHITE,GREEN,pady=21)
    disc2(d,1008,(155,148,138),size=18)
    return im

# ---- ALIGNERS 7: smile-only before/after pair (green)
def results_pair():
    im,d=base(GREEN)
    ct(d,W/2,56,'C L E A R   A L I G N E R S   ·   S P R I N G W O O D',inter(24,700),SALM)
    ct(d,W/2,104,'Straightened,',fraunces(78,560),WHITE)
    ct(d,W/2,198,'invisibly.',fraunces(78,480),SALM)
    photo(im,IMG+'wide-flared-before.jpg',(70,362,530,615),r=28)
    photo(im,IMG+'wide-flared-after.jpg',(550,362,1010,615),r=28)
    tagpill(im,d,160,298,'BEFORE'); tagpill(im,d,570,298,'AFTER',after=True)
    d=ImageDraw.Draw(im)
    ct(d,W/2,668,'Flared front teeth gently aligned — no braces needed.',inter(31,600),WHITE)
    ct(d,W/2,716,'From $59 per week* with MediPay.',inter(29,500),(200,220,211))
    pill(d,W/2,812,'Book Your FREE Consultation',inter(36,800),WHITE,SALMD)
    disc2(d,930,(150,180,168))
    return im

results_featured().convert('RGB').save(OUT+'aligners-ad-6-results.png','PNG')
results_pair().convert('RGB').save(OUT+'aligners-ad-7-before-after.png','PNG')
print('saved 6 & 7')

# ---- FULL SUITE SHEET
names=[('implants-ad-1-offer.png','Implants · Offer'),('implants-ad-2-photo.png','Implants · Frontage'),
       ('implants-ad-3-benefits.png','Implants · Benefits'),('implants-ad-4-dr-allan.png','Implants · Dr Allan'),
       ('implants-ad-5-implant-team.png','Implants · Duo'),('aligners-ad-1-offer.png','Aligners · Offer'),
       ('aligners-ad-2-photo.png','Aligners · Frontage'),('aligners-ad-3-benefits.png','Aligners · Benefits'),
       ('aligners-ad-4-dr-mary.png','Aligners · Dr Mary'),('aligners-ad-5-mary-green.png','Aligners · Dr Mary II'),
       ('aligners-ad-6-results.png','Aligners · Results'),('aligners-ad-7-before-after.png','Aligners · Before/After')]
cols,tile,gap,label_h=4,440,26,54
rows=3
sw=gap+cols*(tile+gap); sh=110+rows*(tile+label_h+gap)
sheet=Image.new('RGB',(sw,sh),(250,246,241)); sd=ImageDraw.Draw(sheet)
sd.text((gap, 30),'Happy Teeth Springwood — Meta Ads Suite',font=fraunces(46,560),fill=GREEN)
lf=inter(22,700)
for i,(n,lab) in enumerate(names):
    x=gap+(i%cols)*(tile+gap); y=110+(i//cols)*(tile+label_h+gap)
    sheet.paste(Image.open(OUT+n).resize((tile,tile),Image.LANCZOS),(x,y))
    sd.text((x, y+tile+12),lab,font=lf,fill=(95,114,104))
sheet.save(OUT+'happy-teeth-ads-suite.png')
print('suite sheet saved', sheet.size)
