// /api/lead.js — Vercel serverless function
// Relays landing page leads to the SmileOx website-form intake as a JSON email via SMTP2GO.
// Set these environment variables in Vercel:
//   SMTP2GO_API_KEY   — SMTP2GO API key
//   LEAD_TO_EMAIL     — SmileOx intake address for Happy Teeth (e.g. happyteeth@intake.smileox.com)
//   LEAD_FROM_EMAIL   — verified sender (e.g. leads@happyteethspringwood.com.au)

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, phone, email, interest, message, page, submittedAt } = req.body || {};

  if (!name || !phone || !email) {
    return res.status(400).json({ error: 'Missing required fields' });
  }

  const payload = {
    source: 'Landing Page',
    page: page || 'Happy Teeth Springwood',
    name,
    phone,
    email,
    interest: interest || '',
    message: message || '',
    submittedAt: submittedAt || new Date().toISOString(),
  };

  const textBody = JSON.stringify(payload, null, 2);

  try {
    const r = await fetch('https://api.smtp2go.com/v3/email/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        api_key: process.env.SMTP2GO_API_KEY,
        to: [process.env.LEAD_TO_EMAIL],
        sender: process.env.LEAD_FROM_EMAIL,
        subject: `New Lead — ${payload.page} — ${name}`,
        text_body: textBody,
      }),
    });

    const data = await r.json();
    if (!r.ok || (data && data.data && data.data.error)) {
      console.error('SMTP2GO error', data);
      return res.status(502).json({ error: 'Relay failed' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Server error' });
  }
}
