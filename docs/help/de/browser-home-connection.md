---
title: Die Heimverbindung deines Browsers
area: troubleshooting
summary: Lass den Browser deiner gehosteten Machine mit Tailscale über dein Internet zu Hause rausgehen, damit Websites seine Anmeldungen annehmen.
code: browser_login.py
site: Tailscale, Sign in to Tailscale, Use this exit node, Open it in Tailscale, Test it, Sign in again, Stop using it, Sign it out of Tailscale too
keywords: tailscale, exit node, home internet, ip address, cloudflare, linkedin
order: 4
---
Manche Websites, wie LinkedIn, X und Seiten hinter einer Cloudflare-Prüfung, lehnen Anmeldungen von einem Browser in der Cloud ab. Deine Einrichtungsseite kann den Browser deiner gehosteten Machine stattdessen über dein Internet zu Hause schicken, mit Tailscale. Das ist kostenlos, dauert etwa 10 Minuten, und das meiste passiert von selbst.

## Einrichten

1. Wähle auf deiner Einrichtungsseite beim Browser deiner Machine **Tailscale** und drücke **Bei Tailscale anmelden**. Melde dich an oder lege dort ein kostenloses Konto an.
2. Installiere Tailscale auf einem Computer zu Hause, der an bleibt, und melde dich dort mit demselben Konto an. Kein Handy: Das schläft.
3. Mach diesen Computer zum Exit-Node. Die Einrichtungsseite zeigt das Menü für sein System. Unter Linux führst du `sudo tailscale set --advertise-exit-node` aus.
4. Drücke **In Tailscale öffnen** und erlaube ihn: Machine settings, Edit route settings, Use as exit node, Save. Wähle im selben Menü Disable key expiry.

Die Einrichtungsseite hakt jeden Schritt selbst ab. Mit einem Exit-Node nutzt dein Browser ihn sofort. Mit mehreren wählst du einen und drückst **Diesen Exit-Node verwenden**.

## Prüfen

Drücke **Testen**. Die Seite zeigt, wo das Web deinen Browser sieht: deine Stadt und deinen Internetanbieter.

## Wenn dein Computer zu Hause aus ist

Dein Browser geht dann direkt von deiner Machine raus, und wieder über dein Zuhause, sobald der Computer wieder an ist. Bei Tailscale abgemeldet? Drücke **Neu anmelden**. Tailscale meldet Geräte nach 6 Monaten ab, außer key expiry ist aus. Die Einrichtungsseite zeigt das Datum.

## Nicht mehr nutzen

Drücke **Nicht mehr nutzen**, um wieder direkt zu gehen. **Auch bei Tailscale abmelden** meldet den Browser deiner Machine auch bei Tailscale ab. Die Admin-Konsole von Tailscale zeigt ihn dann als Expired, und dort kannst du ihn entfernen.
