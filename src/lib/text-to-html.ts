/** Shared SAT passage/question text → safe HTML with Bluebook underlines. */

export function textToHtml(text: string): string {
  const escapeHtml = (s: string) =>
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Preserve intentional <u>...</u> (and classed variants) before escaping.
  const tokens: string[] = [];
  const withPlaceholders = text.replace(
    /<\s*u\b[^>]*>[\s\S]*?<\s*\/\s*u\s*>/gi,
    (match) => {
      const inner = match.replace(/^<\s*u\b[^>]*>/i, "").replace(/<\s*\/\s*u\s*>$/i, "");
      const idx = tokens.length;
      tokens.push(`<u class="sat-underline">${escapeHtml(inner)}</u>`);
      return `\u0000U${idx}\u0000`;
    }
  );

  const escaped = withPlaceholders
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // `_phrase_` → Bluebook underline (avoid matching snake_case).
  // Cap is high enough for full underlined sentences in Bluebook R&W items.
  let withUnderlines = escaped.replace(
    /(^|[^A-Za-z0-9])_([^_\n]{1,400}?)_([^A-Za-z0-9]|$)/g,
    '$1<u class="sat-underline">$2</u>$3'
  );

  withUnderlines = withUnderlines.replace(/\u0000U(\d+)\u0000/g, (_, n) => tokens[Number(n)]);

  return withUnderlines.replace(/\n/g, "<br/>");
}
