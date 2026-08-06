# Happy Teeth Springwood — Meta Lead Generation Package

Prepared by Generate Your Audience.

---

## 1. Landing pages

| File | Page |
|---|---|
| `dental-implants.html` | Dental Implants / All-on-X — from $39 per week |
| `clear-aligners.html` | Clear Aligners — from $59 per week |
| `images/` | All photography used by both pages |
| `api/lead.js` | Serverless function relaying form submissions to SmileOx |
| `vercel.json` | Sets `X-Robots-Tag: noindex, nofollow` across all routes |

**Deployment:** upload the whole folder to Vercel. Paths are relative, so the
`images/` folder must sit alongside the HTML files.

**Environment variables to set in Vercel:**

| Variable | Value |
|---|---|
| `SMTP2GO_API_KEY` | SMTP2GO API key (pending — from client's domain verification) |
| `LEAD_TO_EMAIL` | SmileOx intake address for Happy Teeth |
| `LEAD_FROM_EMAIL` | Verified sender, e.g. leads@happyteethspringwood.com.au |

**Still to add before launch:** Meta Pixel and GTM container in the `<head>`
of both pages. The forms already fire `fbq('track','Lead')` and
`gtag('event','generate_lead')` on successful submission.

### Page features
- Background practice video in the hero banner, muted and looping
- SmileOx lead form on the banner with qualifier questions (treatment interest
  and timeframe) — the only conversion path, no phone number anywhere
- Procedure explained with custom diagrams
- Funding: MediPay (fortnightly, weekly equivalents shown), access-your-super
  (implants only), health fund rebates
- Dentist profiles, FAQs, aftercare, before/after results (aligners page)
- "Visit us at Springwood Mall" banner with live Google Map
- Footer toggle between the two pages
- Both pages set to noindex, nofollow
- AHPRA disclaimers: MediPay terms, surgical risk, super eligibility,
  practitioner attribution on before/after images

---

## 2. Meta ad creatives

Twelve 1080x1080 creatives. `happy-teeth-ads-suite.png` shows all of them
on one labelled sheet for client approval.

### Dental Implants (gold accent)
| File | Angle |
|---|---|
| `implants-ad-1-offer.png` | Price-led offer hero |
| `implants-ad-2-photo.png` | Practice frontage — "Missing or failing teeth?" |
| `implants-ad-3-benefits.png` | Benefits checklist |
| `implants-ad-4-dr-allan.png` | Dr Allan Nguyen |
| `implants-ad-5-implant-team.png` | Dr Allan Nguyen + Dr Jungin Park |

### Clear Aligners (salmon accent)
| File | Angle |
|---|---|
| `aligners-ad-1-offer.png` | Price-led offer hero |
| `aligners-ad-2-photo.png` | Practice frontage |
| `aligners-ad-3-benefits.png` | Benefits checklist |
| `aligners-ad-4-dr-mary.png` | Dr Mary Liu |
| `aligners-ad-5-mary-green.png` | Dr Mary Liu, green variant |
| `aligners-ad-6-results.png` | Before / after — displaced side tooth |
| `aligners-ad-7-before-after.png` | Before / after — flared front teeth |

All creatives carry the MediPay disclaimer. The before/after creatives also
carry the practitioner attribution and an individual-results-vary line.

**Note on the two before/after creatives:** these are AHPRA-appropriate, but
Meta occasionally rejects before/after imagery under its personal health
policy. Suggested approach is to launch the other ten first, then add these
once the account is delivering cleanly.

`gen_ads.py`, `gen_dentist_ads.py` and `gen_ba_ads.py` regenerate the
creatives, so copy or sizing changes can be reissued quickly. Other sizes
(4:5 feed, 9:16 Stories) can be produced from the same scripts.

---

## 3. Brand reference

| Element | Value |
|---|---|
| Brand green | `#286050` |
| Deep green | `#1B453A` |
| Ink green | `#12332B` |
| Brand gold (implants) | `#A47D50` |
| Salmon (aligners) | `#DDA090` |
| Cream | `#FAF6F1` |
| Headings | Fraunces |
| Body | Inter |

---

## 4. Outstanding items

1. Meta Business Portfolio ID — to request access to the Facebook and
   Instagram pages
2. SMTP2GO API key — after the client's domain verification
3. Client sign-off on the ad creatives
4. Meta Pixel and GTM container IDs to add to both pages
