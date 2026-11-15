// The owner's language for what the bridge writes in Telegram (buttons, replies, the send review): the same catalogs
// and rules as i18n.py. Keys are the English text, so English stays the source and the fallback.
import { readFileSync, statSync } from 'node:fs';

const LANGUAGES = ['en', 'nl', 'fr', 'de', 'es', 'it', 'pt-BR', 'zh-CN', 'ja', 'ko', 'ru'];  // locale_prefs.LANGUAGES
const CODES: Record<string, string> = Object.fromEntries(LANGUAGES.map(code => [code.toLowerCase(), code]));
const NEAREST: Record<string, string> = {pt: 'pt-BR', zh: 'zh-CN'};  // locale_prefs.NEAREST: Portuguese from Portugal reads Brazilian, any Chinese Simplified
const catalogs: Record<string, {at: number, entries: Record<string, any>}> = {};
let current = 'en';

const codeOf = (value: any) => CODES[String(value || '').trim().toLowerCase().replace(/_/g, '-')];

// language_of() in locale_prefs.py: the owner's choice, else a language from the locale (signup), else English.
export function languageOf(config: any): string {
  const chosen = codeOf(config?.language);
  if (chosen) return chosen;
  const tag = String(config?.locale || '').trim().toLowerCase().replace(/_/g, '-');
  const base = tag.split('-')[0];
  return (tag && (CODES[tag] || CODES[base] || NEAREST[base])) || 'en';
}

// Set from the config on each tap or message, as the dashboard root is.
export function useLanguage(config: any) { current = languageOf(config); }

// One fixed file per language, each read by name: no path comes from a config value.
const EN = new URL('../i18n/en.json', import.meta.url), NL = new URL('../i18n/nl.json', import.meta.url),
  FR = new URL('../i18n/fr.json', import.meta.url), DE = new URL('../i18n/de.json', import.meta.url),
  ES = new URL('../i18n/es.json', import.meta.url), IT = new URL('../i18n/it.json', import.meta.url),
  PT_BR = new URL('../i18n/pt-BR.json', import.meta.url), ZH_CN = new URL('../i18n/zh-CN.json', import.meta.url),
  JA = new URL('../i18n/ja.json', import.meta.url), KO = new URL('../i18n/ko.json', import.meta.url),
  RU = new URL('../i18n/ru.json', import.meta.url);
const FILES: Record<string, () => {at: number, text: () => string}> = {
  en: () => ({at: statSync(EN).mtimeMs, text: () => readFileSync(EN, 'utf8')}),
  nl: () => ({at: statSync(NL).mtimeMs, text: () => readFileSync(NL, 'utf8')}),
  fr: () => ({at: statSync(FR).mtimeMs, text: () => readFileSync(FR, 'utf8')}),
  de: () => ({at: statSync(DE).mtimeMs, text: () => readFileSync(DE, 'utf8')}),
  es: () => ({at: statSync(ES).mtimeMs, text: () => readFileSync(ES, 'utf8')}),
  it: () => ({at: statSync(IT).mtimeMs, text: () => readFileSync(IT, 'utf8')}),
  'pt-BR': () => ({at: statSync(PT_BR).mtimeMs, text: () => readFileSync(PT_BR, 'utf8')}),
  'zh-CN': () => ({at: statSync(ZH_CN).mtimeMs, text: () => readFileSync(ZH_CN, 'utf8')}),
  ja: () => ({at: statSync(JA).mtimeMs, text: () => readFileSync(JA, 'utf8')}),
  ko: () => ({at: statSync(KO).mtimeMs, text: () => readFileSync(KO, 'utf8')}),
  ru: () => ({at: statSync(RU).mtimeMs, text: () => readFileSync(RU, 'utf8')}),
};

// Read again when the file changed: an update brings new catalogs without a plugin reload.
function catalog(lang: string): Record<string, any> {
  if (!Object.hasOwn(FILES, lang)) return {};
  let file;
  try { file = FILES[lang](); } catch { return {}; }
  if (catalogs[lang]?.at !== file.at) {
    try { catalogs[lang] = {at: file.at, entries: JSON.parse(file.text())}; }
    catch { catalogs[lang] = {at: file.at, entries: {}}; }
  }
  return catalogs[lang].entries;
}

const plural = (lang: string, n: any) => {
  const v = Math.abs(Number(n));
  if (Number.isNaN(v)) return 'other';
  if (lang === 'zh-CN' || lang === 'ja' || lang === 'ko') return 'other';
  if (lang === 'ru') {  // i18n.plural_form: 1, 21 one; 2-4 few; 0, 5-20 many; fractions other
    if (!Number.isInteger(v)) return 'other';
    if (v % 10 === 1 && v % 100 !== 11) return 'one';
    return v % 10 >= 2 && v % 10 <= 4 && !(v % 100 >= 12 && v % 100 <= 14) ? 'few' : 'many';
  }
  return lang === 'fr' || lang === 'pt-BR' ? (v < 2 ? 'one' : 'other') : (v === 1 ? 'one' : 'other');
};

export function t(text: string, ...args: any[]): string {
  let found: any = current !== 'en' ? catalog(current)[text] : undefined, lang = current;
  if (found === undefined) { found = catalog('en')[text] ?? text; lang = 'en'; }
  if (found && typeof found === 'object') {
    const n = args.find(a => typeof a === 'number');
    found = found[plural(lang, n)] || found.other || text;
  }
  let i = 0;
  return String(found).replace(/\{(\d*)\}/g, (m, d) => {
    const k = d === '' ? i++ : Number(d);
    return k < args.length ? String(args[k]) : m;
  });
}
