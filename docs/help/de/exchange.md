---
title: Exchange Server
area: connections
summary: Termine von einem Exchange Server, den dein Unternehmen betreibt (2013 bis 2019 oder Subscription Edition). Nur lesender Zugriff.
covers: connector:exchange
code: ews_calendar.py, machine/sources/calendar_setup.py
order: 16
translated: f2b98c9bd4f08dba
---
## Was gelesen wird

Deine Termine mit Gästen, Räumen und Notizen: die vergangene Woche und der nächste Monat beim Verbinden, danach jede Änderung. Sie erscheinen in **Kalender** und in der Meeting-Vorbereitung.

Der Zugriff ist nur lesend: Es werden keine Termine hinzugefügt, verschoben oder gelöscht. E-Mails von Exchange Server werden noch nicht gelesen.

## Microsoft 365 oder Exchange Server?

Exchange Server wird von deinem Unternehmen betrieben. Microsoft 365 (Exchange Online) ist die Cloud von Microsoft. Wähle dafür stattdessen **Outlook-Kalender**.

Gib zuerst deine Adresse ein. Wenn sie zu Microsoft 365 gehört, zeigt das Formular einen entsprechenden Hinweis und statt des Passwortfelds **Mit Microsoft anmelden**. Dadurch öffnet sich die Anmeldung für Outlook-Kalender, ganz ohne Passwort. Wird das nicht innerhalb weniger Sekunden erkannt oder betreibt dein Unternehmen einen eigenen Server, bleibt das Passwortfeld sichtbar.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **Kalender**, und wähle **Exchange Server**.
2. Gib deine geschäftliche E-Mail-Adresse und dein Windows-Passwort ein.
3. Klicke auf **Verbinden**.

Der Server wird anhand deiner Adresse gefunden (Autodiscover). Wird er nicht gefunden? Öffne **Servereinstellungen** und gib den Server ein, den dir dein IT-Team für Outlook nennt, zum Beispiel `mail.example.com`. Meldest du dich mit einem anderen Namen als deiner Adresse an? Gib ihn unter **Benutzername** als `DOMAIN\name` ein.

Die Anmeldung erfolgt über NTLM oder Basic und ausschließlich über HTTPS.

## Wenn die Verbindung abbricht

- **Der Kalenderserver hat das Passwort abgelehnt**: Dein Windows-Passwort hat sich geändert. Verbinde den Kalender erneut.
- **Ein Microsoft 365-Postfach**: Dein Postfach wurde zu Microsoft 365 verschoben. Trenne diese Verbindung und verbinde **Outlook-Kalender**.
- **Der Kalenderserver war nicht erreichbar**: Es wird automatisch erneut versucht. Manche Server sind nur über das Unternehmensnetzwerk oder VPN erreichbar.

## Verbindung entfernen

Öffne **Verbindungen**, dann den Kalender und **Details**, und wähle **Trennen**. Bereits importierte Daten bleiben erhalten.
