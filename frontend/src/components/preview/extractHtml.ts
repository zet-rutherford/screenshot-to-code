export function extractHtml(code: string): string {
  // Regex to match <html ...> ... </html>, including attributes in the <html> tag, case insensitive and dot matches newlines
  const regex = /<html\b[^>]*>[\s\S]*?<\/html>/i;
  const match = code.match(regex);
  if (match) {
    return match[0];
  }
  return "";
}