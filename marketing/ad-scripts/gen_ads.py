#!/usr/bin/env python3
"""Happy Teeth Springwood — Meta ad set (3 per service), 1080x1080."""
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter
import os

W = H = 1080
GREEN = (40, 96, 80)        # #286050
INK   = (18, 51, 43)        # #12332B
DEEP  = (27, 69, 58)        # #1B453A
SALM  = (221, 160, 144)     # #DDA090
GOLD  = (164, 125, 80); GOLDD = (138, 103, 64)
SALMD = (206, 130, 112)     # #CE8270
CREAM = (250, 246, 241)     # #FAF6F1
LINE  = (229, 222, 213)
WHITE = (255, 255, 255)

FR = '/home/claude/fonts/Fraunces.ttf'
IN = '/home/claude/fonts/Inter.ttf'
UP = '/mnt/user-data/uploads/'
IMG = '/home/claude/happy-teeth-landing/images/'
OUT = '/home/claude/happy-teeth-landing/ads/'

def fraunces(size, wght=560, ital=False):
    f = ImageFont.truetype(FR, size)
    try: f.set_variation_by_axes([0.0, 0.0, 144.0, wght])  # SOFT, WONK, opsz, wght
    except Exception: pass
    return f

def inter(size, wght=500):
    f = ImageFont.truetype(IN, size)
    try: f.set_variation_by_axes([28.0, wght])  # opsz, wght
    except Exception: pass
    return f

def rrect(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def text_w(d, t, f):
    return d.textlength(t, font=f)

def center_text(d, cx, y, t, f, fill):
    d.text((cx - text_w(d, t, f)/2, y), t, font=f, fill=fill)

def pill(d, cx, cy, t, f, fg, bg, padx=44, pady=26, outline=None):
    w = text_w(d, t, f); asc, desc = f.getmetrics()
    th = asc + desc
    x0, y0 = cx - w/2 - padx, cy - th/2 - pady
    x1, y1 = cx + w/2 + padx, cy + th/2 + pady
    rrect(d, (x0, y0, x1, y1), (y1-y0)/2, fill=bg, outline=outline, width=3)
    d.text((cx - w/2, cy - th/2 + 2), t, font=f, fill=fg)
    return (x0, y0, x1, y1)

def wainscot(d, alpha_col, y0, y1, cols=3, m=70, gap=26, r=14, width=3):
    cw = (W - 2*m - (cols-1)*gap) / cols
    for i in range(cols):
        x = m + i*(cw+gap)
        rrect(d, (x, y0, x+cw, y1), r, outline=alpha_col, width=width)
        rrect(d, (x+16, y0+16, x+cw-16, y1-16), r-6, outline=alpha_col, width=2)

def load_logo_on_green(target_w):
    lg = Image.open(UP + 'logo-combined-B-I0u10U.png').convert('RGBA')
    sc = target_w / lg.width
    return lg.resize((target_w, int(lg.height*sc)), Image.LANCZOS)

def logo_chip(canvas, cx, y, lw=330):
    """logo inside a green rounded chip (for light backgrounds)"""
    lg = load_logo_on_green(lw)
    pad = 26
    chip = Image.new('RGBA', (lg.width + pad*2, lg.height + pad*2), (0,0,0,0))
    cd = ImageDraw.Draw(chip)
    rrect(cd, (0,0,chip.width-1,chip.height-1), 30, fill=GREEN+(255,))
    chip.alpha_composite(lg, (pad, pad))
    canvas.alpha_composite(chip, (int(cx - chip.width/2), y))
    return y + chip.height

def photo_panel(canvas, path, box, r=34, darken=0.0, CENTERY=0.42, CENTERX=0.5):
    x0, y0, x1, y1 = box
    bw, bh = x1-x0, y1-y0
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    im = ImageOps.fit(im, (bw, bh), Image.LANCZOS, centering=(CENTERX, CENTERY))
    if darken:
        ov = Image.new('RGB', im.size, INK)
        im = Image.blend(im, ov, darken)
    mask = Image.new('L', (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0,0,bw,bh), r, fill=255)
    canvas.paste(im, (x0, y0), mask)

def tick_row(canvas, d, x, cy, t, f, fg, tick_bg=SALM, tick_fg=INK, r=21):
    d.ellipse((x, cy-r, x+2*r, cy+r), fill=tick_bg)
    tf = inter(26, 800)
    d.text((x+r - text_w(d, '✓', tf)/2, cy - 16), '✓', font=tf, fill=tick_fg)
    asc, desc = f.getmetrics()
    d.text((x + 2*r + 24, cy - (asc+desc)/2 + 2), t, font=f, fill=fg)

def base(bg):
    im = Image.new('RGBA', (W, H), bg + (255,))
    return im, ImageDraw.Draw(im)

def disclaimer(d, lines, y, fill, size=21):
    f = inter(size, 500)
    for i, t in enumerate(lines):
        center_text(d, W/2, y + i*30, t, f, fill)

DISC_MEDIPAY = "*Equivalent weekly cost via MediPay payment plan; repayments fortnightly. Approval, eligibility & T&Cs apply."

# ---------------------------------------------------------------- IMPLANTS 1: offer hero (green)
def implants_offer():
    im, d = base(GREEN)
    lg = load_logo_on_green(360)
    im.alpha_composite(lg, (int(W/2 - lg.width/2), 66))
    center_text(d, W/2, 218, 'S P R I N G W O O D  ·  F R E E  C O N S U L T A T I O N', inter(24, 700), GOLD)
    center_text(d, W/2, 292, 'Dental Implants', fraunces(96, 560), WHITE)
    center_text(d, W/2, 408, 'from', inter(34, 600), (207, 224, 216))
    # monumental price
    f_big = fraunces(230, 620)
    t = '$39'
    tw = text_w(d, t, f_big)
    unit_f = fraunces(52, 480)
    unit = 'per week*'
    uw = text_w(d, unit, unit_f)
    total = tw + 28 + uw
    x0 = W/2 - total/2
    d.text((x0, 430), t, font=f_big, fill=GOLD)
    d.text((x0 + tw + 28, 430 + 176), unit, font=unit_f, fill=WHITE)
    pill(d, W/2, 768, 'Book Your FREE Consultation', inter(38, 800), WHITE, GOLDD)
    d.line((W/2-210, 856, W/2+210, 856), fill=(58,116,98), width=2)
    center_text(d, W/2, 880, 'Single implants  ·  Multiple teeth  ·  All-on-X full arch', inter(30, 600), WHITE)
    center_text(d, W/2, 934, 'MediPay plans  ·  Access-your-super options  ·  Aftercare included', inter(26, 500), (183, 208, 198))
    disclaimer(d, [DISC_MEDIPAY], 1014, (150, 180, 168))
    return im

# ---------------------------------------------------------------- IMPLANTS 2: photo card (surgery)
def implants_photo():
    im, d = base(CREAM)
    photo_panel(im, IMG + 'shopfront.jpg', (50, 50, 1030, 600), r=38, darken=0.05, CENTERY=0.5, CENTERX=0.3)
    # floating price chip on photo
    chip_f = fraunces(56, 620)
    pill(d, 860, 118, 'from $39/wk*', inter(34, 800), INK, GOLD)
    # panel below
    center_text(d, W/2, 646, 'Missing or failing teeth?', fraunces(76, 560), GREEN)
    center_text(d, W/2, 744, 'Eat, speak and smile with confidence again —', inter(33, 500), (95, 114, 104))
    center_text(d, W/2, 788, 'with fixed, natural-looking dental implants in Springwood.', inter(33, 500), (95, 114, 104))
    pill(d, W/2, 916, 'Book Your FREE Consultation', inter(38, 800), WHITE, GREEN)
    disclaimer(d, [DISC_MEDIPAY], 1012, (155, 148, 138))
    return im

# ---------------------------------------------------------------- IMPLANTS 3: benefits checklist
def implants_benefits():
    im, d = base(INK)
    # inner panel
    rrect(d, (46, 46, 1034, 1034), 40, outline=(58,116,98), width=3)
    lg = load_logo_on_green(300)
    im.alpha_composite(lg, (int(W/2 - lg.width/2), 92))
    center_text(d, W/2, 226, 'A L L - O N - X   &   D E N T A L   I M P L A N T S', inter(24, 700), GOLD)
    center_text(d, W/2, 282, 'A fixed new smile,', fraunces(84, 560), WHITE)
    center_text(d, W/2, 384, 'made affordable.', fraunces(84, 480), GOLD)
    ticks = ['Eat the foods you love again',
             'Helps prevent jawbone loss',
             'A full arch on as few as 4 implants',
             'From $39 per week* with MediPay']
    ty = 560
    tf = inter(37, 600)
    for i, t in enumerate(ticks):
        tick_row(im, d, 190, ty + i*84, t, tf, WHITE)
    pill(d, W/2, 942, 'Claim Your FREE Consultation', inter(38, 800), WHITE, GOLDD)
    disclaimer(d, [DISC_MEDIPAY], 1000, (150, 180, 168), size=19)
    return im

# ---------------------------------------------------------------- ALIGNERS 1: offer hero (cream)
def aligners_offer():
    im, d = base(CREAM)
    logo_chip(im, W/2, 62, lw=300)
    center_text(d, W/2, 232, 'S P R I N G W O O D  ·  F R E E  C O N S U L T A T I O N', inter(24, 700), SALMD)
    center_text(d, W/2, 296, 'Straighten your teeth.', fraunces(88, 560), GREEN)
    # italic accent
    f_it = fraunces(88, 520)
    center_text(d, W/2, 400, 'Skip the braces.', f_it, SALMD)
    # aligner arcs motif
    for i, (op, yy) in enumerate([(70, 545), (130, 585), (255, 625)]):
        col = (40, 96, 80, op)
        ov = Image.new('RGBA', (W, H), (0,0,0,0))
        od = ImageDraw.Draw(ov)
        od.arc((290, yy, 790, yy+320), 200, 340, fill=col, width=16)
        im.alpha_composite(ov)
    # price chip
    f_price = fraunces(120, 620)
    t = '$59'
    tw = text_w(d, t, f_price)
    unit_f = fraunces(44, 480); unit = 'per week*'
    uw = text_w(d, unit, unit_f)
    total = tw + 22 + uw
    x0 = W/2 - total/2
    d.text((x0, 690), t, font=f_price, fill=GREEN)
    d.text((x0 + tw + 22, 690 + 86), unit, font=unit_f, fill=(95,114,104))
    pill(d, W/2, 918, 'Book Your FREE Consultation', inter(38, 800), WHITE, GREEN)
    disclaimer(d, [DISC_MEDIPAY], 1014, (155, 148, 138))
    return im

# ---------------------------------------------------------------- ALIGNERS 2: photo card (reception)
def aligners_photo():
    im, d = base(GREEN)
    photo_panel(im, IMG + 'shopfront.jpg', (50, 50, 1030, 560), r=38, darken=0.06, CENTERY=0.5)
    pill(d, 858, 118, 'from $59/wk*', inter(34, 800), INK, SALM)
    center_text(d, W/2, 606, 'Clear Aligners', fraunces(92, 560), WHITE)
    center_text(d, W/2, 718, 'Nearly invisible. Removable. No metal.', inter(35, 600), SALM)
    center_text(d, W/2, 776, 'Guided by our Springwood dentists from first scan to final smile.', inter(29, 500), (200, 220, 211))
    pill(d, W/2, 902, 'Book Your FREE Consultation', inter(38, 800), WHITE, SALMD)
    disclaimer(d, [DISC_MEDIPAY], 1006, (168, 195, 184))
    return im

# ---------------------------------------------------------------- ALIGNERS 3: checklist
def aligners_benefits():
    im, d = base(CREAM)
    rrect(d, (46, 46, 1034, 1034), 40, outline=LINE, width=3)
    logo_chip(im, W/2, 88, lw=290)
    center_text(d, W/2, 250, 'C L E A R   A L I G N E R S   ·   S P R I N G W O O D', inter(24, 700), SALMD)
    center_text(d, W/2, 306, 'Your smile,', fraunces(84, 560), GREEN)
    center_text(d, W/2, 406, 'discreetly straightened.', fraunces(84, 480), SALMD)
    ticks = ['Nearly invisible — most won\u2019t notice',
             'Removable for eating & brushing',
             'Digital scan & smile preview first',
             'From $59 per week* with MediPay']
    ty = 574
    tf = inter(37, 600)
    for i, t in enumerate(ticks):
        tick_row(im, d, 190, ty + i*84, t, tf, (33, 61, 51), tick_bg=GREEN, tick_fg=WHITE)
    pill(d, W/2, 942, 'Book Your FREE Consultation', inter(38, 800), WHITE, GREEN)
    disclaimer(d, [DISC_MEDIPAY], 1000, (155, 148, 138), size=19)
    return im

jobs = [
    ('implants-ad-1-offer.png', implants_offer),
    ('implants-ad-2-photo.png', implants_photo),
    ('implants-ad-3-benefits.png', implants_benefits),
    ('aligners-ad-1-offer.png', aligners_offer),
    ('aligners-ad-2-photo.png', aligners_photo),
    ('aligners-ad-3-benefits.png', aligners_benefits),
]
os.makedirs(OUT, exist_ok=True)
for name, fn in jobs:
    img = fn().convert('RGB')
    img.save(OUT + name, 'PNG')
    print('saved', name)
