// The owner's language for what the bridge writes in Telegram (buttons, replies, the send review): the same catalogs
// and rules as i18n.py. Keys are the English text, so English stays the source and the fallback.
import { readFileSync, statSync } from 'node:fs';

const LANGUAGES = ['en', 'nl', 'fr', 'de', 'es'];  // locale_prefs.LANGUAGES
const catalogs: Record<string, {at: number, entries: Record<string, any>}> = {};
let current = 'en';

// language_of() in locale_prefs.py: the owner's choice, else a language from the locale (signup), else English.
export function languageOf(config: any): string {
  const chosen = String(config?.language || '').toLowerCase();
  if (LANGUAGES.includes(chosen)) return chosen;
  const tag = /^([A-Za-z]{2,3})[-_][A-Za-z]{2}$/.exec(String(config?.locale || '').trim());
  const lang = tag ? tag[1].toLowerCase() : 'en';
  return LANGUAGES.includes(lang) ? lang : 'en';
}

// Set from the config on each tap or message, as the dashboard root is.
export function useLanguage(config: any) { current = languageOf(config); }

// Read again when the file changed: an update brings new catalogs without a plugin reload.
function catalog(lang: string): Record<string, any> {
  const file = new URL(`../i18n/${lang}.json`, import.meta.url);
  let at = 0;
  try { at = statSync(file).mtimeMs; } catch { return {}; }
  if (catalogs[lang]?.at !== at) {
    try { catalogs[lang] = {at, entries: JSON.parse(readFileSync(file, 'utf8'))}; }
    catch { catalogs[lang] = {at, entries: {}}; }
  }
  return catalogs[lang].entries;
}

const plural = (lang: string, n: any) => {
  const v = Math.abs(Number(n));
  if (Number.isNaN(v)) return 'other';
  return lang === 'fr' ? (v < 2 ? 'one' : 'other') : (v === 1 ? 'one' : 'other');
};

export function t(text: string, ...args: any[]): string {
  let found: any = current !== 'en' ? catalog(current)[text] : undefined;
  if (found === undefined) found = catalog('en')[text] ?? text;
  if (found && typeof found === 'object') {
    const n = args.find(a => typeof a === 'number');
    found = found[plural(current, n)] || found.other || text;
  }
  let i = 0;
  return String(found).replace(/\{(\d*)\}/g, (m, d) => {
    const k = d === '' ? i++ : Number(d);
    return k < args.length ? String(args[k]) : m;
  });
}
