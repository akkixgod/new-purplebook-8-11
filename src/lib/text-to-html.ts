/** Shared SAT passage/question text → safe HTML with Bluebook underlines. */

export function textToHtml(text: string): string {
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // `_phrase_` → Bluebook underline (avoid matching snake_case).
  // Cap is high enough for full underlined sentences in Bluebook R&W items.
  const withUnderlines = escaped.replace(
    /(^|[^A-Za-z0-9])_([^_\n]{1,400}?)_([^A-Za-z0-9]|$)/g,
    '$1<u class="sat-underline">$2</u>$3'
  );

  return withUnderlines.replace(/\n/g, "<br/>");
}
