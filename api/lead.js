// /api/lead.js — Vercel serverless function
//
// Relays landing page form submissions into SmileOx via its Website Form Intake.
// SmileOx expects an email whose plain-text body is a JSON payload, sent over TLS.
//
// Required environment variables in Vercel:
//   SMTP2GO_API_KEY   SMTP2GO API key
//   LEAD_FROM_EMAIL   verified sender on the SMTP2GO account,
//                     e.g. no-reply@happyteethspringwood.com.au
// Optional overrides (only if SmileOx reissues an intake address):
//   INTAKE_IMPLANTS, INTAKE_ALIGNERS

const INTAKES = {
  implants:
    process.env.INTAKE_IMPLANTS ||
    'dental-implants+51c38aac-85c5-452b-8640-a3697eb0dab9@intake.smileox.com.au',
  aligners:
    process.env.INTAKE_ALIGNERS ||
    'ortho+8ca047a5-f8fc-4379-b798-1d1782d2fed3@intake.smileox.com.au',
};

// "Jane Maree Smith" -> { firstName: "Jane", lastName: "Maree Smith" }
function splitName(full) {
  const parts = String(full || '').trim().replace(/\s+/g, ' ').split(' ');
  if (parts.length === 0 || parts[0] === '') return { firstName: '', lastName: '' };
  if (parts.length === 1) return { firstName: parts[0], lastName: '' };
  return { firstName: parts[0], lastName: parts.slice(1).join(' ') };
}

// Normalise Australian numbers to E.164 so SmileOx matches leads reliably
// and the SMS automations can dial them.
function normalisePhone(raw) {
  const input = String(raw || '').trim();
  if (!input) return '';
  const digits = input.replace(/[^\d+]/g, '');
  if (digits.startsWith('+')) return digits;
  const n = digits.replace(/\D/g, '');
  if (n.startsWith('61') && n.length >= 11) return '+' + n;
  if (n.startsWith('0') && n.length === 10) return '+61' + n.slice(1);
  if (n.length === 9 && /^[45]/.test(n)) return '+61' + n;
  return input;
}

async function sendViaSmtp2go(body) {
  return fetch('https://api.smtp2go.com/v3/email/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
}

export default async function handler(req, res) {
  // GET /api/lead — config health check. Never returns the key itself.
  if (req.method === 'GET') {
    return res.status(200).json({
      ok: true,
      runtime: 'reachable',
      hasApiKey: Boolean(process.env.SMTP2GO_API_KEY),
      hasFromEmail: Boolean(process.env.LEAD_FROM_EMAIL),
      fromEmail: process.env.LEAD_FROM_EMAIL || null,
      intakes: Object.keys(INTAKES),
    });
  }

  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST, GET');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Fail loudly and clearly if the environment isn't configured yet.
  if (!process.env.SMTP2GO_API_KEY || !process.env.LEAD_FROM_EMAIL) {
    console.error('Missing env vars', {
      hasApiKey: Boolean(process.env.SMTP2GO_API_KEY),
      hasFromEmail: Boolean(process.env.LEAD_FROM_EMAIL),
    });
    return res.status(500).json({ error: 'Not configured', reason: 'missing_env' });
  }

  const {
    formKey, page, name, firstName: firstIn, lastName: lastIn, email, phone,
    teeth, concern, timeframe, submittedAt,
  } = req.body || {};

  // Forms post firstName / lastName. `name` is still accepted so an older
  // cached page keeps working after a deploy.
  const first = String(firstIn || '').trim();
  const last = String(lastIn || '').trim();
  const { firstName, lastName } = first || last
    ? { firstName: first, lastName: last }
    : splitName(name);

  if (!firstName || !phone || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const to = INTAKES[formKey];
  if (!to) {
    console.error('Unknown formKey:', formKey);
    return res.status(400).json({ error: 'Unknown form' });
  }

  // SmileOx schema: firstName / lastName / email / phoneNumber, plus any
  // extra fields, which are stored against the lead.
  const payload = {
    firstName,
    lastName,
    email: String(email).trim(),
    phoneNumber: normalisePhone(phone),
    source: 'Meta Ads Landing Page',
    page: page || formKey,
    submittedAt: submittedAt || new Date().toISOString(),
  };
  if (teeth) payload.teethToReplace = teeth;
  if (concern) payload.smileConcern = concern;
  if (timeframe) payload.timeframe = timeframe;

  const mail = {
    api_key: process.env.SMTP2GO_API_KEY,
    to: [to],
    sender: process.env.LEAD_FROM_EMAIL,
    subject: 'Website form submission',
    text_body: JSON.stringify(payload),
  };

  // Retry transient failures — a dropped lead costs far more than a retry.
  const delays = [0, 600, 1800];
  let lastDetail = null;

  for (let attempt = 0; attempt < delays.length; attempt++) {
    if (delays[attempt]) await new Promise((r) => setTimeout(r, delays[attempt]));
    try {
      const r = await sendViaSmtp2go(mail);
      const data = await r.json().catch(() => ({}));
      const succeeded = r.ok && data && data.data && Number(data.data.succeeded) > 0;
      if (succeeded) return res.status(200).json({ ok: true });

      lastDetail = data;
      const transient = r.status >= 500 || r.status === 429;
      if (!transient) break;
    } catch (err) {
      lastDetail = String(err);
    }
  }

  // Log the payload so nothing is lost if delivery fails — the lead can be
  // recovered from the Vercel function logs and entered manually.
  const providerError =
    (lastDetail && lastDetail.data && (lastDetail.data.error || lastDetail.data.error_code)) ||
    (typeof lastDetail === 'string' ? lastDetail : null);

  console.error('SmileOx relay failed', { to, detail: lastDetail, payload });
  return res.status(502).json({ error: 'Relay failed', reason: providerError || 'unknown' });
}
