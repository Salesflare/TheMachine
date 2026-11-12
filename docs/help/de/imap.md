---
title: Andere E-Mail (IMAP)
area: connections
summary: Mail von jedem Anbieter mit IMAP, etwa iCloud, Yahoo, Fastmail, Telenet oder deine eigene Domain. Liest vorerst nur.
covers: connector:imap
code: imap_mail.py, imap_presets.py, onboarding.py
order: 13
---
## Was sie liest

Deinen Posteingang und deinen Ordner Gesendet: beim Verbinden die letzten 7 Tage, danach alles Neue. Mail, die du sendest, zählt auch, so lernt sie, wie du schreibst und was du versprochen hast. Andere Ordner werden nicht gelesen.

In deinem Postfach ändert sich nichts. Mail wird nicht als gelesen markiert.

## Was sie tun kann

Vorerst liest sie nur: Senden aus diesem Postfach geht noch nicht. Eine für dich vorbereitete Antwort kopierst du selbst in dein Mailprogramm.

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

Die Servereinstellungen werden für die meisten Anbieter ausgefüllt. Deiner nicht gefunden? Öffne **Servereinstellungen** und gib ein, was dein Anbieter für Mailprogramme angibt: IMAP-Server, Port und Sicherheit (SSL/TLS oder STARTTLS). The Machine verbindet sich nie ohne TLS.

Gmail oder Mail von Microsoft, auch auf deiner eigenen Domain? Wähle dann **Gmail** oder **Outlook**. Die melden sich ohne Passwort an.

## Wenn sie stoppt

- **Der Mailserver hat das Passwort abgelehnt**: du hast es geändert, oder das App-Passwort wurde entfernt. Verbinde neu mit dem neuen.
- **Der Mailserver war nicht erreichbar**: sie versucht es selbst noch einmal. Klappt es weiter nicht, prüfe den Servernamen in den Servereinstellungen.

## Entfernen

**Verbindungen**, das Konto öffnen, **Details**, dann **Trennen**. Sie liest nicht mehr, und was schon da ist, bleibt. Entferne das App-Passwort auch bei deinem Anbieter.
