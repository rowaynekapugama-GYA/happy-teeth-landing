#!/usr/bin/env python3
"""Happy Teeth — dentist-featured Meta ad variations (2 per service)."""
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os

W = H = 1080
GREEN = (40, 96, 80); INK = (18, 51, 43); SALM = (221, 160, 144)
GOLD = (164, 125, 80); GOLDD = (138, 103, 64)
SALMD = (206, 130, 112); CREAM = (250, 246, 241); LINE = (229, 222, 213)
WHITE = (255, 255, 255); MUT = (95, 114, 104)

FR = '/home/claude/fonts/Fraunces.ttf'; IN = '/home/claude/fonts/Inter.ttf'
UP = '/mnt/user-data/uploads/'; OUT = '/home/claude/happy-teeth-landing/ads/'

def fraunces(size, wght=560):
    f = ImageFont.truetype(FR, size)
    try: f.set_variation_by_axes([0.0, 0.0, 144.0, wght])
    except Exception: pass
    return f

def inter(size, wght=500):
    f = ImageFont.truetype(IN, size)
    try: f.set_variation_by_axes([28.0, wght])
    except Exception: pass
    return f

def rrect(d, xy, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)

def tw(d, t, f): return d.textlength(t, font=f)

def ct(d, cx, y, t, f, fill):
    d.text((cx - tw(d, t, f)/2, y), t, font=f, fill=fill)

def pill(d, cx, cy, t, f, fg, bg, padx=44, pady=26):
    w = tw(d, t, f); asc, desc = f.getmetrics(); th = asc + desc
    x0, y0, x1, y1 = cx-w/2-padx, cy-th/2-pady, cx+w/2+padx, cy+th/2+pady
    rrect(d, (x0, y0, x1, y1), (y1-y0)/2, fill=bg)
    d.text((cx-w/2, cy-th/2+2), t, font=f, fill=fg)

def photo(canvas, path, box, r=36, cy=0.42, cx=0.5):
    x0, y0, x1, y1 = box; bw, bh = x1-x0, y1-y0
    im = ImageOps.exif_transpose(Image.open(path)).convert('RGB')
    im = ImageOps.fit(im, (bw, bh), Image.LANCZOS, centering=(cx, cy))
    mask = Image.new('L', (bw, bh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, bw, bh), r, fill=255)
    canvas.paste(im, (x0, y0), mask)

def nameplate(canvas, d, x, y, name, role, dark=True, accent=None):
    nf, rf = inter(30, 800), inter(23, 600)
    w = max(tw(d, name, nf), tw(d, role, rf))
    bg = (18, 51, 43, 225) if dark else (255, 255, 255, 235)
    fg1 = WHITE if dark else INK
    fg2 = (accent if accent else (SALM if dark else SALMD))
    ov = Image.new('RGBA', canvas.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    rrect(od, (x, y, x + w + 56, y + 106), 22, fill=bg)
    od.text((x + 28, y + 18), name, font=nf, fill=fg1)
    od.text((x + 28, y + 60), role, font=rf, fill=fg2)
    canvas.alpha_composite(ov)

def chip(d, cx, cy, t, bg=None):
    pill(d, cx, cy, t, inter(34, 800), WHITE if bg else INK, bg if bg else SALM, padx=36, pady=20)

def logo_on_green(target_w):
    lg = Image.open(UP + 'logo-combined-B-I0u10U.png').convert('RGBA')
    sc = target_w / lg.width
    return lg.resize((target_w, int(lg.height * sc)), Image.LANCZOS)

def base(bg):
    im = Image.new('RGBA', (W, H), bg + (255,))
    return im, ImageDraw.Draw(im)

def disc(d, y, fill, size=20):
    ct(d, W/2, y, "*Equivalent weekly cost via MediPay payment plan; repayments fortnightly. Approval, eligibility & T&Cs apply.", inter(size, 500), fill)

# ---------------- ALIGNERS 4: Meet Dr Mary Liu (cream)
def mary_meet():
    im, d = base(CREAM)
    photo(im, UP + 'mary.png', (50, 50, 1030, 592), r=38, cy=0.30)
    nameplate(im, d, 76, 460, 'Dr Mary Liu', 'Clear Aligner Dentist · 20+ years')
    d = ImageDraw.Draw(im)
    chip(d, 872, 118, 'from $59/wk*')
    ct(d, W/2, 640, 'Your smile, in expert hands', fraunces(72, 560), GREEN)
    ct(d, W/2, 736, 'Digital scan, smile preview and a clear aligner plan', inter(32, 500), MUT)
    ct(d, W/2, 780, 'made just for you — at Happy Teeth Springwood.', inter(32, 500), MUT)
    pill(d, W/2, 908, 'Book Your FREE Consultation', inter(38, 800), WHITE, GREEN)
    disc(d, 1010, (155, 148, 138))
    return im

# ---------------- ALIGNERS 5: Mary on green
def mary_green():
    im, d = base(GREEN)
    lg = logo_on_green(280)
    im.alpha_composite(lg, (int(W/2 - lg.width/2), 54))
    d = ImageDraw.Draw(im)
    ct(d, W/2, 186, 'Straighten your teeth', fraunces(78, 560), WHITE)
    ct(d, W/2, 280, 'with Dr Mary Liu', fraunces(78, 480), SALM)
    photo(im, UP + 'mary.png', (140, 408, 940, 806), r=36, cy=0.32)
    nameplate(im, d, 166, 690, 'Dr Mary Liu', 'Clear Aligner Dentist · 20+ years')
    d = ImageDraw.Draw(im)
    ct(d, W/2, 838, 'Nearly invisible aligners  ·  from $59 per week*', inter(33, 600), WHITE)
    pill(d, W/2, 942, 'Book Your FREE Consultation', inter(38, 800), WHITE, SALMD)
    disc(d, 1020, (150, 180, 168))
    return im

# ---------------- IMPLANTS 4: Meet Dr Allan Nguyen (green)
def allan_meet():
    im, d = base(GREEN)
    photo(im, UP + 'AllanProfile-BgqUZGQo.png', (50, 50, 1030, 592), r=38, cy=0.35)
    nameplate(im, d, 76, 460, 'Dr Allan Nguyen', 'All-On-X & Implant Dentist · 10+ years', accent=(214,182,140))
    d = ImageDraw.Draw(im)
    chip(d, 872, 118, 'from $39/wk*', bg=GOLD)
    ct(d, W/2, 636, 'Implants, planned with precision', fraunces(66, 560), WHITE)
    ct(d, W/2, 726, 'Advanced implant training and personalised treatment', inter(31, 500), (200, 220, 211))
    ct(d, W/2, 770, 'planning — from a single tooth to a full All-on-X arch.', inter(31, 500), (200, 220, 211))
    pill(d, W/2, 898, 'Book Your FREE Consultation', inter(38, 800), WHITE, GOLDD)
    disc(d, 1006, (150, 180, 168))
    return im

# ---------------- IMPLANTS 5: two implant dentists (cream)
def implant_duo():
    im, d = base(CREAM)
    rrect(d, (46, 46, 1034, 1034), 40, outline=LINE, width=3)
    ct(d, W/2, 96, 'D E N T A L   I M P L A N T S   ·   S P R I N G W O O D', inter(24, 700), GOLDD)
    ct(d, W/2, 148, 'Two dedicated implant &', fraunces(72, 560), GREEN)
    ct(d, W/2, 236, 'surgical dentists.', fraunces(72, 480), GOLDD)
    # duo panels
    photo(im, UP + 'AllanProfile-BgqUZGQo.png', (108, 366, 528, 786), r=32, cy=0.35)
    photo(im, UP + 'jungin.webp', (552, 366, 972, 786), r=32, cy=0.35)
    nameplate(im, d, 126, 664, 'Dr Allan Nguyen', 'All-On-X & Implants', accent=(214,182,140))
    nameplate(im, d, 570, 664, 'Dr Jungin Park', 'Surgical & Implants', accent=(214,182,140))
    d = ImageDraw.Draw(im)
    ct(d, W/2, 822, 'Experienced hands for every stage — from $39 per week*', inter(32, 600), (33, 61, 51))
    pill(d, W/2, 930, 'Book Your FREE Consultation', inter(38, 800), WHITE, GREEN)
    disc(d, 1000, (155, 148, 138), size=19)
    return im

jobs = [
    ('aligners-ad-4-dr-mary.png', mary_meet),
    ('aligners-ad-5-mary-green.png', mary_green),
    ('implants-ad-4-dr-allan.png', allan_meet),
    ('implants-ad-5-implant-team.png', implant_duo),
]
for name, fn in jobs:
    fn().convert('RGB').save(OUT + name, 'PNG')
    print('saved', name)
