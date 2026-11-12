---
title: Andere E-Mail (IMAP)
area: connections
summary: Mail von jedem Anbieter mit IMAP, etwa iCloud, Yahoo, Fastmail, Telenet oder deine eigene Domain.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
---
## Was sie liest

Deinen Posteingang und deinen Ordner Gesendet: beim Verbinden die letzten 7 Tage, danach alles Neue. Mail, die du sendest, zählt auch, so lernt sie, wie du schreibst und was du versprochen hast. Andere Ordner werden nicht gelesen.

In deinem Postfach ändert sich nichts, außer einer Kopie dessen, was The Machine sendet, in deinem Ordner Gesendet. Mail wird nicht als gelesen markiert.

## Was sie tun kann

Sie sendet Mail erst, wenn du auf Senden drückst, über den Mailserver deines Anbieters (SMTP) mit demselben Passwort. Eine Kopie landet in deinem Ordner Gesendet. Antworten bleiben in ihrem Gespräch, und deine Signatur ist die aus den Einstellungen, sonst die, mit der deine gesendeten Mails enden.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **+ Hinzufügen**, und wähle **Andere E-Mail**.
2. Gib deine E-Mail-Adresse und dein Passwort ein.
3. Drücke **Verbinden**.

Viele Anbieter wollen für Mailprogramme ein App-Passwort, nicht dein normales Passwort. Erstelle eins in den Kontoeinstellungen deines Anbieters:

- iCloud: ein app-spezifisches Passwort auf account.apple.com.
- Yahoo: Kontosicherheit, App-Passwort generieren.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: dein normales Passwort für Telenet-Mail.
- Proton Mail: lass Proton Mail Bridge auf demselben Computer laufen und nimm das Passwort, das Bridge anzeigt.

Die Servereinstellungen werden für die meisten Anbieter ausgefüllt. Deiner nicht gefunden? Öffne **Servereinstellungen** und gib ein, was dein Anbieter für Mailprogramme angibt: IMAP- und SMTP-Server, ihre Ports und Sicherheit (SSL/TLS oder STARTTLS). The Machine verbindet sich nie ohne TLS.

Gmail oder Mail von Microsoft, auch auf deiner eigenen Domain? Wähle dann **Gmail** oder **Outlook**. Die melden sich ohne Passwort an.

## Wenn sie stoppt

- **Der Mailserver hat das Passwort abgelehnt**: du hast es geändert, oder das App-Passwort wurde entfernt. Verbinde neu mit dem neuen.
- **Der Mailserver hat das Passwort zum Senden abgelehnt**: Nichts wurde gesendet. Verbinde neu; lehnt er weiter ab, prüfe den SMTP-Server in den Servereinstellungen. Bis dahin liest sie nur.
- **Der Mailserver war nicht erreichbar**: sie versucht es selbst noch einmal. Klappt es weiter nicht, prüfe den Servernamen in den Servereinstellungen.

## Entfernen

**Verbindungen**, das Konto öffnen, **Details**, dann **Trennen**. Sie liest nicht mehr, und was schon da ist, bleibt. Entferne das App-Passwort auch bei deinem Anbieter.
