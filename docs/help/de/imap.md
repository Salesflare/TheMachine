---
title: Andere E-Mail (IMAP)
area: connections
summary: E-Mails von beliebigen Anbietern mit IMAP, zum Beispiel iCloud, Yahoo, Fastmail, Telenet oder deiner eigenen Domain.
covers: connector:imap
code: imap_mail.py, smtp_mail.py, imap_presets.py, machine/sources/imap_setup.py
order: 13
translated: a21e9d52d723f351
---
## Was sie liest

Deinen Posteingang und deinen Ordner „Gesendet“: die letzten 7 Tage beim Verbinden und danach alle neuen E-Mails. Auch deine gesendeten E-Mails zählen. So lernt sie, wie du schreibst und was du versprochen hast. Andere Ordner werden nicht gelesen.

In deinem Postfach wird nichts verändert, abgesehen von einer Kopie der E-Mails, die The Machine sendet, in deinem Ordner „Gesendet“. E-Mails werden nicht als gelesen markiert.

## Was sie kann

Sie sendet E-Mails erst, wenn du auf **Senden** klickst. Dafür verwendet sie den Mailserver deines Anbieters (SMTP) mit demselben Passwort. Eine Kopie landet in deinem Ordner „Gesendet“. Antworten bleiben im selben Thread. Deine Signatur stammt aus den **Einstellungen**, andernfalls aus dem Ende deiner gesendeten E-Mails.

## Verbinden

1. Öffne im Dashboard **Verbindungen**, dann **E-Mail**, und wähle **Andere E-Mail** aus.
2. Gib deine E-Mail-Adresse und dein Passwort ein.
3. Klicke auf **Verbinden**.

Viele Anbieter verlangen für Mail-Apps ein App-Passwort statt deines normalen Passworts. Erstelle es in den Kontoeinstellungen deines Anbieters:

- iCloud: ein app-spezifisches Passwort unter account.apple.com.
- Yahoo: Account security, Generate app password.
- Fastmail: Settings, Privacy and security, App passwords.
- Telenet: dein normales Telenet-Mail-Passwort.
- Zoho Mail mit Zwei-Faktor-Authentifizierung: ein anwendungsspezifisches Passwort in deinem Zoho-Konto unter Security.
- Proton Mail: Führe Proton Mail Bridge auf demselben Computer aus und verwende das von Bridge angezeigte Passwort. Das funktioniert nur, wenn The Machine ebenfalls auf diesem Computer läuft. The Machine zeigt den Fingerabdruck des Bridge-Zertifikats an und vertraut nur diesem Zertifikat.

Für die meisten Anbieter werden die Servereinstellungen automatisch ausgefüllt. Ist dein Anbieter nicht dabei? Öffne **Servereinstellungen** und gib die Angaben ein, die dein Anbieter für Mail-Apps bereitstellt: die IMAP- und SMTP-Server, ihre Ports und die Sicherheitseinstellungen (SSL/TLS oder STARTTLS). The Machine verbindet sich nie ohne TLS.

Verwendest du Gmail oder Microsoft-Mail, auch mit deiner eigenen Domain? Wähle stattdessen **Gmail** oder **Outlook** aus. Die Anmeldung funktioniert dort ohne Passwort. Auch Server, die du unter Servereinstellungen eingibst, gehören zu diesen Optionen: Microsoft akzeptiert keine Passwörter mehr von Mail-Apps.

Hast du eine Microsoft-365-Adresse eingegeben? Das Formular erkennt sie und zeigt statt des Passwortfelds **Mit Microsoft anmelden** an. Dadurch wird die Outlook-Anmeldung geöffnet. Wird die Adresse nicht innerhalb weniger Sekunden erkannt, bleibt das Passwortfeld bestehen.

## Wenn die Verbindung abbricht

- **Der Mailserver hat das Passwort abgelehnt**: Du hast es geändert oder das App-Passwort wurde entfernt. Verbinde das Konto erneut mit dem neuen Passwort.
- **Der Mailserver hat das Passwort zum Senden abgelehnt**: Es wurde nichts gesendet. Verbinde das Konto erneut. Wird das Passwort weiterhin abgelehnt, überprüfe den SMTP-Server unter Servereinstellungen. Bis dahin liest sie nur E-Mails.
- **Der Mailserver war nicht erreichbar**: Sie versucht es automatisch erneut. Schlägt es weiterhin fehl, überprüfe den Servernamen unter Servereinstellungen.
- **Das Zertifikat des Mailservers gilt für** einen anderen Namen: Bei Shared Hosting antwortet der Server oft mit seinem eigenen Namen. Gib den Namen ein, der unter Servereinstellungen angezeigt wird. The Machine überspringt die Zertifikatsprüfung nie.

## Verbindung entfernen

Öffne **Verbindungen**, wähle das Konto aus, dann **Details** und **Trennen**. Sie liest dann keine E-Mails mehr. Was sie bereits abgerufen hat, bleibt erhalten. Entferne das App-Passwort auch bei deinem Anbieter.
