# Happy Teeth Springwood — Meta Lead Generation

Landing pages and ad creatives for the Happy Teeth Springwood Meta lead
generation campaigns. Built by Generate Your Audience.

## Quick start

```bash
git clone <this-repo>
cd happy-teeth-landing-pages
npx vercel            # preview deploy
npx vercel --prod     # production deploy
```

Then in **Vercel > Project > Settings > Environment Variables**, add:

| Variable | Value |
|---|---|
| `SMTP2GO_API_KEY` | SMTP2GO API key |
| `LEAD_FROM_EMAIL` | Verified sender, e.g. no-reply@happyteethspringwood.com.au |

Redeploy after adding them, then submit a test enquiry on each page and
confirm the lead lands in the matching SmileOx pipeline.

> **Never commit the API key.** `.env` is git-ignored; use `.env.example`
> as the template.

## Repo layout

```
index.html              Chooser page for the site root
dental-implants.html    Implants / All-on-X landing page
clear-aligners.html     Clear aligners landing page
api/lead.js             Serverless relay: form -> SmileOx intake
images/                 All page photography and diagrams
vercel.json             noindex headers on every route
marketing/meta-ads/     12 ad creatives + approval sheet (not deployed)
marketing/ad-scripts/   Python generators for the creatives
```

---

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
| `SMTP2GO_API_KEY` | SMTP2GO API key |
| `LEAD_FROM_EMAIL` | Verified sender on the SMTP2GO account, e.g. no-reply@happyteethspringwood.com.au |

Optional, only if SmileOx reissues an intake address: `INTAKE_IMPLANTS`,
`INTAKE_ALIGNERS`.

**SmileOx intake addresses** (already hardcoded in `api/lead.js`):

| Form | Intake |
|---|---|
| Dental Implants | dental-implants+51c38aac-...@intake.smileox.com.au |
| Clear Aligners | ortho+8ca047a5-...@intake.smileox.com.au |

Each submission is sent to the matching intake as an email whose plain-text
body is the JSON payload SmileOx expects: `firstName`, `lastName`, `email`,
`phoneNumber`, plus `source`, `page`, `submittedAt` and the qualifier answers
(`teethToReplace` / `smileConcern` / `timeframe`). Phone numbers are
normalised to E.164 (+61) so SmileOx matches leads reliably and the SMS
automations can dial them. Transient send failures are retried three times,
and any failed payload is written to the Vercel function logs so a lead can
be recovered manually.

**Enable Require TLS** on the sending domain in SMTP2GO (Settings → Sender
Domains). SmileOx may reject messages delivered without TLS.

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
