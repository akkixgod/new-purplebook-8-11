type SendEmailInput = {
  to: string;
  subject: string;
  html: string;
  text: string;
};

export type SendEmailResult =
  | { ok: true; provider: "resend" }
  | { ok: false; reason: "not_configured" | "provider_error"; detail: string };

function defaultFrom(): string {
  return process.env.EMAIL_FROM?.trim() || "PurpleBook <onboarding@resend.dev>";
}

export function isEmailConfigured(): boolean {
  return Boolean(process.env.RESEND_API_KEY?.trim());
}

/**
 * Send via Resend when RESEND_API_KEY is set.
 * Never silently succeeds when delivery did not happen.
 */
export async function sendEmail(input: SendEmailInput): Promise<SendEmailResult> {
  const apiKey = process.env.RESEND_API_KEY?.trim();

  if (!apiKey) {
    console.warn(
      [
        "[email] RESEND_API_KEY is not set — email was NOT sent.",
        "Set RESEND_API_KEY (and optionally EMAIL_FROM) in .env / Vercel.",
        `To: ${input.to}`,
        `Subject: ${input.subject}`,
        "",
        input.text,
      ].join("\n")
    );
    return {
      ok: false,
      reason: "not_configured",
      detail: "RESEND_API_KEY is missing",
    };
  }

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: defaultFrom(),
        to: [input.to],
        subject: input.subject,
        html: input.html,
        text: input.text,
      }),
    });

    if (!res.ok) {
      const body = await res.text().catch(() => "");
      const detail = `Resend failed (${res.status}): ${body.slice(0, 300)}`;
      console.error("[email]", detail);
      return { ok: false, reason: "provider_error", detail };
    }

    return { ok: true, provider: "resend" };
  } catch (err) {
    const detail = err instanceof Error ? err.message : String(err);
    console.error("[email] network/provider error:", detail);
    return { ok: false, reason: "provider_error", detail };
  }
}

export function passwordResetEmailContent(resetUrl: string): {
  subject: string;
  html: string;
  text: string;
} {
  const subject = "Reset your PurpleBook password";
  const text = [
    "You requested a password reset for your PurpleBook account.",
    "",
    "Open this link to choose a new password (expires in 1 hour):",
    resetUrl,
    "",
    "If you did not request this, you can ignore this email.",
  ].join("\n");

  const html = `
    <div style="font-family: system-ui, -apple-system, Segoe UI, sans-serif; max-width: 480px; margin: 0 auto; color: #111;">
      <h1 style="font-size: 20px; margin-bottom: 12px;">Reset your password</h1>
      <p style="font-size: 14px; line-height: 1.5; color: #374151;">
        You requested a password reset for your PurpleBook account. Click the button below to choose a new password. This link expires in <strong>1 hour</strong>.
      </p>
      <p style="margin: 28px 0;">
        <a href="${resetUrl}" style="display: inline-block; background: #7c3aed; color: #fff; text-decoration: none; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: 600;">
          Reset password
        </a>
      </p>
      <p style="font-size: 12px; color: #6b7280; line-height: 1.5;">
        Or paste this link into your browser:<br />
        <a href="${resetUrl}" style="color: #7c3aed; word-break: break-all;">${resetUrl}</a>
      </p>
      <p style="font-size: 12px; color: #9ca3af; margin-top: 24px;">
        If you did not request this, you can ignore this email.
      </p>
    </div>
  `.trim();

  return { subject, html, text };
}
